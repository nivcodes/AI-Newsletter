"""
Improved HTML processor with fixed structure and modern layout
Addresses all structural issues and creates a clean, organized newsletter
"""
import os
import logging
from datetime import datetime
from config import OUTPUT_DIR, CATEGORIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImprovedHTMLProcessor:
    """Generate clean, structured HTML newsletter with modern layout"""
    
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or OUTPUT_DIR
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
    
    def get_modern_css_styles(self):
        """Return modern CSS styles with improved structure"""
        return """
        /* CSS Custom Properties for consistent theming */
        :root {
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-gradient: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            --accent-color: #667eea;
            --text-primary: #1a202c;
            --text-secondary: #4a5568;
            --text-muted: #718096;
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --border-color: #e2e8f0;
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.06);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.08);
            --shadow-lg: 0 8px 25px rgba(0, 0, 0, 0.12);
            --border-radius: 12px;
            --spacing-xs: 8px;
            --spacing-sm: 16px;
            --spacing-md: 24px;
            --spacing-lg: 32px;
            --spacing-xl: 48px;
        }
        
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background-color: var(--bg-secondary);
            margin: 0;
            padding: var(--spacing-md);
        }
        
        /* Main container */
        .newsletter-container {
            max-width: 800px;
            margin: 0 auto;
            background-color: var(--bg-primary);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-lg);
            overflow: hidden;
        }
        
        /* Header section */
        .newsletter-header {
            background: var(--primary-gradient);
            color: white;
            padding: var(--spacing-xl) var(--spacing-lg);
            text-align: center;
            position: relative;
        }
        
        .newsletter-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="dots" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23dots)"/></svg>');
            pointer-events: none;
        }
        
        .newsletter-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: var(--spacing-sm);
            position: relative;
            z-index: 1;
        }
        
        .newsletter-subtitle {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 400;
            position: relative;
            z-index: 1;
        }
        
        /* Introduction section */
        .newsletter-intro {
            padding: var(--spacing-lg);
            background: var(--secondary-gradient);
            border-bottom: 1px solid var(--border-color);
        }
        
        .intro-text {
            font-size: 1.1rem;
            line-height: 1.7;
            color: var(--text-secondary);
        }
        
        /* Newsletter sections */
        .newsletter-section {
            margin-bottom: var(--spacing-md);
        }
        
        .section-header {
            background: var(--secondary-gradient);
            padding: var(--spacing-md) var(--spacing-lg);
            border-left: 4px solid var(--accent-color);
            margin: 0;
        }
        
        .section-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 0;
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        /* Articles container */
        .articles-container {
            padding: var(--spacing-lg);
            display: grid;
            gap: var(--spacing-md);
        }
        
        /* Article cards */
        .article-card {
            background: var(--bg-primary);
            border-radius: var(--border-radius);
            box-shadow: var(--shadow-md);
            overflow: hidden;
            transition: all 0.3s ease;
            border: 1px solid var(--border-color);
        }
        
        .article-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }
        
        .article-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid var(--border-color);
        }
        
        .article-content {
            padding: var(--spacing-md);
        }
        
        .article-category {
            display: inline-block;
            background: var(--primary-gradient);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: var(--spacing-sm);
        }
        
        .article-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: var(--spacing-sm);
            line-height: 1.3;
        }
        
        .article-summary {
            color: var(--text-secondary);
            line-height: 1.6;
            margin-bottom: var(--spacing-md);
        }
        
        .article-link {
            display: inline-flex;
            align-items: center;
            gap: var(--spacing-xs);
            background: var(--primary-gradient);
            color: white;
            text-decoration: none;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.2s ease;
            font-size: 0.9rem;
        }
        
        .article-link:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            color: white;
            text-decoration: none;
        }
        
        /* Editor's Take section */
        .editors-take-section {
            background: linear-gradient(135deg, #1a202c, #2d3748);
            color: white;
            padding: var(--spacing-lg);
            margin: var(--spacing-lg) 0;
        }
        
        .editors-take-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: var(--spacing-md);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }
        
        .editors-take-grid {
            display: grid;
            gap: var(--spacing-md);
        }
        
        .editors-take-item {
            background: rgba(255, 255, 255, 0.1);
            padding: var(--spacing-md);
            border-radius: var(--border-radius);
            border-left: 4px solid #f6ad55;
            backdrop-filter: blur(10px);
        }
        
        .editors-take-article-title {
            font-weight: 600;
            margin-bottom: var(--spacing-sm);
            color: #f7fafc;
            font-size: 1.1rem;
        }
        
        .editors-take-text {
            line-height: 1.6;
            color: #e2e8f0;
        }
        
        /* Footer */
        .newsletter-footer {
            background: #2d3748;
            color: #a0aec0;
            padding: var(--spacing-lg);
            text-align: center;
        }
        
        .footer-text {
            margin-bottom: var(--spacing-md);
            line-height: 1.6;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: var(--spacing-md);
            flex-wrap: wrap;
        }
        
        .footer-link {
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.2s ease;
        }
        
        .footer-link:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            body {
                padding: var(--spacing-sm);
            }
            
            .newsletter-container {
                border-radius: 0;
            }
            
            .newsletter-header {
                padding: var(--spacing-lg) var(--spacing-md);
            }
            
            .newsletter-title {
                font-size: 2rem;
            }
            
            .newsletter-intro,
            .articles-container,
            .section-header,
            .editors-take-section,
            .newsletter-footer {
                padding-left: var(--spacing-md);
                padding-right: var(--spacing-md);
            }
            
            .article-content {
                padding: var(--spacing-md);
            }
            
            .article-title {
                font-size: 1.2rem;
            }
            
            .footer-links {
                flex-direction: column;
                gap: var(--spacing-sm);
            }
        }
        
        /* Print styles */
        @media print {
            body {
                background: white;
                padding: 0;
            }
            
            .newsletter-container {
                box-shadow: none;
                border: 1px solid #ccc;
            }
            
            .article-card {
                break-inside: avoid;
                box-shadow: none;
                border: 1px solid var(--border-color);
            }
            
            .article-link {
                background: none;
                color: var(--accent-color);
                border: 1px solid var(--accent-color);
            }
        }
        """
    
    def categorize_articles_by_content(self, articles, summaries):
        """Organize articles and summaries by category with proper structure"""
        categorized = {
            'research': [],
            'tools': [],
            'industry': [],
            'use-case': [],
            'misc': []
        }
        
        for i, article in enumerate(articles):
            category = article.get('category', 'misc')
            if i < len(summaries) and summaries[i]:
                # Clean up summary text
                summary = summaries[i]
                if isinstance(summary, str):
                    # Remove markdown formatting
                    summary = summary.replace('**', '').replace('*', '')
                    # Get first few sentences
                    sentences = summary.split('. ')
                    clean_summary = '. '.join(sentences[:2])
                    if len(clean_summary) > 250:
                        clean_summary = clean_summary[:250] + "..."
                else:
                    clean_summary = "AI-powered summary available in full article."
                
                article_data = {
                    'title': article.get('title', 'Untitled Article'),
                    'url': article.get('url', '#'),
                    'image_url': article.get('image_url', ''),
                    'summary': clean_summary,
                    'popularity_score': article.get('popularity_score', 0),
                    'category': category
                }
                categorized[category].append(article_data)
        
        # Sort articles within each category by popularity score
        for category in categorized:
            categorized[category].sort(key=lambda x: x.get('popularity_score', 0), reverse=True)
        
        return categorized
    
    def build_article_card(self, article):
        """Build HTML for a single article card with clean structure"""
        # Build image HTML if available
        image_html = ""
        if article.get('image_url'):
            image_html = f'''
            <img src="{article['image_url']}" 
                 alt="{article['title']}" 
                 class="article-image" 
                 loading="lazy" />
            '''
        
        # Get category configuration
        category = article.get('category', 'misc')
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        return f'''
        <article class="article-card">
            {image_html}
            <div class="article-content">
                <span class="article-category">{category_config['title']}</span>
                <h3 class="article-title">{article['title']}</h3>
                <div class="article-summary">{article['summary']}</div>
                <a href="{article['url']}" class="article-link" target="_blank" rel="noopener">
                    👉 Read Article
                </a>
            </div>
        </article>
        '''
    
    def build_section_html(self, category, articles):
        """Build HTML for a complete section with proper structure"""
        if not articles:
            return ""
        
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        # Build all article cards for this section
        articles_html = ""
        for article in articles:
            articles_html += self.build_article_card(article)
        
        return f'''
        <section class="newsletter-section">
            <div class="section-header">
                <h2 class="section-title">{category_config['emoji']} {category_config['title']}</h2>
            </div>
            <div class="articles-container">
                {articles_html}
            </div>
        </section>
        '''
    
    def build_editors_takes_html(self, editors_takes):
        """Build HTML for editor's takes section with improved structure"""
        if not editors_takes:
            return ""
        
        takes_html = ""
        for take in editors_takes:
            takes_html += f'''
            <div class="editors-take-item">
                <div class="editors-take-article-title">{take.get('title', 'Editorial Commentary')}</div>
                <div class="editors-take-text">{take.get('take', '')}</div>
            </div>
            '''
        
        return f'''
        <section class="editors-take-section">
            <h2 class="editors-take-title">✍️ Editor's Take</h2>
            <div class="editors-take-grid">
                {takes_html}
            </div>
        </section>
        '''
    
    def generate_improved_html(self, content):
        """Generate improved HTML newsletter with fixed structure"""
        logger.info("🎨 Generating improved HTML newsletter with fixed structure...")
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Get articles and summaries
        articles = content.get('articles', [])
        summaries = content.get('summaries', [])
        
        # Categorize content properly
        categorized = self.categorize_articles_by_content(articles, summaries)
        
        # Build content sections
        content_sections = ""
        section_order = ['research', 'tools', 'industry', 'use-case', 'misc']
        
        for category in section_order:
            if categorized.get(category):
                content_sections += self.build_section_html(category, categorized[category])
        
        # Build complete HTML document
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>🧠 AI Daily Digest – {current_date}</title>
    <style>{self.get_modern_css_styles()}</style>
