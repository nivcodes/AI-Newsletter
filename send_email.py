import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(subject, html_path, to_email, from_email, smtp_server, smtp_port, smtp_user, smtp_password):
    with open(html_path, 'r') as f:
        html_content = f.read()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(smtp_user, smtp_password)
        server.sendmail(from_email, to_email, msg.as_string())

    print(f"✅ Email sent to {to_email}")

send_email(
    subject="🧠 Your AI News Digest – Test Edition",
    html_path="newsletter_premium.html",
    to_email=os.getenv("EMAIL_TO"),
    from_email=os.getenv("EMAIL_FROM"),
    smtp_server=os.getenv("SMTP_SERVER"),
    smtp_port=int(os.getenv("SMTP_PORT")),
    smtp_user=os.getenv("EMAIL_USER"),
    smtp_password=os.getenv("EMAIL_PASSWORD")
)
