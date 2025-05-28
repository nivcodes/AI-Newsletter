"""
Enhanced AI Newsletter Generator - Premium Edition
Integrates all enhanced components for a curated, visually compelling daily digest
"""
import argparse
import logging
import sys
from datetime import datetime

# Import enhanced utilities
from utils.enhanced_content_fetcher import fetch_and_filter_articles
from utils.enhanced_summarizer import generate_newsletter_content
from utils.premium_html_processor import save_premium_newsletter_files
from utils.image_fetcher import fetch_article_images
from utils.email_sender import send_newsletter_email, test_email_config, send_test_email
from config import MAX_ARTICLES, OUTPUT_DIR

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('enhanced_newsletter_generator.log')
    ]
)
logger = logging.getLogger(__name__)


def generate_enhanced_newsletter(max_articles=None, style="editorial", save_files=True, 
                               output_dir=None, fetch_images=True):
    """
    Generate enhanced newsletter with all premium features
    
    Args:
        max_articles (int): Maximum number of articles to include
        style (str): Newsletter style ('editorial' or 'rundown')
        save_files (bool): Whether to save files to disk
        output_dir (str): Custom output directory
        fetch_images (bool): Whether to fetch and process images
    
    Returns:
        dict: Generated content and file paths
    """
    logger.info("🚀 Starting Enhanced AI Newsletter Generation...")
    
    try:
        # Step 1: Fetch and filter articles with enhanced sources
        logger.info("📰 Fetching AI articles from multiple sources...")
        articles = fetch_and_filter_articles(max_articles or MAX_ARTICLES)
        
        if not articles:
            logger.error("❌ No AI articles found. Newsletter generation failed.")
            return None
        
        logger.info(f"✅ Found {len(articles)} AI articles")
        
        # Step 2: Fetch images for articles
        if fetch_images:
            logger.info("🖼️ Fetching images for articles...")
            articles = fetch_article_images(articles)
            logger.info("✅ Image processing completed")
        
        # Step 3: Generate enhanced content with editorial approach
        logger.info("🧠 Generating enhanced newsletter content...")
        content = generate_newsletter_content(articles, style=style)
        
        if not content or not content['summaries']:
            logger.error("❌ Failed to generate newsletter content.")
            return None
        
        logger.info(f"✅ Generated content with {len(content['summaries'])} summaries")
        
        # Log generation info
        gen_info = content.get('generation_info', {})
        logger.info(f"📊 Content generated using: {gen_info.get('llm_used', 'unknown')} LLM")
        logger.info(f"📊 Categories covered: {', '.join(gen_info.get('categories', []))}")
        
        if content.get('editors_takes'):
            logger.info(f"✍️ Generated {len(content['editors_takes'])} Editor's Takes")
        
        # Step 4: Save files in multiple formats
        files_saved = {}
        if save_files:
            logger.info("💾 Saving newsletter files in multiple formats...")
            files_saved = save_premium_newsletter_files(content, output_dir or OUTPUT_DIR)
        
        result = {
            'content': content,
            'articles': articles,
            'files': files_saved,
            'timestamp': datetime.now().isoformat(),
            'stats': {
                'total_articles': len(articles),
                'summaries_generated': len(content['summaries']),
                'editors_takes': len(content.get('editors_takes', [])),
                'categories': len(set(article.get('category', 'misc') for article in articles)),
                'images_processed': sum(1 for article in articles if article.get('image_info'))
            }
        }
        
        logger.info("🎉 Enhanced newsletter generation completed successfully!")
        return result
        
    except Exception as e:
        logger.error(f"❌ Enhanced newsletter generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return None


def send_enhanced_newsletter(html_file_path=None, subject=None):
    """
    Send enhanced newsletter via email
    
    Args:
        html_file_path (str): Path to HTML file to send
        subject (str): Email subject line
    
    Returns:
        bool: Success status
    """
    logger.info("📧 Sending enhanced newsletter email...")
    
    # Use premium email-optimized HTML if no path provided
    if not html_file_path:
        html_file_path = f"{OUTPUT_DIR}/newsletter_email_premium.html"
    
    try:
        success = send_newsletter_email(html_file_path, subject)
        if success:
            logger.info("✅ Enhanced newsletter sent successfully!")
        else:
            logger.error("❌ Failed to send enhanced newsletter")
        return success
        
    except Exception as e:
        logger.error(f"❌ Error sending enhanced newsletter: {e}")
        return False


def print_generation_summary(result):
    """Print a detailed summary of the generation process"""
    if not result:
        return
    
    stats = result.get('stats', {})
    files = result.get('files', {})
    
    print("\n" + "="*60)
    print("📊 ENHANCED NEWSLETTER GENERATION SUMMARY")
    print("="*60)
    
    # Statistics
    print(f"📰 Articles processed: {stats.get('total_articles', 0)}")
    print(f"📝 Summaries generated: {stats.get('summaries_generated', 0)}")
    print(f"✍️ Editor's Takes: {stats.get('editors_takes', 0)}")
    print(f"🏷️ Categories covered: {stats.get('categories', 0)}")
    print(f"🖼️ Images processed: {stats.get('images_processed', 0)}")
    
    # Generation info
    gen_info = result['content'].get('generation_info', {})
    print(f"🤖 LLM used: {gen_info.get('llm_used', 'unknown')}")
    print(f"⏰ Generated at: {result.get('timestamp', 'unknown')}")
    
    # Files generated
    if files:
        print(f"\n📁 Files generated ({len(files)}):")
        for file_type, path in files.items():
            print(f"  • {file_type}: {path}")
    
    # Categories breakdown
    articles = result.get('articles', [])
    if articles:
        from collections import Counter
        categories = Counter(article.get('category', 'misc') for article in articles)
        print(f"\n🏷️ Category breakdown:")
        for category, count in categories.most_common():
            from config import CATEGORIES
            emoji = CATEGORIES.get(category, {}).get('emoji', '📄')
            title = CATEGORIES.get(category, {}).get('title', category.title())
            print(f"  • {emoji} {title}: {count} articles")
    
    print("="*60)


def main():
    """Enhanced main function with comprehensive command-line interface"""
    parser = argparse.ArgumentParser(
        description='Enhanced AI Newsletter Generator - Premium Edition',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                                    # Generate and send newsletter
  %(prog)s --generate-only --max-articles 15 # Generate 15 articles, don't send
  %(prog)s --style editorial --fetch-images  # Use editorial style with images
  %(prog)s --send-only --html-file custom.html # Send existing file
  %(prog)s --test-email                       # Test email configuration
        """
    )
    
    # Generation options
    parser.add_argument('--max-articles', type=int, default=MAX_ARTICLES,
                       help=f'Maximum number of articles to include (default: {MAX_ARTICLES})')
    parser.add_argument('--style', choices=['editorial', 'rundown', 'basic'], default='editorial',
                       help='Newsletter style (default: editorial)')
    parser.add_argument('--output-dir', type=str, default=OUTPUT_DIR,
                       help=f'Output directory for generated files (default: {OUTPUT_DIR})')
    
    # Feature toggles
    parser.add_argument('--fetch-images', action='store_true', default=True,
                       help='Fetch and process images for articles (default: enabled)')
    parser.add_argument('--no-images', action='store_true',
                       help='Skip image fetching and processing')
    
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
    parser.add_argument('--use-premium', action='store_true', default=True,
                       help='Use premium email template (default: enabled)')
    
    # Utility options
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress most output')
    parser.add_argument('--summary', action='store_true', default=True,
                       help='Show generation summary (default: enabled)')
    parser.add_argument('--no-summary', action='store_true',
                       help='Skip generation summary')
    
    args = parser.parse_args()
    
    # Adjust logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    elif args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    # Handle image fetching flags
    fetch_images = args.fetch_images and not args.no_images
    show_summary = args.summary and not args.no_summary
    
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
            html_file = args.html_file
            if not html_file:
                if args.use_premium:
                    html_file = f"{args.output_dir}/newsletter_email_premium.html"
                else:
                    html_file = f"{args.output_dir}/newsletter_styled.html"
            
            success = send_enhanced_newsletter(html_file, args.subject)
            sys.exit(0 if success else 1)
        
        else:
            # Generate enhanced newsletter (default action)
            result = generate_enhanced_newsletter(
                max_articles=args.max_articles,
                style=args.style,
                save_files=True,
                output_dir=args.output_dir,
                fetch_images=fetch_images
            )
            
            if not result:
                logger.error("❌ Enhanced newsletter generation failed")
                sys.exit(1)
            
            # Show summary
            if show_summary:
                print_generation_summary(result)
            
            # Send email unless generate-only is specified
            if not args.generate_only:
                # Choose which version to send
                html_path = None
                if args.use_premium:
                    html_path = result['files'].get('email_html')
                
                if not html_path:
                    html_path = result['files'].get('premium_html')
                
                if html_path:
                    success = send_enhanced_newsletter(html_path, args.subject)
                    if not success:
                        logger.warning("⚠️ Newsletter generated but email sending failed")
                        sys.exit(1)
                else:
                    logger.error("❌ No HTML file found to send")
                    sys.exit(1)
            
            logger.info("🎉 All operations completed successfully!")
    
    except KeyboardInterrupt:
        logger.info("⏹️ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Unexpected error: {e}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