</head>
<body>
    <div class="newsletter-container">
        <!-- Header -->
        <header class="newsletter-header">
            <h1 class="newsletter-title">🧠 AI Daily Digest</h1>
            <p class="newsletter-subtitle">{current_date} • Curated Intelligence for Developers & Founders</p>
        </header>
        
        <!-- Introduction -->
        <section class="newsletter-intro">
            <div class="intro-text">
                {content.get('intro', 'Welcome to your curated AI newsletter! Today we bring you the latest developments in artificial intelligence, from breakthrough research to practical tools and industry insights.')}
            </div>
        </section>
        
        <!-- Content Sections -->
        {content_sections}
        
        <!-- Editor's Take Section -->
        {self.build_editors_takes_html(content.get('editors_takes', []))}
        
        <!-- Footer -->
        <footer class="newsletter-footer">
            <div class="footer-text">
                Thanks for reading AI Daily Digest! Forward this to a friend who'd love staying ahead in AI.
            </div>
            <div class="footer-links">
                <a href="#" class="footer-link">Archive</a>
                <a href="#" class="footer-link">Subscribe</a>
                <a href="#" class="footer-link">Feedback</a>
                <a href="#" class="footer-link">Unsubscribe</a>
            </div>
        </footer>
    </div>
</body>
</html>'''
        
        # Save to file
        output_path = os.path.join(self.output_dir, "newsletter_improved.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Improved HTML newsletter saved to: {output_path}")
        return output_path
    
    def save_improved_formats(self, content):
        """Save newsletter in improved format"""
        logger.info("💾 Saving improved newsletter...")
        
        saved_files = {}
        
        try:
            # Improved HTML
            saved_files['improved_html'] = self.generate_improved_html(content)
            
            logger.info(f"✅ Saved improved format successfully")
            
        except Exception as e:
            logger.error(f"Error saving improved format: {e}")
            import traceback
            logger.error(traceback.format_exc())
        
        return saved_files


# Main function
def save_improved_newsletter_files(content, output_dir=None):
    """Save improved newsletter files with fixed structure"""
    processor = ImprovedHTMLProcessor(output_dir)
    return processor.save_improved_formats(content)
