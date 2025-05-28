"""
Simple test script for AI Newsletter Generator
"""
import sys
from datetime import datetime

def test_newsletter():
    """Test the newsletter generation"""
    print("🚀 Testing AI Newsletter Generator")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Import the main components
        from utils.enhanced_content_fetcher import fetch_and_filter_articles
        from utils.enhanced_summarizer import generate_newsletter_content
        from utils.fixed_html_processor import save_fixed_newsletter_files
        
        print("✅ All imports successful")
        
        # Test with minimal articles
        print("📰 Fetching 2 articles for testing...")
        articles = fetch_and_filter_articles(max_articles=2)
        
        if not articles:
            print("❌ No articles fetched")
            return False
        
        print(f"✅ Found {len(articles)} articles")
        
        # Generate content
        print("🧠 Generating newsletter content...")
        content = generate_newsletter_content(articles, style="editorial")
        
        if not content or not content['summaries']:
            print("❌ Failed to generate content")
            return False
        
        print(f"✅ Generated {len(content['summaries'])} summaries")
        
        # Generate HTML
        print("🎨 Generating HTML...")
        files = save_fixed_newsletter_files(content)
        
        if files and files.get('fixed_html'):
            print(f"✅ HTML generated: {files['fixed_html']}")
            print("🎉 Test completed successfully!")
            return True
        else:
            print("❌ Failed to generate HTML")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_newsletter()
    sys.exit(0 if success else 1)
