from markdown import markdown
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# === CONVERT MARKDOWN TO HTML ===
def convert_markdown_to_html(md_file, html_file):
    with open(md_file, 'r') as f:
        md_text = f.read()
    html_text = markdown(md_text, extensions=['extra', 'smarty'])
    with open(html_file, 'w') as f:
        f.write(html_text)
    return html_file

# === SEND EMAIL ===
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

    return f"Email sent to {to_email} with subject '{subject}'"

# Convert newsletter.md to HTML
html_output_path = "newsletter.html"
convert_markdown_to_html("newsletter.md", html_output_path)

html_output_path  # Show output path for user to verify before sending email
