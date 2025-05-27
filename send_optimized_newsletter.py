"""
Generate and send email-optimized newsletter
"""
import os
from utils.content_fetcher import fetch_and_filter_articles
from utils.summarizer import generate_newsletter_content
from utils.email_optimized_processor import save_email_optimized_newsletter
from utils.email_sender import send_newsletter_email
from config import MAX_ARTICLES, OUTPUT_DIR

def main():
    print("🚀 Generating Gmail-optimized AI Newsletter...")
    
    try:
        # Step 1: Fetch and filter articles
        print("📰 Fetching AI articles...")
        articles = fetch_and_filter_articles(MAX_ARTICLES)
        
        if not articles:
            print("❌ No AI articles found.")
            return
        
        print(f"✅ Found {len(articles)} AI articles")
        
        # Step 2: Generate content
        print("🧠 Generating newsletter content...")
        content = generate_newsletter_content(articles, style="rundown")
        
        if not content or not content['summaries']:
            print("❌ Failed to generate newsletter content.")
            return
        
        print(f"✅ Generated content with {len(content['summaries'])} summaries")
        
        # Step 3: Generate email-optimized HTML
        print("✨ Creating Gmail-optimized newsletter...")
        files = save_email_optimized_newsletter(content, OUTPUT_DIR)
        
        # Step 4: Send email
        print("📧 Sending newsletter email...")
        html_path = files['email_optimized_html']
        success = send_newsletter_email(html_path, "🧠 AI News Digest - Gmail Optimized Edition")
        
        if success:
            print("🎉 Newsletter sent successfully!")
            print(f"📄 Email-optimized file: {html_path}")
            print("\n✨ This version fixes all Gmail compatibility issues:")
            print("   • Clean formatting without raw Markdown")
            print("   • Proper HTML table structure for email clients")
            print("   • Inline styles for maximum compatibility")
            print("   • Optimized image sizing and layout")
            print("   • Consistent typography and spacing")
            print("   • Beautiful responsive design")
        else:
            print("❌ Failed to send newsletter")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
