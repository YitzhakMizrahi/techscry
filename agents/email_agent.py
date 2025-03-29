# email_agent.py

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")


def send_email(subject: str, html_body: str):
    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USERNAME
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject

    # This is the key part that makes it render as HTML
    part = MIMEText(html_body, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
        print(f"📧 Email sent: {subject}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


if __name__ == "__main__":
    test_subject = "Test Email from TechScry"
    test_body = "This is a test email to confirm SMTP is working."
    send_email(test_subject, test_body)
