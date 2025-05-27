"""
Content fetching utilities for RSS feeds and article extraction
"""
import feedparser
from newspaper import Article
import time
import logging
from config import RSS_FEEDS, ARTICLES_PER_FEED, DELAY_BETWEEN_REQUESTS, AI_KEYWORDS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_ai_related(text):
    """Check if text contains AI-related keywords"""
    return any(keyword.lower() in text.lower() for keyword in AI_KEYWORDS)


def fetch_articles_from_rss():
    """Fetch articles from configured RSS feeds"""
    logger.info("🔍 Fetching articles from RSS feeds...")
    articles = []
    
    for feed_url in RSS_FEEDS:
        try:
            logger.info(f"Fetching from: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:ARTICLES_PER_FEED]:
                articles.append((entry.title, entry.link))
                
        except Exception as e:
            logger.error(f"Failed to fetch from {feed_url}: {e}")
            continue
    
    logger.info(f"✅ Fetched {len(articles)} articles total")
    return articles


def extract_article_content(url):
    """Extract full text and image from article URL"""
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        return {
            'text': article.text,
            'image_url': article.top_image or "",
            'authors': article.authors,
            'publish_date': article.publish_date
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to extract content from {url}: {e}")
        return None


def filter_ai_articles(articles, max_articles=3):
    """Filter articles for AI-related content"""
    logger.info("🤖 Filtering for AI-related articles...")
    ai_articles = []
    
    for title, url in articles:
        if len(ai_articles) >= max_articles:
            break
            
        logger.info(f"🔗 Processing: {title}")
        
        # Extract content
        content = extract_article_content(url)
        if not content or not content['text']:
            continue
            
        # Check if AI-related
        full_text = title + " " + content['text']
        if not is_ai_related(full_text):
            logger.info("⏭️  Skipping - not AI-related")
            continue
            
        ai_articles.append({
            'title': title,
            'url': url,
            'text': content['text'],
            'image_url': content['image_url'],
            'authors': content['authors'],
            'publish_date': content['publish_date']
        })
        
        logger.info("✅ Added AI-related article")
        
        # Rate limiting
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    logger.info(f"🎯 Found {len(ai_articles)} AI-related articles")
    return ai_articles


def fetch_and_filter_articles(max_articles=None):
    """Main function to fetch and filter articles"""
    if max_articles is None:
        from config import MAX_ARTICLES
        max_articles = MAX_ARTICLES
        
    # Fetch all articles
    all_articles = fetch_articles_from_rss()
    
    # Filter for AI content
    ai_articles = filter_ai_articles(all_articles, max_articles)
    
    return ai_articles
