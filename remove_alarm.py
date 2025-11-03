import sys
from crontab import CronTab

"""
remove_alarm.py

Remove any cron jobs created by set_alarm.py. Looks for jobs with comments
"rpi-fade-in-alarm-lights" and "rpi-fade-in-alarm-sound" and removes them.

Assisted by Microsoft Copilot
"""

COMMENTS = ("rpi-fade-in-alarm-lights", "rpi-fade-in-alarm-sound")

def main():
    try:
        cron = CronTab(user=True)
    except Exception as e:
        print(f"Failed to access user crontab: {e}")
        sys.exit(1)

    for comment in COMMENTS:
        cron.remove_all(comment=comment)

    cron.write()

if __name__ == "__main__":
    main()
