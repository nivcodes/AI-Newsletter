"""
AI Newsletter Generator - Main Script
Consolidates all functionality for generating and sending AI newsletters
"""
import argparse
import logging
import sys
from datetime import datetime

# Import our utilities
from utils.content_fetcher import fetch_and_filter_articles
from utils.summarizer import generate_newsletter_content
from utils.html_processor import save_newsletter_files
from utils.modern_html_processor import save_modern_newsletter_files
from utils.email_sender import send_newsletter_email, test_email_config, send_test_email
from config import MAX_ARTICLES, OUTPUT_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('newsletter_generator.log')
    ]
)
logger = logging.getLogger(__name__)


def generate_newsletter(max_articles=None, style="rundown", save_files=True, output_dir=None):
    """
    Generate complete newsletter
    
    Args:
        max_articles (int): Maximum number of articles to include
        style (str): Newsletter style ('rundown' or 'basic')
        save_files (bool): Whether to save files to disk
        output_dir (str): Custom output directory
    
    Returns:
        dict: Generated content and file paths
    """
    logger.info("🚀 Starting AI Newsletter Generation...")
    
    try:
        # Step 1: Fetch and filter articles
        logger.info("📰 Fetching AI articles...")
        articles = fetch_and_filter_articles(max_articles or MAX_ARTICLES)
        
        if not articles:
            logger.error("❌ No AI articles found. Newsletter generation failed.")
            return None
        
        logger.info(f"✅ Found {len(articles)} AI articles")
        
        # Step 2: Generate content
        logger.info("🧠 Generating newsletter content...")
        content = generate_newsletter_content(articles, style=style)
        
        if not content or not content['summaries']:
            logger.error("❌ Failed to generate newsletter content.")
            return None
        
        logger.info(f"✅ Generated content with {len(content['summaries'])} summaries")
        
        # Step 3: Save files
        files_saved = {}
        if save_files:
            logger.info("💾 Saving newsletter files...")
            files_saved = save_newsletter_files(content, output_dir or OUTPUT_DIR)
            
            # Also generate modern version
            logger.info("✨ Generating modern newsletter design...")
            modern_files = save_modern_newsletter_files(content, output_dir or OUTPUT_DIR)
            files_saved.update(modern_files)
        
        result = {
            'content': content,
            'articles': articles,
            'files': files_saved,
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info("🎉 Newsletter generation completed successfully!")
        return result
        
    except Exception as e:
        logger.error(f"❌ Newsletter generation failed: {e}")
        return None


def send_newsletter(html_file_path=None, subject=None):
    """
    Send newsletter via email
    
    Args:
        html_file_path (str): Path to HTML file to send
        subject (str): Email subject line
    
    Returns:
        bool: Success status
    """
    logger.info("📧 Sending newsletter email...")
    
    # Use default styled HTML if no path provided
    if not html_file_path:
        html_file_path = f"{OUTPUT_DIR}/newsletter_styled.html"
    
    try:
        success = send_newsletter_email(html_file_path, subject)
        if success:
            logger.info("✅ Newsletter sent successfully!")
        else:
            logger.error("❌ Failed to send newsletter")
        return success
        
    except Exception as e:
        logger.error(f"❌ Error sending newsletter: {e}")
        return False


def main():
    """Main function with command-line interface"""
    parser = argparse.ArgumentParser(description='AI Newsletter Generator')
    
    # Generation options
    parser.add_argument('--max-articles', type=int, default=MAX_ARTICLES,
                       help='Maximum number of articles to include')
    parser.add_argument('--style', choices=['rundown', 'basic'], default='rundown',
                       help='Newsletter style')
    parser.add_argument('--design', choices=['modern', 'classic'], default='modern',
                       help='Newsletter design (modern=beautiful responsive, classic=simple)')
    parser.add_argument('--output-dir', type=str, default=OUTPUT_DIR,
                       help='Output directory for generated files')
    
    # Actions
    parser.add_argument('--generate-only', action='store_true',
                       help='Generate newsletter without sending email')
    parser.add_argument('--send-only', action='store_true',
                       help='Send existing newsletter without regenerating')
    parser.add_argument('--test-email', action='store_true',
                       help='Test email configuration')
    parser.add_argument('--send-test', action='store_true',
                       help='Send test email')
    
    # Email options
    parser.add_argument('--html-file', type=str,
                       help='Specific HTML file to send (for --send-only)')
    parser.add_argument('--subject', type=str,
                       help='Custom email subject')
    
    # Utility options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress most output')
    
    args = parser.parse_args()
    
    # Adjust logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Execute based on arguments
    try:
        if args.test_email:
            logger.info("🔧 Testing email configuration...")
            success = test_email_config()
            sys.exit(0 if success else 1)
        
        elif args.send_test:
            logger.info("📧 Sending test email...")
            success = send_test_email()
            sys.exit(0 if success else 1)
        
        elif args.send_only:
            logger.info("📧 Sending existing newsletter...")
            html_file = args.html_file or f"{args.output_dir}/newsletter_styled.html"
            success = send_newsletter(html_file, args.subject)
            sys.exit(0 if success else 1)
        
        else:
            # Generate newsletter (default action)
            result = generate_newsletter(
                max_articles=args.max_articles,
                style=args.style,
                save_files=True,
                output_dir=args.output_dir
            )
            
            if not result:
                logger.error("❌ Newsletter generation failed")
                sys.exit(1)
            
            # Send email unless generate-only is specified
            if not args.generate_only:
                # Choose which version to send based on design preference
                if args.design == 'modern':
                    html_path = result['files'].get('modern_html') or result['files'].get('styled_html')
                else:
                    html_path = result['files'].get('styled_html')
                
                if html_path:
                    success = send_newsletter(html_path, args.subject)
                    if not success:
                        logger.warning("⚠️ Newsletter generated but email sending failed")
                        sys.exit(1)
                else:
                    logger.error("❌ No HTML file found to send")
                    sys.exit(1)
            
            logger.info("🎉 All operations completed successfully!")
            
            # Print summary
            print("\n" + "="*50)
            print("📊 NEWSLETTER GENERATION SUMMARY")
            print("="*50)
            print(f"Articles processed: {len(result['articles'])}")
            print(f"Summaries generated: {len(result['content']['summaries'])}")
            print(f"Style: {args.style}")
            print(f"Output directory: {args.output_dir}")
            
            if result['files']:
                print("\nFiles generated:")
                for file_type, path in result['files'].items():
                    print(f"  {file_type}: {path}")
            
            if not args.generate_only:
                print(f"\n✅ Newsletter sent successfully!")
            
            print("="*50)
    
    except KeyboardInterrupt:
        logger.info("⏹️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
