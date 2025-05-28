"""
Test script for Enhanced AI Newsletter Generator
Demonstrates the new features and capabilities
"""
import sys
import logging
from datetime import datetime

# Import enhanced components
from utils.enhanced_content_fetcher import EnhancedContentFetcher
from utils.enhanced_summarizer import EnhancedSummarizer
from utils.premium_html_processor import PremiumHTMLProcessor
from utils.image_fetcher import ImageFetcher

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def test_content_fetching():
    """Test the enhanced content fetching capabilities"""
    print("\n" + "="*60)
    print("🧪 TESTING ENHANCED CONTENT FETCHING")
    print("="*60)
    
    try:
        fetcher = EnhancedContentFetcher()
        
        # Test with a small number for quick testing
        print("📰 Fetching 3 articles for testing...")
        articles = fetcher.fetch_and_process_all_articles(max_articles=3)
        
        if articles:
            print(f"✅ Successfully fetched {len(articles)} articles")
            
            # Show article details
            for i, article in enumerate(articles, 1):
                print(f"\n📄 Article {i}:")
                print(f"  Title: {article.get('title', 'N/A')[:80]}...")
                print(f"  Category: {article.get('category', 'N/A')}")
                print(f"  Score: {article.get('popularity_score', 0)}")
                print(f"  Source: {article.get('source_feed', 'N/A')}")
                print(f"  Has Image: {'Yes' if article.get('image_url') else 'No'}")
            
            return articles
        else:
            print("❌ No articles fetched")
            return []
            
    except Exception as e:
        print(f"❌ Content fetching test failed: {e}")
        return []


def test_summarization(articles):
    """Test the enhanced summarization capabilities"""
    print("\n" + "="*60)
    print("🧪 TESTING ENHANCED SUMMARIZATION")
    print("="*60)
    
    if not articles:
        print("⏭️ Skipping - no articles to summarize")
        return None
    
    try:
        summarizer = EnhancedSummarizer()
        
        print("🧠 Generating editorial summaries...")
        content = summarizer.generate_newsletter_content(articles[:2], style="editorial")  # Test with 2 articles
        
        if content and content.get('summaries'):
            print(f"✅ Generated {len(content['summaries'])} summaries")
            
            # Show generation info
            gen_info = content.get('generation_info', {})
            print(f"🤖 LLM used: {gen_info.get('llm_used', 'unknown')}")
            print(f"📊 Categories: {', '.join(gen_info.get('categories', []))}")
            
            if content.get('editors_takes'):
                print(f"✍️ Editor's Takes: {len(content['editors_takes'])}")
            
            # Show first summary preview
            if content['summaries']:
                print(f"\n📝 First summary preview:")
                preview = content['summaries'][0][:200] + "..." if len(content['summaries'][0]) > 200 else content['summaries'][0]
                print(f"  {preview}")
            
            return content
        else:
            print("❌ No summaries generated")
            return None
            
    except Exception as e:
        print(f"❌ Summarization test failed: {e}")
        return None


def test_image_processing(articles):
    """Test the image fetching capabilities"""
    print("\n" + "="*60)
    print("🧪 TESTING IMAGE PROCESSING")
    print("="*60)
    
    if not articles:
        print("⏭️ Skipping - no articles to process")
        return articles
    
    try:
        fetcher = ImageFetcher()
        
        print("🖼️ Processing images for articles...")
        # Test with just the first article to avoid too many requests
        test_articles = articles[:1]
        processed_articles = fetcher.process_articles_images(test_articles)
        
        if processed_articles:
            print(f"✅ Processed images for {len(processed_articles)} articles")
            
            for article in processed_articles:
                image_info = article.get('image_info')
                if image_info:
                    print(f"  📸 {article.get('title', 'Unknown')[:50]}...")
                    print(f"    Source: {image_info.get('source', 'unknown')}")
                    print(f"    URL: {image_info.get('url', 'N/A')[:60]}...")
                else:
                    print(f"  ❌ No image for: {article.get('title', 'Unknown')[:50]}...")
        
        return processed_articles
        
    except Exception as e:
        print(f"❌ Image processing test failed: {e}")
        return articles


