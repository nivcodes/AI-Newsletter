"""
Test script to generate newsletter using the fixed HTML processor
"""
import sys
import logging
from datetime import datetime

# Import the fixed components
from utils.enhanced_content_fetcher import fetch_and_filter_articles
from utils.enhanced_summarizer import generate_newsletter_content
from utils.fixed_html_processor import save_fixed_newsletter_files
from utils.image_fetcher import fetch_article_images

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_fixed_newsletter():
    """Test the fixed newsletter generation"""
    print("🚀 Testing Fixed AI Newsletter Generator")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Step 1: Fetch articles (small number for testing)
        print("\n📰 Fetching 3 articles for testing...")
        articles = fetch_and_filter_articles(max_articles=3)
        
        if not articles:
            print("❌ No articles fetched")
            return False
        
        print(f"✅ Found {len(articles)} articles")
        
        # Step 2: Fetch images (optional, can skip for faster testing)
        print("\n🖼️ Processing images...")
        articles = fetch_article_images(articles)
        print("✅ Image processing completed")
        
        # Step 3: Generate content
        print("\n🧠 Generating newsletter content...")
        content = generate_newsletter_content(articles, style="editorial")
        
        if not content or not content['summaries']:
            print("❌ Failed to generate content")
            return False
        
        print(f"✅ Generated {len(content['summaries'])} summaries")
        
        # Step 4: Generate fixed HTML
        print("\n🎨 Generating fixed HTML...")
        files = save_fixed_newsletter_files(content)
        
        if files and files.get('fixed_html'):
            print(f"✅ Fixed HTML generated: {files['fixed_html']}")
            
            # Show summary
            print("\n" + "="*50)
            print("📊 TEST RESULTS")
            print("="*50)
            print(f"Articles processed: {len(articles)}")
            print(f"Summaries generated: {len(content['summaries'])}")
            print(f"Editor's takes: {len(content.get('editors_takes', []))}")
            print(f"Fixed HTML file: {files['fixed_html']}")
            print("="*50)
            
            return True
        else:
            print("❌ Failed to generate fixed HTML")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_fixed_newsletter()
    if success:
        print("\n🎉 Fixed newsletter test completed successfully!")
        print("🚀 You can now view the fixed newsletter at: output/newsletter_fixed.html")
    else:
        print("\n❌ Fixed newsletter test failed")
    
    sys.exit(0 if success else 1)
