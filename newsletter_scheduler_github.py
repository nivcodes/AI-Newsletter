#!/usr/bin/env python3
"""
AI Newsletter Scheduler for GitHub Actions
Cloud-optimized version with enhanced logging and error handling
"""
import argparse
import logging
import sys
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
import holidays
import os

# Import newsletter components
from enhanced_newsletter_generator import generate_enhanced_newsletter, send_enhanced_newsletter
from config import EMAIL_CONFIG, OUTPUT_DIR

# GitHub Actions optimized configuration
SCHEDULE_CONFIG = {
    'SCHEDULE_TIME': "07:00",  # 7 AM Eastern
    'SCHEDULE_DAYS': [1, 2, 3, 4, 5],  # Monday-Friday (1=Monday, 7=Sunday)
    'RETRY_ATTEMPTS': 2,  # Reduced for cloud environment
    'RETRY_DELAY_MINUTES': 5,  # Shorter delay for cloud
    'SKIP_HOLIDAYS': True,
    'LOG_RETENTION_DAYS': 7  # Shorter retention for cloud
}

# Set up logging optimized for GitHub Actions
def setup_logging():
    """Set up comprehensive logging optimized for GitHub Actions"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    log_file = log_dir / "newsletter_scheduler_github.log"
    
    # Configure logging with both file and console output
    # GitHub Actions captures console output automatically
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


def log_github_actions_output(message, is_error=False):
    """
    Log messages in GitHub Actions format for better visibility
    
    Args:
        message (str): Message to log
        is_error (bool): Whether this is an error message
    """
    if is_error:
        print(f"::error::{message}")
    else:
        print(f"::notice::{message}")
    
    # Also log normally
    if is_error:
        logger.error(message)
    else:
        logger.info(message)


def generate_and_send_newsletter():
    """
    Generate and send newsletter with comprehensive error handling
    Optimized for GitHub Actions environment
    
    Returns:
        tuple: (success: bool, message: str, stats: dict)
    """
    try:
        logger.info("🚀 Starting newsletter generation in GitHub Actions...")
        log_github_actions_output("Starting AI Newsletter generation")
        
        # Generate newsletter with cloud-optimized settings
        result = generate_enhanced_newsletter(
            max_articles=12,
            style="editorial",
            save_files=True,
            output_dir=OUTPUT_DIR,
            fetch_images=True  # Keep images for full experience
        )
        
        if not result:
            error_msg = "Newsletter generation failed - no result returned"
            log_github_actions_output(error_msg, is_error=True)
            return False, error_msg, {}
        
        logger.info("✅ Newsletter generated successfully")
        log_github_actions_output("Newsletter generated successfully")
        
        # Send newsletter
        html_file = result['files'].get('email_html') or result['files'].get('premium_html')
        if not html_file:
            error_msg = "No HTML file found to send"
            log_github_actions_output(error_msg, is_error=True)
            return False, error_msg, result.get('stats', {})
        
        logger.info("📧 Sending newsletter email...")
        email_success = send_enhanced_newsletter(html_file)
        
        if not email_success:
            error_msg = "Newsletter generated but email sending failed"
            log_github_actions_output(error_msg, is_error=True)
            return False, error_msg, result.get('stats', {})
        
        logger.info("🎉 Newsletter sent successfully!")
        log_github_actions_output("Newsletter sent successfully!")
        
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
🌐 Generated in GitHub Actions cloud environment
"""
        
        # Log stats in GitHub Actions format
        log_github_actions_output(f"Articles processed: {stats.get('total_articles', 0)}")
        log_github_actions_output(f"Summaries generated: {stats.get('summaries_generated', 0)}")
        log_github_actions_output(f"Categories covered: {stats.get('categories', 0)}")
        
        return True, success_message, stats
        
    except Exception as e:
        error_msg = f"Unexpected error during newsletter generation: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
        logger.error(error_msg)
        log_github_actions_output(f"Newsletter generation failed: {str(e)}", is_error=True)
        return False, error_msg, {}