def test_html_generation(content):
    """Test the premium HTML generation"""
    print("\n" + "="*60)
    print("🧪 TESTING PREMIUM HTML GENERATION")
    print("="*60)
    
    if not content:
        print("⏭️ Skipping - no content to process")
        return
    
    try:
        processor = PremiumHTMLProcessor()
        
        print("🎨 Generating premium HTML newsletter...")
        files = processor.save_all_formats(content)
        
        if files:
            print(f"✅ Generated {len(files)} file formats:")
            for file_type, path in files.items():
                print(f"  📄 {file_type}: {path}")
        else:
            print("❌ No files generated")
            
    except Exception as e:
        print(f"❌ HTML generation test failed: {e}")


def test_configuration():
    """Test configuration and environment setup"""
    print("\n" + "="*60)
    print("🧪 TESTING CONFIGURATION")
    print("="*60)
    
    try:
        from config import (
            RSS_FEEDS, CATEGORIES, AI_KEYWORDS, HIGH_IMPACT_KEYWORDS,
            OPENAI_API_KEY, ANTHROPIC_API_KEY, USE_EXTERNAL_LLM
        )
        
        print("📋 Configuration loaded successfully:")
        print(f"  RSS Feed categories: {len(RSS_FEEDS)}")
        print(f"  Total RSS feeds: {sum(len(feeds) for feeds in RSS_FEEDS.values())}")
        print(f"  Article categories: {len(CATEGORIES)}")
        print(f"  AI keywords: {len(AI_KEYWORDS)}")
        print(f"  High-impact keywords: {len(HIGH_IMPACT_KEYWORDS)}")
        
        # Check LLM configuration
        print(f"\n🤖 LLM Configuration:")
        print(f"  Use external LLM: {USE_EXTERNAL_LLM}")
        print(f"  OpenAI API configured: {'Yes' if OPENAI_API_KEY else 'No'}")
        print(f"  Anthropic API configured: {'Yes' if ANTHROPIC_API_KEY else 'No'}")
        
        print("✅ Configuration test passed")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")


def run_full_test():
    """Run comprehensive test of all enhanced features"""
    print("🚀 ENHANCED AI NEWSLETTER GENERATOR - COMPREHENSIVE TEST")
    print(f"⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test 1: Configuration
    test_configuration()
    
    # Test 2: Content Fetching
    articles = test_content_fetching()
    
    # Test 3: Image Processing
    if articles:
        articles = test_image_processing(articles)
    
    # Test 4: Summarization
    content = test_summarization(articles)
    
    # Test 5: HTML Generation
    if content:
        test_html_generation(content)
    
    # Final Summary
    print("\n" + "="*60)
    print("🎉 COMPREHENSIVE TEST COMPLETED")
    print("="*60)
    print(f"⏰ Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if content and content.get('summaries'):
        print("✅ All major components tested successfully!")
        print("\n🚀 Ready to run: python enhanced_newsletter_generator.py --generate-only")
    else:
        print("⚠️ Some tests failed - check configuration and dependencies")
        print("\n🔧 Try: python enhanced_newsletter_generator.py --test-email")


def run_quick_test():
    """Run a quick test of basic functionality"""
    print("🚀 ENHANCED AI NEWSLETTER GENERATOR - QUICK TEST")
    
    try:
        # Quick configuration check
        from config import RSS_FEEDS, CATEGORIES
        print(f"✅ Configuration loaded: {len(RSS_FEEDS)} feed categories, {len(CATEGORIES)} article categories")
        
        # Quick component import test
        from utils.enhanced_content_fetcher import EnhancedContentFetcher
        from utils.enhanced_summarizer import EnhancedSummarizer
        from utils.premium_html_processor import PremiumHTMLProcessor
        print("✅ All enhanced components imported successfully")
        
        print("\n🎉 Quick test passed! System is ready.")
        print("🚀 Run full test with: python test_enhanced_newsletter.py --full")
        print("🚀 Generate newsletter with: python enhanced_newsletter_generator.py --generate-only")
        
    except Exception as e:
        print(f"❌ Quick test failed: {e}")
        print("🔧 Check your dependencies: pip install -r requirements.txt")


def main():
    """Main test function"""
    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        run_full_test()
    else:
        run_quick_test()


if __name__ == "__main__":
    main()
