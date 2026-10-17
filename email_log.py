''' Emails last month's search log (logs/searches-YYYY-MM.csv) to the
    site's Gmail account, using MAIL_USERNAME and MAIL_PASSWORD from .env

    Run daily as a PythonAnywhere scheduled task; it only sends on the
    1st of the month:  python3 /home/<username>/citycounty/email_log.py
    To send a specific month now (e.g. for testing):  python3 email_log.py 2026-10
'''

import os
import smtplib
import sys
from datetime import date, timedelta
from email.message import EmailMessage
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")


def send_log(month):

    ''' Email the log file for month ("YYYY-MM") as an attachment '''

    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_PASSWORD")
    filename = f"searches-{month}.csv"
    log_path = os.path.join(LOG_DIR, filename)

    msg = EmailMessage()
    msg["Subject"] = f"MO City County search log: {month}"
    msg["From"] = username
    msg["To"] = username

    # attach the log, or note that there were no searches that month
    if os.path.exists(log_path):
        with open(log_path, "rb") as f:
            data = f.read()
        searches = max(data.count(b"\n") - 1, 0)    # minus header row
        msg.set_content(f"{searches} searches logged in {month}. Log file attached.")
        msg.add_attachment(data, maintype="text", subtype="csv", filename=filename)
    else:
        msg.set_content(f"No searches logged in {month}.")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(username, password)
        smtp.send_message(msg)
    print(f"Sent {filename} to {username}")


if __name__ == "__main__":
    load_dotenv(os.path.join(BASE_DIR, ".env"))

    # month given on command line: send it now
    if len(sys.argv) > 1:
        send_log(sys.argv[1])

    # scheduled run: on the 1st, send the month that just ended
    elif date.today().day == 1:
        last_month = date.today().replace(day=1) - timedelta(days=1)
        send_log(f"{last_month:%Y-%m}")