def run_scheduled_newsletter():
    """
    Main scheduler function with retry logic
    Optimized for GitHub Actions environment
    
    Returns:
        bool: Overall success status
    """
    logger.info("🕐 Newsletter scheduler started in GitHub Actions")
    log_github_actions_output("AI Newsletter Scheduler started")
    
    # Check if we should run today
    should_run, reason = should_run_today()
    if not should_run:
        logger.info(f"⏭️ Skipping newsletter today: {reason}")
        log_github_actions_output(f"Skipping newsletter: {reason}")
        return True  # Not an error, just skipped
    
    logger.info(f"✅ Running newsletter: {reason}")
    log_github_actions_output(f"Running newsletter: {reason}")
    
    # Attempt newsletter generation with retries
    for attempt in range(1, SCHEDULE_CONFIG['RETRY_ATTEMPTS'] + 1):
        logger.info(f"📝 Newsletter generation attempt {attempt}/{SCHEDULE_CONFIG['RETRY_ATTEMPTS']}")
        log_github_actions_output(f"Attempt {attempt}/{SCHEDULE_CONFIG['RETRY_ATTEMPTS']}")
        
        success, message, stats = generate_and_send_newsletter()
        
        if success:
            # Success!
            logger.info("🎉 Newsletter scheduler completed successfully")
            log_github_actions_output("Newsletter scheduler completed successfully")
            
            # Output summary for GitHub Actions
            print("\n" + "="*60)
            print("📊 NEWSLETTER GENERATION SUMMARY")
            print("="*60)
            print(message)
            print("="*60)
            
            return True
        
        # Failed attempt
        logger.error(f"❌ Attempt {attempt} failed: {message}")
        log_github_actions_output(f"Attempt {attempt} failed", is_error=True)
        
        # If we have more attempts, wait and retry
        if attempt < SCHEDULE_CONFIG['RETRY_ATTEMPTS']:
            wait_minutes = SCHEDULE_CONFIG['RETRY_DELAY_MINUTES']
            logger.info(f"⏳ Waiting {wait_minutes} minutes before retry...")
            log_github_actions_output(f"Waiting {wait_minutes} minutes before retry")
            time.sleep(wait_minutes * 60)
        else:
            # Final failure
            failure_message = f"Newsletter generation failed after {SCHEDULE_CONFIG['RETRY_ATTEMPTS']} attempts."
            logger.error("💥 Newsletter scheduler failed after all retry attempts")
            log_github_actions_output(failure_message, is_error=True)
            
            # Output failure summary
            print("\n" + "="*60)
            print("❌ NEWSLETTER GENERATION FAILED")
            print("="*60)
            print(f"Failed after {SCHEDULE_CONFIG['RETRY_ATTEMPTS']} attempts")
            print(f"Last error: {message}")
            print("Check the logs above for detailed error information.")
            print("="*60)
            
            return False
    
    return False


def test_configuration():
    """Test scheduler configuration and dependencies"""
    logger.info("🧪 Testing scheduler configuration in GitHub Actions...")
    log_github_actions_output("Testing configuration")
    
    errors = []
    
    # Test email configuration
    try:
        from utils.email_sender import test_email_config
        if not test_email_config():
            errors.append("Email configuration test failed")
    except Exception as e:
        errors.append(f"Email configuration error: {e}")
    
    # Test newsletter generation (dry run with minimal resources)
    try:
        logger.info("Testing newsletter generation (dry run)...")
        result = generate_enhanced_newsletter(
            max_articles=2,  # Very small test for cloud
            save_files=False,  # Don't save files
            fetch_images=False  # Skip images for speed
        )
        if not result:
            errors.append("Newsletter generation test failed")
        else:
            logger.info("✅ Newsletter generation test passed")
            log_github_actions_output("Newsletter generation test passed")
    except Exception as e:
        errors.append(f"Newsletter generation test error: {e}")
    
    # Test holiday checking
    try:
        should_run, reason = should_run_today()
        logger.info(f"Schedule check: {reason}")
        log_github_actions_output(f"Schedule check: {reason}")
    except Exception as e:
        errors.append(f"Schedule checking error: {e}")
    
    # Test environment variables
    required_env_vars = ['EMAIL_FROM', 'EMAIL_TO', 'EMAIL_USER', 'EMAIL_PASSWORD', 'SMTP_SERVER']
    missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
    if missing_env_vars:
        errors.append(f"Missing environment variables: {', '.join(missing_env_vars)}")
    
    if errors:
        logger.error("❌ Configuration test failed:")
        for error in errors:
            logger.error(f"  • {error}")
            log_github_actions_output(error, is_error=True)
        return False
    else:
        logger.info("✅ All configuration tests passed!")
        log_github_actions_output("All configuration tests passed!")
        return True


def main():
    """Main entry point with command line interface"""
    parser = argparse.ArgumentParser(
        description='AI Newsletter Scheduler for GitHub Actions',
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
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Log GitHub Actions environment info
    if os.getenv('GITHUB_ACTIONS'):
        log_github_actions_output("Running in GitHub Actions environment")
        log_github_actions_output(f"Workflow: {os.getenv('GITHUB_WORKFLOW', 'Unknown')}")
        log_github_actions_output(f"Run ID: {os.getenv('GITHUB_RUN_ID', 'Unknown')}")
    
    try:
        if args.test:
            success = test_configuration()
            if success:
                log_github_actions_output("Configuration test completed successfully")
            sys.exit(0 if success else 1)
        
        elif args.dry_run:
            logger.info("🧪 Dry run mode - generating newsletter without sending")
            log_github_actions_output("Running in dry-run mode")
            success, message, stats = generate_and_send_newsletter()
            if success:
                logger.info("✅ Dry run completed successfully")
                log_github_actions_output("Dry run completed successfully")
                print(f"\n{message}")
            else:
                logger.error(f"❌ Dry run failed: {message}")
                log_github_actions_output("Dry run failed", is_error=True)
            sys.exit(0 if success else 1)
        
        elif args.force:
            logger.info("🚀 Force mode - running regardless of schedule")
            log_github_actions_output("Running in force mode")
            success, message, stats = generate_and_send_newsletter()
            if success:
                log_github_actions_output("Force run completed successfully")
            else:
                log_github_actions_output("Force run failed", is_error=True)
            sys.exit(0 if success else 1)
        
        else:
            # Normal scheduled run
            success = run_scheduled_newsletter()
            sys.exit(0 if success else 1)
    
    except KeyboardInterrupt:
        logger.info("⏹️ Scheduler interrupted by user")
        log_github_actions_output("Scheduler interrupted", is_error=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"💥 Unexpected scheduler error: {e}")
        logger.error(traceback.format_exc())
        log_github_actions_output(f"Unexpected error: {str(e)}", is_error=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
