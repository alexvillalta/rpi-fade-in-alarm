import os
import sys
from crontab import CronTab

"""
set_alarm.py

Usage:
    python3 set_alarm.py <hour> <minute> <lights_offset_minutes>

Creates two daily cron jobs using python-crontab:
- lights.py runs at (hour:minute) minus lights_offset_minutes
- sound.sh runs at hour:minute

Both commands use absolute paths based on this script's location.

Assisted by Microsoft Copilot
"""

def error_exit(message: str, code: int = 1):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(code)

def parse_args(argv):
    if len(argv) != 5 and len(argv) != 6:
        error_exit("Expected these arguments: <hour> <minute> <lights_offset_minutes> <weather_offset_minutes> <OPTIONAL weather_location>")

    try:
        hour = int(argv[1])
        minute = int(argv[2])
        lights_offset_minutes = int(argv[3])
        weather_offset_minutes = int(argv[4])
        if len(argv) == 6:
            weather_location = str(argv[5])
        else:
            weather_location = ""
    except ValueError:
        error_exit("First 4 arguments must be integers and weather_location must be a string")

    if not (0 <= hour <= 23):
        error_exit("Hour must be between 0 and 23")
    if not (0 <= minute <= 59):
        error_exit("Minute must be between 0 and 59")
    if lights_offset_minutes < 0:
        error_exit("Lights offset (minutes) must be non-negative")
    if weather_offset_minutes < 0:
        error_exit("Weather offset (minutes) must be non-negative")
    return hour, minute, lights_offset_minutes, weather_offset_minutes, weather_location

def compute_offset_time(hour: int, minute: int, offset_minutes: int):
    total_minutes = (hour * 60 + minute + offset_minutes) % (24 * 60)
    target_hour = total_minutes // 60
    target_minute = total_minutes % 60
    return target_hour, target_minute

def main():
    hour, minute, lights_offset_minutes, weather_offset_minutes, weather_location = parse_args(sys.argv)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    lights_script = os.path.join(script_dir, "lights.py")
    sound_script = os.path.join(script_dir, "sound.sh")
    weather_script = os.path.join(script_dir, "weather.sh")

    if not os.path.isfile(lights_script):
        error_exit(f"lights.py not found at {lights_script}")
    if not os.path.isfile(sound_script):
        error_exit(f"sound.sh not found at {sound_script}")
    if not os.path.isfile(weather_script):
        error_exit(f"sound.sh not found at {weather_script}")

    lights_hour, lights_minute = compute_offset_time(hour, minute, -lights_offset_minutes)
    weather_hour, weather_minute = compute_offset_time(hour, minute, weather_offset_minutes)

    try:
        cron = CronTab(user=True)
    except Exception as e:
        error_exit(f"Failed to access crontab: {e}")

    # Add some required env variables to crontab 
    # TODO: find more elegant way to do this without needing to specify these here
    env_vars_required = [
        "PATH", 
        "XDG_SESSION_TYPE", 
        "XDG_SESSION_ID", 
        "XDG_RUNTIME_DIR", 
        "SSH_CONNECTION", 
        "SSH_CLIENT", 
        "SSH_TTY", 
        "TEXTDOMAIN", 
        "DBUS_SESSION_BUS_ADDRESS",
    ]
    for var_name in env_vars_required:
        if var_name in os.environ:
            var_value = os.environ[var_name]
            cron.env[var_name] = var_value
            print(f"Set cron env variable: {var_name}={var_value}")
        else:
            print(f"Warning: env variable '{var_name}' not found in current user's env variables")

    # Remove any existing jobs created by this script to avoid duplicates
    lights_comment = "rpi-fade-in-alarm-lights"
    sound_comment = "rpi-fade-in-alarm-sound"
    weather_comment = "rpi-fade-in-alarm-weather"
    cron.remove_all(comment=lights_comment)
    cron.remove_all(comment=sound_comment)
    cron.remove_all(comment=weather_comment)

    # Create lights job (use python3 to run lights.py)
    lights_command = f"/usr/bin/python3 {lights_script}"
    lights_job = cron.new(command=lights_command, comment=lights_comment)
    lights_job.setall(f"{lights_minute} {lights_hour} * * *")

    # Create sound job (use bash to run sound.sh)
    sound_command = f"/bin/bash {sound_script}"
    sound_job = cron.new(command=sound_command, comment=sound_comment)
    sound_job.setall(f"{minute} {hour} * * *")

    # Create weather job (use bash to run weather.sh)
    weather_command = f"/bin/bash {weather_script}" + ("" if weather_location == "" else f" {weather_location}")
    weather_job = cron.new(command=weather_command, comment=weather_comment)
    weather_job.setall(f"{weather_minute} {weather_hour} * * *")

    try:
        cron.write()
    except Exception as e:
        error_exit(f"Failed to write crontab: {e}")

    print(f"Installed cron jobs:")
    print(f" - lights.py at {lights_hour:02d}:{lights_minute:02d} (offset -{lights_offset_minutes} min)")
    print(f" - sound.sh at {hour:02d}:{minute:02d}")
    print(f" - weather.sh at {weather_hour:02d}:{weather_minute:02d} (offset {weather_offset_minutes} min)")

if __name__ == "__main__":
    main()