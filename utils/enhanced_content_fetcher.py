"""
Enhanced content fetching utilities with multiple sources, popularity scoring, and categorization
"""
import feedparser
from newspaper import Article
import requests
import time
import logging
from datetime import datetime, timedelta
from urllib.parse import urlparse
import re
from config import (
    RSS_FEEDS, API_SOURCES, ARTICLES_PER_FEED, DELAY_BETWEEN_REQUESTS, 
    AI_KEYWORDS, HIGH_IMPACT_KEYWORDS, CATEGORIES, MIN_ARTICLE_LENGTH,
    MAX_ARTICLE_AGE_HOURS, MAX_ARTICLES_PER_CATEGORY
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ArticleScorer:
    """Calculate popularity scores for articles"""
    
    @staticmethod
    def calculate_popularity_score(article):
        """Calculate multi-factor popularity score"""
        score = 0
        
        # Engagement signals (when available)
        score += article.get('upvotes', 0) * 0.3
        score += article.get('comments', 0) * 0.2
        score += article.get('shares', 0) * 0.25
        
        # Keyword importance weighting
        text_content = (article.get('title', '') + ' ' + article.get('text', '')).lower()
        
        # High-impact keywords get significant boost
        for keyword in HIGH_IMPACT_KEYWORDS:
            if keyword.lower() in text_content:
                score += 15
        
        # AI keywords get moderate boost
        for keyword in AI_KEYWORDS:
            if keyword.lower() in text_content:
                score += 5
        
        # Recency bonus (24-48 hours)
        if article.get('publish_date'):
            try:
                if isinstance(article['publish_date'], str):
                    # Try to parse string date
                    pub_date = datetime.fromisoformat(article['publish_date'].replace('Z', '+00:00'))
                else:
                    pub_date = article['publish_date']
                
                hours_old = (datetime.now() - pub_date.replace(tzinfo=None)).total_seconds() / 3600
                
                if hours_old <= 24:
                    score += 25
                elif hours_old <= 48:
                    score += 15
                elif hours_old <= 72:
                    score += 5
            except:
                # If date parsing fails, give small penalty
                score -= 5
        
        # Source credibility bonus
        source_domain = urlparse(article.get('url', '')).netloc.lower()
        credible_sources = [
            'arxiv.org', 'openai.com', 'anthropic.com', 'ai.googleblog.com',
            'techcrunch.com', 'venturebeat.com', 'technologyreview.com'
        ]
        
        if any(domain in source_domain for domain in credible_sources):
            score += 10
        
        # Length bonus (longer articles often more substantial)
        text_length = len(article.get('text', ''))
        if text_length > 1000:
            score += 10
        elif text_length > 500:
            score += 5
        
        return max(0, score)  # Ensure non-negative score


class ArticleCategorizer:
    """Categorize articles into research, tools, industry, etc."""
    
    @staticmethod
    def categorize_article(article):
        """Determine article category based on content and source"""
        title = article.get('title', '').lower()
        text = article.get('text', '').lower()
        url = article.get('url', '').lower()
        
        content = f"{title} {text}"
        
        # Score each category
        category_scores = {}
        
        for category, config in CATEGORIES.items():
            score = 0
            
            # Keyword matching
            for keyword in config['keywords']:
                if keyword.lower() in content:
                    score += 10
            
            # Source matching
            for source in config['sources']:
                if source.lower() in url:
                    score += 20
            
            category_scores[category] = score
        
        # Return category with highest score, default to 'misc'
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        else:
            return 'misc'


class EnhancedContentFetcher:
    """Enhanced content fetcher with multiple sources and intelligent processing"""
    
    def __init__(self):
        self.scorer = ArticleScorer()
        self.categorizer = ArticleCategorizer()
    
    def is_ai_related(self, text):
        """Enhanced AI content detection"""
        text_lower = text.lower()
        
        # Must contain at least 2 AI keywords for better precision
        ai_keyword_count = sum(1 for keyword in AI_KEYWORDS if keyword.lower() in text_lower)
        return ai_keyword_count >= 2
    
    def is_recent_article(self, publish_date):
        """Check if article is within acceptable age range"""
        if not publish_date:
            return True  # Include if no date available
        
        try:
            if isinstance(publish_date, str):
                pub_date = datetime.fromisoformat(publish_date.replace('Z', '+00:00'))
            else:
                pub_date = publish_date
            
            hours_old = (datetime.now() - pub_date.replace(tzinfo=None)).total_seconds() / 3600
            return hours_old <= MAX_ARTICLE_AGE_HOURS
        except:
            return True  # Include if date parsing fails
    
    def extract_article_content(self, url):
        """Enhanced article content extraction with better error handling"""
        try:
            article = Article(url)
            article.download()
            article.parse()
            
            # Skip if article is too short
            if len(article.text) < MIN_ARTICLE_LENGTH:
                return None
            
            return {
                'text': article.text,
                'image_url': article.top_image or "",
                'authors': article.authors,
                'publish_date': article.publish_date,
                'meta_description': getattr(article, 'meta_description', ''),
                'meta_keywords': getattr(article, 'meta_keywords', [])
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to extract content from {url}: {e}")
            return None
    
    def fetch_rss_articles(self):
        """Fetch articles from categorized RSS feeds"""
        logger.info("🔍 Fetching articles from RSS feeds...")
        articles = []
        
        for category, feeds in RSS_FEEDS.items():
            logger.info(f"📡 Fetching {category} articles...")
            
            for feed_url in feeds:
                try:
                    logger.info(f"  Processing: {feed_url}")
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:ARTICLES_PER_FEED]:
                        # Extract basic info
                        article_data = {
                            'title': entry.title,
                            'url': entry.link,
                            'source_category': category,
                            'source_feed': feed_url,
                            'publish_date': getattr(entry, 'published_parsed', None)
                        }
                        
                        # Convert publish_date if available
                        if article_data['publish_date']:
                            article_data['publish_date'] = datetime(*article_data['publish_date'][:6])
                        
                        articles.append(article_data)
                        
                except Exception as e:
                    logger.error(f"Failed to fetch from {feed_url}: {e}")
                    continue
                
                # Rate limiting
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        logger.info(f"✅ Fetched {len(articles)} articles from RSS feeds")
        return articles
    
    def fetch_hackernews_articles(self):
        """Fetch AI-related articles from Hacker News"""
        logger.info("🔥 Fetching from Hacker News...")
        articles = []
        
        try:
            # Get top stories
            response = requests.get(f"{API_SOURCES['hackernews']}/topstories.json")
            story_ids = response.json()[:50]  # Top 50 stories
            
            for story_id in story_ids[:20]:  # Process first 20
                try:
                    story_response = requests.get(f"{API_SOURCES['hackernews']}/item/{story_id}.json")
                    story = story_response.json()
                    
                    if story and story.get('title') and story.get('url'):
                        # Check if AI-related
                        if self.is_ai_related(story['title']):
                            article_data = {
                                'title': story['title'],
                                'url': story['url'],
                                'source_category': 'misc',
                                'source_feed': 'hackernews',
                                'upvotes': story.get('score', 0),
                                'comments': story.get('descendants', 0),
                                'publish_date': datetime.fromtimestamp(story.get('time', 0))
                            }
                            articles.append(article_data)
                    
                    time.sleep(0.1)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error fetching HN story {story_id}: {e}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error fetching from Hacker News: {e}")
        
        logger.info(f"✅ Fetched {len(articles)} articles from Hacker News")
        return articles
    
    def process_articles(self, raw_articles):
        """Process raw articles: extract content, score, and categorize"""
        logger.info("🔄 Processing articles...")
        processed_articles = []
        
        for article_data in raw_articles:
            try:
                logger.info(f"🔗 Processing: {article_data['title']}")
                
                # Skip if not recent enough
                if not self.is_recent_article(article_data.get('publish_date')):
                    logger.info("⏭️  Skipping - too old")
                    continue
                
                # Extract full content
                content = self.extract_article_content(article_data['url'])
                if not content:
                    continue
                
                # Merge data
                full_article = {**article_data, **content}
                
                # Check if AI-related (enhanced check)
                full_text = f"{full_article['title']} {full_article['text']}"
                if not self.is_ai_related(full_text):
                    logger.info("⏭️  Skipping - not AI-related")
                    continue
                
                # Calculate popularity score
                full_article['popularity_score'] = self.scorer.calculate_popularity_score(full_article)
                
                # Categorize article
                full_article['category'] = self.categorizer.categorize_article(full_article)
                
                processed_articles.append(full_article)
                logger.info(f"✅ Added article (score: {full_article['popularity_score']}, category: {full_article['category']})")
                
                # Rate limiting
                time.sleep(DELAY_BETWEEN_REQUESTS)
                
            except Exception as e:
                logger.error(f"Error processing article {article_data.get('title', 'Unknown')}: {e}")
                continue
        
        logger.info(f"🎯 Processed {len(processed_articles)} AI-related articles")
        return processed_articles
    
    def curate_top_articles(self, articles):
        """Curate top articles by category and overall score"""
        logger.info("🎨 Curating top articles...")
        
        # Sort by popularity score
        articles.sort(key=lambda x: x['popularity_score'], reverse=True)
        
        # Group by category
        categorized = {}
        for article in articles:
            category = article['category']
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(article)
        
        # Select top articles per category
        curated_articles = []
        for category, category_articles in categorized.items():
            top_articles = category_articles[:MAX_ARTICLES_PER_CATEGORY]
            curated_articles.extend(top_articles)
            logger.info(f"📊 {category}: {len(top_articles)} articles selected")
        
        # Sort final list by score
        curated_articles.sort(key=lambda x: x['popularity_score'], reverse=True)
        
        logger.info(f"🏆 Curated {len(curated_articles)} top articles")
        return curated_articles
    
    def fetch_and_process_all_articles(self, max_articles=None):
        """Main method to fetch, process, and curate articles"""
        logger.info("🚀 Starting enhanced article fetching...")
        
        # Fetch from all sources
        all_articles = []
        
        # RSS feeds
        rss_articles = self.fetch_rss_articles()
        all_articles.extend(rss_articles)
        
        # Hacker News
        hn_articles = self.fetch_hackernews_articles()
        all_articles.extend(hn_articles)
        
        # Process all articles
        processed_articles = self.process_articles(all_articles)
        
        # Curate top articles
        curated_articles = self.curate_top_articles(processed_articles)
        
        # Limit final count if specified
        if max_articles:
            curated_articles = curated_articles[:max_articles]
        
        logger.info(f"🎉 Final selection: {len(curated_articles)} articles")
        return curated_articles


# Main function for backward compatibility
def fetch_and_filter_articles(max_articles=None):
    """Enhanced main function to fetch and filter articles"""
    fetcher = EnhancedContentFetcher()
    return fetcher.fetch_and_process_all_articles(max_articles)
