"""
Email sending utilities for AI Newsletter Generator
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import EMAIL_CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def send_newsletter_email(html_file_path, subject=None, custom_config=None):
    """Send newsletter email using HTML file"""
    
    # Use custom config if provided, otherwise use default
    config = custom_config if custom_config else EMAIL_CONFIG
    
    # Validate configuration
    required_fields = ['from_email', 'to_email', 'smtp_server', 'smtp_port', 'smtp_user', 'smtp_password']
    for field in required_fields:
        if not config.get(field):
            logger.error(f"Missing email configuration: {field}")
            return False
    
    # Default subject if not provided
    if not subject:
        from datetime import datetime
        subject = f"🧠 Your AI News Digest – {datetime.today().strftime('%B %d, %Y')}"
    
    try:
        # Read HTML content
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = config['from_email']
        msg["To"] = config['to_email']
        
        # Add HTML part
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        # Send email
        logger.info(f"📧 Sending email to {config['to_email']}...")
        
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            server.login(config['smtp_user'], config['smtp_password'])
            server.sendmail(config['from_email'], config['to_email'], msg.as_string())
        
        logger.info(f"✅ Email sent successfully to {config['to_email']}")
        return True
        
    except FileNotFoundError:
        logger.error(f"HTML file not found: {html_file_path}")
        return False
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def send_newsletter_content(html_content, subject=None, custom_config=None):
    """Send newsletter email using HTML content string"""
    
    # Use custom config if provided, otherwise use default
    config = custom_config if custom_config else EMAIL_CONFIG
    
    # Validate configuration
    required_fields = ['from_email', 'to_email', 'smtp_server', 'smtp_port', 'smtp_user', 'smtp_password']
    for field in required_fields:
        if not config.get(field):
            logger.error(f"Missing email configuration: {field}")
            return False
    
    # Default subject if not provided
    if not subject:
        from datetime import datetime
        subject = f"🧠 Your AI News Digest – {datetime.today().strftime('%B %d, %Y')}"
    
    try:
        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = config['from_email']
        msg["To"] = config['to_email']
        
        # Add HTML part
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)
        
        # Send email
        logger.info(f"📧 Sending email to {config['to_email']}...")
        
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            server.login(config['smtp_user'], config['smtp_password'])
            server.sendmail(config['from_email'], config['to_email'], msg.as_string())
        
        logger.info(f"✅ Email sent successfully to {config['to_email']}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def test_email_config(custom_config=None):
    """Test email configuration without sending actual newsletter"""
    
    config = custom_config if custom_config else EMAIL_CONFIG
    
    # Check if all required fields are present
    required_fields = ['from_email', 'to_email', 'smtp_server', 'smtp_port', 'smtp_user', 'smtp_password']
    missing_fields = [field for field in required_fields if not config.get(field)]
    
    if missing_fields:
        logger.error(f"Missing email configuration fields: {', '.join(missing_fields)}")
        return False
    
    try:
        # Test SMTP connection
        logger.info("🔧 Testing SMTP connection...")
        
        with smtplib.SMTP_SSL(config['smtp_server'], config['smtp_port']) as server:
            server.login(config['smtp_user'], config['smtp_password'])
        
        logger.info("✅ Email configuration test successful")
        return True
        
    except Exception as e:
        logger.error(f"Email configuration test failed: {e}")
        return False


def send_test_email(custom_config=None):
    """Send a test email to verify configuration"""
    
    test_html = """
    <html>
    <body>
        <h1>🧪 AI Newsletter Test Email</h1>
        <p>This is a test email to verify your newsletter email configuration is working correctly.</p>
        <p>If you received this email, your setup is ready to send newsletters!</p>
    </body>
    </html>
    """
    
    return send_newsletter_content(
        html_content=test_html,
        subject="🧪 AI Newsletter Configuration Test",
        custom_config=custom_config
    )
