"""
Image fetching utilities for newsletter visual enhancement
"""
import requests
from PIL import Image
import io
import logging
import os
from urllib.parse import urlparse, urljoin
import re
from bs4 import BeautifulSoup
import time

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageFetcher:
    """Fetch and process images for newsletter articles"""
    
    def __init__(self, cache_dir="output/images"):
        self.cache_dir = cache_dir
        self.ensure_cache_dir()
        
        # Default fallback images by category
        self.fallback_images = {
            'research': 'https://via.placeholder.com/600x300/4285f4/ffffff?text=🧠+Research',
            'tools': 'https://via.placeholder.com/600x300/34a853/ffffff?text=⚙️+Tools',
            'industry': 'https://via.placeholder.com/600x300/ea4335/ffffff?text=📢+Industry',
            'use-case': 'https://via.placeholder.com/600x300/fbbc04/ffffff?text=🎯+Use+Cases',
            'misc': 'https://via.placeholder.com/600x300/9aa0a6/ffffff?text=🧵+Quick+Hits'
        }
    
    def ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_safe_filename(self, url, title=""):
        """Generate safe filename from URL and title"""
        # Use title if available, otherwise use URL path
        if title:
            base_name = re.sub(r'[^\w\s-]', '', title.strip())
            base_name = re.sub(r'[-\s]+', '-', base_name)[:50]
        else:
            parsed = urlparse(url)
            base_name = os.path.basename(parsed.path) or "image"
        
        # Add timestamp to avoid conflicts
        timestamp = str(int(time.time()))
        return f"{base_name}_{timestamp}.jpg"
    
    def is_logo_or_icon(self, image_url, image_size=None):
        """Check if an image is likely a logo or icon"""
        url_lower = image_url.lower()
        
        # Common logo/icon indicators in URL
        logo_indicators = [
            'logo', 'icon', 'favicon', 'brand', 'header', 'nav',
            'avatar', 'profile', 'thumb', 'badge', 'button'
        ]
        
        # Check URL for logo indicators
        if any(indicator in url_lower for indicator in logo_indicators):
            return True
        
        # Check file path for logo directories
        logo_paths = ['/img/logo', '/images/logo', '/assets/logo', '/static/logo']
        if any(path in url_lower for path in logo_paths):
            return True
        
        # Check for very small images (likely icons)
        if image_size:
            width, height = image_size
            if width < 200 or height < 150:
                return True
        
        # Check for square images (often logos)
        if image_size:
            width, height = image_size
            if width == height and width < 400:
                return True
        
        return False
    
    def score_image_quality(self, image_url, image_size=None, context=""):
        """Score image quality for article relevance"""
        score = 0
        url_lower = image_url.lower()
        
        # Negative scoring for logos/icons
        if self.is_logo_or_icon(image_url, image_size):
            score -= 50
        
        # Positive scoring for article-relevant images
        article_indicators = [
            'article', 'post', 'content', 'story', 'news',
            'featured', 'hero', 'main', 'cover'
        ]
        
        if any(indicator in url_lower for indicator in article_indicators):
            score += 20
        
        # Size scoring
        if image_size:
            width, height = image_size
            # Prefer landscape images for articles
            if width > height and width >= 400:
                score += 15
            # Bonus for good article image sizes
            if 600 <= width <= 1200 and 300 <= height <= 800:
                score += 10
        
        # Context relevance (if we have article title/content)
        if context:
            context_lower = context.lower()
            # Look for AI/tech related terms in image URL
            tech_terms = ['ai', 'tech', 'robot', 'computer', 'data', 'digital']
            if any(term in url_lower for term in tech_terms):
                score += 10
        
        return score
    
    def extract_og_image(self, url, title=""):
        """Extract Open Graph image from article URL with quality scoring"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            candidate_images = []
            
            # Try Open Graph image first
            og_image = soup.find('meta', property='og:image')
            if og_image and og_image.get('content'):
                image_url = og_image['content']
                # Make absolute URL if relative
                if image_url.startswith('/'):
                    image_url = urljoin(url, image_url)
                
                # Score this image
                score = self.score_image_quality(image_url, context=title)
                candidate_images.append((image_url, score, 'og:image'))
            
            # Try Twitter card image
            twitter_image = soup.find('meta', attrs={'name': 'twitter:image'})
            if twitter_image and twitter_image.get('content'):
                image_url = twitter_image['content']
                if image_url.startswith('/'):
                    image_url = urljoin(url, image_url)
                
                score = self.score_image_quality(image_url, context=title)
                candidate_images.append((image_url, score, 'twitter:image'))
            
            # Try to find content images with better scoring
            images = soup.find_all('img')
            for img in images:
                src = img.get('src')
                if src and not src.startswith('data:'):
                    if src.startswith('/'):
                        src = urljoin(url, src)
                    
                    # Get image dimensions if available
                    width = img.get('width')
                    height = img.get('height')
                    image_size = None
                    if width and height:
                        try:
                            image_size = (int(width), int(height))
                        except ValueError:
                            pass
                    
                    # Score this image
                    score = self.score_image_quality(src, image_size, title)
                    
                    # Only consider images with positive scores
                    if score > 0:
                        candidate_images.append((src, score, 'content'))
            
            # Return the highest scoring image
            if candidate_images:
                best_image = max(candidate_images, key=lambda x: x[1])
                logger.info(f"Selected image with score {best_image[1]} from {best_image[2]}")
                return best_image[0]
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting OG image from {url}: {e}")
            return None
    
    def extract_arxiv_image(self, url):
        """Extract first figure from arXiv paper"""
        try:
            # For arXiv papers, we can try to get the PDF and extract first figure
            # This is complex, so for now we'll use a placeholder
            # In a full implementation, you'd use PyMuPDF or similar to extract images from PDF
            
            if 'arxiv.org' in url:
                # Extract arXiv ID from URL
                arxiv_match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', url)
                if arxiv_match:
                    arxiv_id = arxiv_match.group(1)
                    # Return a placeholder for now - in production you'd extract from PDF
                    return f"https://via.placeholder.com/600x400/4285f4/ffffff?text=arXiv+{arxiv_id}"
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting arXiv image from {url}: {e}")
            return None
    
    def search_duckduckgo_images(self, query, safe_search=True):
        """Search for images using DuckDuckGo (fallback method)"""
        try:
            # This is a simplified version - in production you'd use proper DDG API
            # For now, return a generated placeholder based on query
            safe_query = re.sub(r'[^\w\s]', '', query)[:30]
            placeholder_url = f"https://via.placeholder.com/600x300/9aa0a6/ffffff?text={safe_query.replace(' ', '+')}"
            return placeholder_url
            
        except Exception as e:
            logger.error(f"Error searching images for '{query}': {e}")
            return None
    
    def download_and_process_image(self, image_url, filename, max_width=600):
        """Download and process image for newsletter use"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(image_url, headers=headers, timeout=15)
            response.raise_for_status()
            
            # Open image with PIL
            image = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large
            if image.width > max_width:
                ratio = max_width / image.width
                new_height = int(image.height * ratio)
                image = image.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save processed image
            filepath = os.path.join(self.cache_dir, filename)
            image.save(filepath, 'JPEG', quality=85, optimize=True)
            
            logger.info(f"✅ Downloaded and processed image: {filename}")
            return filepath
            
        except Exception as e:
            logger.error(f"Error downloading/processing image {image_url}: {e}")
            return None
    
    def get_article_image(self, article):
        """Get the best available image for an article"""
        title = article.get('title', '')
        url = article.get('url', '')
        category = article.get('category', 'misc')
        
        logger.info(f"🖼️ Fetching image for: {title}")
        
        # Try existing image_url from article extraction
        if article.get('image_url'):
            image_url = article['image_url']
            filename = self.get_safe_filename(image_url, title)
            filepath = self.download_and_process_image(image_url, filename)
            if filepath:
                return {
                    'local_path': filepath,
                    'url': image_url,
                    'source': 'article_extraction'
                }
        
        # Try Open Graph image extraction with title context
        og_image_url = self.extract_og_image(url, title)
        if og_image_url:
            filename = self.get_safe_filename(og_image_url, title)
            filepath = self.download_and_process_image(og_image_url, filename)
            if filepath:
                return {
                    'local_path': filepath,
                    'url': og_image_url,
                    'source': 'open_graph'
                }
        
        # Try arXiv-specific extraction
        if 'arxiv.org' in url:
            arxiv_image_url = self.extract_arxiv_image(url)
            if arxiv_image_url:
                filename = self.get_safe_filename(arxiv_image_url, title)
                filepath = self.download_and_process_image(arxiv_image_url, filename)
                if filepath:
                    return {
                        'local_path': filepath,
                        'url': arxiv_image_url,
                        'source': 'arxiv'
                    }
        
        # Try image search as fallback
        search_query = f"{title} AI artificial intelligence"
        search_image_url = self.search_duckduckgo_images(search_query)
        if search_image_url:
            filename = self.get_safe_filename(search_image_url, title)
            filepath = self.download_and_process_image(search_image_url, filename)
            if filepath:
                return {
                    'local_path': filepath,
                    'url': search_image_url,
                    'source': 'search'
                }
        
        # Use category fallback
        fallback_url = self.fallback_images.get(category, self.fallback_images['misc'])
        filename = f"fallback_{category}_{int(time.time())}.jpg"
        filepath = self.download_and_process_image(fallback_url, filename)
        
        if filepath:
            return {
                'local_path': filepath,
                'url': fallback_url,
                'source': 'fallback'
            }
        
        logger.warning(f"❌ Could not fetch any image for: {title}")
        return None
    
    def process_articles_images(self, articles):
        """Process images for a list of articles"""
        logger.info(f"🎨 Processing images for {len(articles)} articles...")
        
        for article in articles:
            try:
                image_info = self.get_article_image(article)
                if image_info:
                    article['image_info'] = image_info
                    # Keep backward compatibility
                    article['image_url'] = image_info['url']
                else:
                    article['image_info'] = None
                
                # Small delay to be respectful
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error processing image for {article.get('title', 'Unknown')}: {e}")
                article['image_info'] = None
        
        logger.info("✅ Completed image processing")
        return articles
    
    def cleanup_old_images(self, days_old=7):
        """Clean up old cached images"""
        try:
            import time
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            for filename in os.listdir(self.cache_dir):
                filepath = os.path.join(self.cache_dir, filename)
                if os.path.isfile(filepath):
                    file_time = os.path.getmtime(filepath)
                    if file_time < cutoff_time:
                        os.remove(filepath)
                        logger.info(f"🗑️ Cleaned up old image: {filename}")
                        
        except Exception as e:
            logger.error(f"Error cleaning up old images: {e}")


# Main function for easy use
def fetch_article_images(articles):
    """Fetch images for a list of articles"""
    fetcher = ImageFetcher()
    return fetcher.process_articles_images(articles)
