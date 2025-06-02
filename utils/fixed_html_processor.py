"""
Fixed HTML processor that builds HTML programmatically to avoid template rendering issues
"""
import os
import logging
from datetime import datetime
from config import OUTPUT_DIR, CATEGORIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FixedHTMLProcessor:
    """Build HTML newsletter programmatically to avoid template rendering issues"""
    
    def __init__(self, output_dir=None):
        self.output_dir = output_dir or OUTPUT_DIR
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
    
    def get_css_styles(self):
        """Return the CSS styles for the newsletter"""
        return """
        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #2c3e50;
            background-color: #f8fafc;
            margin: 0;
            padding: 0;
        }
        
        /* Container */
        .newsletter-container {
            max-width: 720px;
            margin: 0 auto;
            background-color: #ffffff;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
        }
        
        /* Header */
        .newsletter-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .newsletter-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 10px;
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
        
        /* Introduction */
        .newsletter-intro {
            padding: 30px;
            background: linear-gradient(to bottom, #ffffff, #f8fafc);
            border-bottom: 1px solid #e2e8f0;
        }
        
        .intro-text {
            font-size: 1.1rem;
            line-height: 1.7;
            color: #4a5568;
        }
        
        /* Section headers */
        .section-header {
            background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
            padding: 20px 30px;
            border-left: 4px solid #667eea;
            margin: 0;
        }
        
        .section-title {
            font-size: 1.4rem;
            font-weight: 700;
            color: #2d3748;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        /* Article cards */
        .articles-container {
            padding: 0 30px 30px;
        }
        
        .article-card {
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 25px;
            overflow: hidden;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border: 1px solid #e2e8f0;
        }
        
        .article-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }
        
        .article-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid #e2e8f0;
        }
        
        .article-content {
            padding: 25px;
        }
        
        .article-category {
            display: inline-block;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
        }
        
        .article-title {
            font-size: 1.3rem;
            font-weight: 700;
            color: #1a202c;
            margin-bottom: 15px;
            line-height: 1.4;
        }
        
        .article-summary {
            color: #4a5568;
            line-height: 1.6;
            margin-bottom: 15px;
        }
        
        .article-link {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            text-decoration: none;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: 600;
            transition: all 0.2s ease;
            margin-top: 15px;
        }
        
        .article-link:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
            color: white;
            text-decoration: none;
        }
        
        /* Editor's Take section */
        .editors-take-section {
            background: linear-gradient(135deg, #1a202c, #2d3748);
            color: white;
            padding: 30px;
            margin: 30px 0;
        }
        
        .editors-take-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .editors-take-item {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 15px;
            border-left: 4px solid #f6ad55;
        }
        
        .editors-take-article-title {
            font-weight: 600;
            margin-bottom: 10px;
            color: #f7fafc;
        }
        
        .editors-take-text {
            line-height: 1.6;
            color: #e2e8f0;
        }
        
        /* Footer */
        .newsletter-footer {
            background: #2d3748;
            color: #a0aec0;
            padding: 30px;
            text-align: center;
        }
        
        .footer-text {
            margin-bottom: 15px;
            line-height: 1.6;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        
        .footer-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
        }
        
        .footer-link:hover {
            color: #764ba2;
            text-decoration: underline;
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .newsletter-container {
                margin: 0;
                box-shadow: none;
            }
            
            .newsletter-header {
                padding: 30px 20px;
            }
            
            .newsletter-title {
                font-size: 2rem;
            }
            
            .newsletter-intro,
            .articles-container,
            .section-header,
            .editors-take-section,
            .newsletter-footer {
                padding-left: 20px;
                padding-right: 20px;
            }
            
            .article-content {
                padding: 20px;
            }
            
            .article-title {
                font-size: 1.2rem;
            }
            
            .footer-links {
                flex-direction: column;
                gap: 10px;
            }
        }
        """
    
    def categorize_articles_by_content(self, articles, summaries):
        """Organize articles and summaries by category"""
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
                article_data = {
                    'title': article.get('title', ''),
                    'url': article.get('url', ''),
                    'image_url': article.get('image_url', ''),
                    'summary': summaries[i],
                    'popularity_score': article.get('popularity_score', 0)
                }
                categorized[category].append(article_data)
        
        return categorized
    
    def build_article_card(self, article, category_name):
        """Build HTML for a single article card"""
        category_config = CATEGORIES.get(category_name, CATEGORIES['misc'])
        
        # Build image HTML if available
        image_html = ""
        if article.get('image_url'):
            image_html = f'<img src="{article["image_url"]}" alt="{article["title"]}" class="article-image" />'
        
        # Clean up the summary (remove markdown formatting for display)
        summary = article.get('summary', '').replace('**', '').replace('*', '')
        
        # Extract just the text content, not the full markdown
        summary_lines = summary.split('\n')
        clean_summary = []
        for line in summary_lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('['):
                clean_summary.append(line)
        
        summary_text = ' '.join(clean_summary[:3])  # First 3 meaningful lines
        if len(summary_text) > 300:
            summary_text = summary_text[:300] + "..."
        
        return f"""
            <article class="article-card">
                {image_html}
                <div class="article-content">
                    <span class="article-category">{category_config['title']}</span>
                    <h3 class="article-title">{article['title']}</h3>
                    <div class="article-summary">{summary_text}</div>
                    <a href="{article['url']}" class="article-link">👉 Read more</a>
                </div>
            </article>
        """
    
    def build_section_html(self, category, articles):
        """Build HTML for a complete section"""
        if not articles:
            return ""
        
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        # Build section header
        section_html = f"""
        <div class="section-header">
            <h2 class="section-title">{category_config['emoji']} {category_config['title']}</h2>
        </div>
        <div class="articles-container">
        """
        
        # Add all articles for this section
        for article in articles:
            section_html += self.build_article_card(article, category)
        
        section_html += "</div>"
        
        return section_html
    
    def build_editors_takes_html(self, editors_takes):
        """Build HTML for editor's takes section"""
        if not editors_takes:
            return ""
        
        takes_html = ""
        for take in editors_takes:
            takes_html += f"""
            <div class="editors-take-item">
                <div class="editors-take-article-title">{take.get('title', '')}</div>
                <div class="editors-take-text">{take.get('take', '')}</div>
            </div>
            """
        
        return f"""
        <section class="editors-take-section">
            <h2 class="editors-take-title">✍️ Editor's Take</h2>
            {takes_html}
        </section>
        """
    
    def generate_fixed_html(self, content):
        """Generate HTML newsletter using programmatic approach"""
        logger.info("🎨 Generating fixed HTML newsletter...")
        
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Get articles and summaries
        articles = content.get('articles', [])
        summaries = content.get('summaries', [])
        
        # Categorize content
        categorized = self.categorize_articles_by_content(articles, summaries)
        
        # Build HTML document
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>🧠 AI Daily Digest – {current_date}</title>
    <style>{self.get_css_styles()}</style>
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
            <div class="intro-text">{content.get('intro', '')}</div>
        </section>
        
        <!-- Content Sections -->
        {self.build_section_html('research', categorized.get('research', []))}
        {self.build_section_html('tools', categorized.get('tools', []))}
        {self.build_section_html('industry', categorized.get('industry', []))}
        {self.build_section_html('use-case', categorized.get('use-case', []))}
        {self.build_section_html('misc', categorized.get('misc', []))}
        
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
</html>"""
        
        # Save to file
        output_path = os.path.join(self.output_dir, "newsletter_fixed.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Fixed HTML newsletter saved to: {output_path}")
        return output_path
    
    def save_all_formats(self, content):
        """Save newsletter in multiple formats with expected file keys"""
        logger.info("💾 Saving fixed newsletter...")
        
        saved_files = {}
        
        try:
            # Generate the HTML content
            html_path = self.generate_fixed_html(content)
            
            # Save with multiple keys that the main generator expects
            saved_files['fixed_html'] = html_path
            saved_files['email_html'] = html_path  # For email sending
            saved_files['premium_html'] = html_path  # Alternative key
            saved_files['styled_html'] = html_path  # Another alternative
            
            logger.info(f"✅ Saved newsletter in multiple formats successfully")
            logger.info(f"📁 Available file keys: {list(saved_files.keys())}")
            
        except Exception as e:
            logger.error(f"Error saving newsletter formats: {e}")
        
        return saved_files


# Main function
def save_fixed_newsletter_files(content, output_dir=None):
    """Save fixed newsletter files"""
    processor = FixedHTMLProcessor(output_dir)
    return processor.save_all_formats(content)
