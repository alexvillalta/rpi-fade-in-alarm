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

    removed_any = False
    for comment in COMMENTS:
        jobs = list(cron.find_comment(comment))
        if jobs:
            for job in jobs:
                cron.remove(job)
            print(f"Removed {len(jobs)} job(s) with comment '{comment}'.")
            removed_any = True

    if removed_any:
        cron.write()
        print("Crontab updated.")
    else:
        print("No alarms were set.")

if __name__ == "__main__":
    main()