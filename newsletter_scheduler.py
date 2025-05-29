#!/usr/bin/env python3
"""
AI Newsletter Scheduler
Handles automated daily newsletter generation with retry logic, holiday checking, and admin notifications
"""
import argparse
import logging
import sys
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
import holidays
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Import newsletter components
from enhanced_newsletter_generator import generate_enhanced_newsletter, send_enhanced_newsletter
from config import EMAIL_CONFIG, OUTPUT_DIR

# Scheduler Configuration
SCHEDULE_CONFIG = {
    'SCHEDULE_TIME': "07:00",  # 7 AM
    'SCHEDULE_DAYS': [1, 2, 3, 4, 5],  # Monday-Friday (1=Monday, 7=Sunday)
    'RETRY_ATTEMPTS': 3,
    'RETRY_DELAY_MINUTES': 10,
    'SKIP_HOLIDAYS': True,
    'ADMIN_EMAIL': EMAIL_CONFIG.get('to_email'),  # Default to newsletter recipient
    'LOG_RETENTION_DAYS': 30
}

# Set up logging
def setup_logging():
    """Set up comprehensive logging for scheduler"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "newsletter_scheduler.log"
    
    # Configure logging with both file and console output
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_logging()


def should_run_today():
    """
    Check if newsletter should run today based on schedule and holidays
    
    Returns:
        tuple: (should_run: bool, reason: str)
    """
    now = datetime.now()
    
    # Check if today is a scheduled day (Monday=1, Sunday=7)
    weekday = now.isoweekday()
    if weekday not in SCHEDULE_CONFIG['SCHEDULE_DAYS']:
        return False, f"Not a scheduled day (today is {now.strftime('%A')})"
    
    # Check holidays if enabled
    if SCHEDULE_CONFIG['SKIP_HOLIDAYS']:
        us_holidays = holidays.US()
        if now.date() in us_holidays:
            holiday_name = us_holidays[now.date()]
            return False, f"Holiday: {holiday_name}"
    
    return True, "Scheduled day, no holidays"


def send_admin_notification(subject, message, is_success=True):
    """
    Send notification email to admin
    
    Args:
        subject (str): Email subject
        message (str): Email body
        is_success (bool): Whether this is a success or failure notification
    """
    admin_email = SCHEDULE_CONFIG['ADMIN_EMAIL']
    if not admin_email:
        logger.warning("No admin email configured for notifications")
        return False
    
    try:
        # Create email
        msg = MIMEMultipart()
        msg["Subject"] = f"🤖 AI Newsletter Scheduler: {subject}"
        msg["From"] = EMAIL_CONFIG['from_email']
        msg["To"] = admin_email
        
        # Add emoji based on success/failure
        emoji = "✅" if is_success else "❌"
        html_content = f"""
        <html>
        <body>
            <h2>{emoji} AI Newsletter Scheduler Report</h2>
            <p><strong>Time:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <p><strong>Status:</strong> {subject}</p>
            <div style="background-color: {'#d4edda' if is_success else '#f8d7da'}; 
                        border: 1px solid {'#c3e6cb' if is_success else '#f5c6cb'}; 
                        padding: 15px; margin: 10px 0; border-radius: 5px;">
                <pre>{message}</pre>
            </div>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(html_content, "html"))
        
        # Send email
        with smtplib.SMTP_SSL(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
            server.login(EMAIL_CONFIG['smtp_user'], EMAIL_CONFIG['smtp_password'])
            server.sendmail(EMAIL_CONFIG['from_email'], admin_email, msg.as_string())
        
        logger.info(f"Admin notification sent: {subject}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send admin notification: {e}")
        return False


def generate_and_send_newsletter():
    """
    Generate and send newsletter with comprehensive error handling
    
    Returns:
        tuple: (success: bool, message: str, stats: dict)
    """
    try:
        logger.info("🚀 Starting newsletter generation...")
        
        # Generate newsletter
        result = generate_enhanced_newsletter(
            max_articles=12,
            style="editorial",
            save_files=True,
            output_dir=OUTPUT_DIR,
            fetch_images=True
        )
        
        if not result:
            return False, "Newsletter generation failed - no result returned", {}
        
        logger.info("✅ Newsletter generated successfully")
        
        # Send newsletter
        html_file = result['files'].get('email_html') or result['files'].get('premium_html')
        if not html_file:
            return False, "No HTML file found to send", result.get('stats', {})
        
        logger.info("📧 Sending newsletter email...")
        email_success = send_enhanced_newsletter(html_file)
        
        if not email_success:
            return False, "Newsletter generated but email sending failed", result.get('stats', {})
        
        logger.info("🎉 Newsletter sent successfully!")
        
        # Return success with stats
        stats = result.get('stats', {})
        success_message = f"""Newsletter generated and sent successfully!

📊 Generation Stats:
• Articles processed: {stats.get('total_articles', 0)}
• Summaries generated: {stats.get('summaries_generated', 0)}
• Categories covered: {stats.get('categories', 0)}
• Images processed: {stats.get('images_processed', 0)}

📁 Files generated: {len(result.get('files', {}))}
📧 Email sent to: {EMAIL_CONFIG.get('to_email', 'configured recipient')}
"""
        
        return True, success_message, stats
        
    except Exception as e:
        error_msg = f"Unexpected error during newsletter generation: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        logger.error(error_msg)
        return False, error_msg, {}


def run_scheduled_newsletter():
    """
    Main scheduler function with retry logic
    
    Returns:
        bool: Overall success status
    """
    logger.info("🕐 Newsletter scheduler started")
    
    # Check if we should run today
    should_run, reason = should_run_today()
    if not should_run:
        logger.info(f"⏭️ Skipping newsletter today: {reason}")
        return True  # Not an error, just skipped
    
    logger.info(f"✅ Running newsletter: {reason}")
    
    # Attempt newsletter generation with retries
    for attempt in range(1, SCHEDULE_CONFIG['RETRY_ATTEMPTS'] + 1):
        logger.info(f"📝 Newsletter generation attempt {attempt}/{SCHEDULE_CONFIG['RETRY_ATTEMPTS']}")
        
        success, message, stats = generate_and_send_newsletter()
        
        if success:
            # Success! Send admin notification
            send_admin_notification("Newsletter Sent Successfully", message, is_success=True)
            logger.info("🎉 Newsletter scheduler completed successfully")
            return True
        
        # Failed attempt
        logger.error(f"❌ Attempt {attempt} failed: {message}")
        
        # If we have more attempts, wait and retry
        if attempt < SCHEDULE_CONFIG['RETRY_ATTEMPTS']:
            wait_minutes = SCHEDULE_CONFIG['RETRY_DELAY_MINUTES']
            logger.info(f"⏳ Waiting {wait_minutes} minutes before retry...")
            time.sleep(wait_minutes * 60)
        else:
            # Final failure - send admin notification
            failure_message = f"""Newsletter generation failed after {SCHEDULE_CONFIG['RETRY_ATTEMPTS']} attempts.

Last error:
{message}

Please check the logs and system configuration.
"""
            send_admin_notification("Newsletter Generation Failed", failure_message, is_success=False)
            logger.error("💥 Newsletter scheduler failed after all retry attempts")
            return False
    
    return False


def cleanup_old_logs():
    """Clean up old log files"""
    try:
        log_dir = Path("logs")
        if not log_dir.exists():
            return
        
        cutoff_date = datetime.now() - timedelta(days=SCHEDULE_CONFIG['LOG_RETENTION_DAYS'])
        
        for log_file in log_dir.glob("*.log*"):
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                log_file.unlink()
                logger.info(f"Cleaned up old log file: {log_file}")
                
    except Exception as e:
        logger.warning(f"Failed to cleanup old logs: {e}")


def test_configuration():
    """Test scheduler configuration and dependencies"""
    logger.info("🧪 Testing scheduler configuration...")
    
    errors = []
    
    # Test email configuration
    try:
        from utils.email_sender import test_email_config
        if not test_email_config():
            errors.append("Email configuration test failed")
    except Exception as e:
        errors.append(f"Email configuration error: {e}")
    
    # Test newsletter generation (dry run)
    try:
        logger.info("Testing newsletter generation (dry run)...")
        result = generate_enhanced_newsletter(
            max_articles=3,  # Small test
            save_files=False,  # Don't save files
            fetch_images=False  # Skip images for speed
        )
        if not result:
            errors.append("Newsletter generation test failed")
        else:
            logger.info("✅ Newsletter generation test passed")
    except Exception as e:
        errors.append(f"Newsletter generation test error: {e}")
    
    # Test holiday checking
    try:
        should_run, reason = should_run_today()
        logger.info(f"Schedule check: {reason}")
    except Exception as e:
        errors.append(f"Schedule checking error: {e}")
    
    if errors:
        logger.error("❌ Configuration test failed:")
        for error in errors:
            logger.error(f"  • {error}")
        return False
    else:
        logger.info("✅ All configuration tests passed!")
        return True


def main():
    """Main entry point with command line interface"""
    parser = argparse.ArgumentParser(
        description='AI Newsletter Scheduler',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run scheduled newsletter
  %(prog)s --test            # Test configuration
  %(prog)s --force           # Force run regardless of schedule
  %(prog)s --dry-run         # Test generation without sending
        """
    )
    
    parser.add_argument('--test', action='store_true',
                       help='Test configuration and dependencies')
    parser.add_argument('--force', action='store_true',
                       help='Force run regardless of schedule/holidays')
    parser.add_argument('--dry-run', action='store_true',
                       help='Generate newsletter but do not send email')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--admin-email', type=str,
                       help='Override admin email for notifications')
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Override admin email if provided
    if args.admin_email:
        SCHEDULE_CONFIG['ADMIN_EMAIL'] = args.admin_email
    
    # Clean up old logs
    cleanup_old_logs()
    
    try:
        if args.test:
            success = test_configuration()
            sys.exit(0 if success else 1)
        
        elif args.dry_run:
            logger.info("🧪 Dry run mode - generating newsletter without sending")
            success, message, stats = generate_and_send_newsletter()
            if success:
                logger.info("✅ Dry run completed successfully")
                print(f"\n{message}")
            else:
                logger.error(f"❌ Dry run failed: {message}")
            sys.exit(0 if success else 1)
        
        elif args.force:
            logger.info("🚀 Force mode - running regardless of schedule")
            success, message, stats = generate_and_send_newsletter()
            if success:
                send_admin_notification("Newsletter Sent (Forced)", message, is_success=True)
            else:
                send_admin_notification("Newsletter Failed (Forced)", message, is_success=False)
            sys.exit(0 if success else 1)
        
        else:
            # Normal scheduled run
            success = run_scheduled_newsletter()
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        logger.info("⏹️ Scheduler interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected scheduler error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
