"""
Premium HTML processor for enhanced newsletter generation with categorization and visual elements
"""
import os
import markdown
import logging
from datetime import datetime
from bs4 import BeautifulSoup
import re
from config import OUTPUT_DIR, TEMPLATE_DIR, CATEGORIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PremiumHTMLProcessor:
    """Process newsletter content into premium HTML format with categorization"""
    
    def __init__(self, template_path=None):
        self.template_path = template_path or f"{TEMPLATE_DIR}/premium_newsletter_template.html"
        self.output_dir = OUTPUT_DIR
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir, exist_ok=True)
    
    def load_template(self):
        """Load the HTML template"""
        try:
            with open(self.template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            logger.error(f"Template not found: {self.template_path}")
            return self.get_fallback_template()
    
    def get_fallback_template(self):
        """Provide a basic fallback template if main template is missing"""
        return """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>AI Daily Digest – {{date}}</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 720px; margin: 0 auto; padding: 20px; }
        .article { margin-bottom: 30px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        h1 { color: #333; }
        h2 { color: #666; }
    </style>
</head>
<body>
    <h1>🧠 AI Daily Digest – {{date}}</h1>
    {{#if intro}}<div class="intro">{{intro}}</div>{{/if}}
    <div class="content">{{content}}</div>
</body>
</html>
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
                    'content': summaries[i],
                    'popularity_score': article.get('popularity_score', 0)
                }
                categorized[category].append(article_data)
        
        return categorized
    
    def process_markdown_content(self, content):
        """Convert markdown content to HTML and enhance formatting"""
        if not content:
            return ""
        
        # Convert markdown to HTML
        html_content = markdown.markdown(content, extensions=['extra'])
        
        # Parse with BeautifulSoup for enhancement
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Enhance "The Rundown:" sections
        for p in soup.find_all('p'):
            if p.get_text().startswith('**The Rundown:**'):
                p['class'] = 'article-rundown'
        
        # Enhance "Why it matters:" sections
        for p in soup.find_all('p'):
            if '**Why it matters:**' in p.get_text():
                p['class'] = 'article-why-matters'
                # Wrap the label
                content = str(p)
                content = content.replace('**Why it matters:**', 
                    '<div class="why-matters-label">🎯 Why it matters:</div>')
                p.replace_with(BeautifulSoup(content, 'html.parser'))
        
        # Enhance bullet points
        for ul in soup.find_all('ul'):
            ul['class'] = 'article-points'
        
        # Enhance links
        for a in soup.find_all('a'):
            if 'Read more' in a.get_text() or '👉' in a.get_text():
                a['class'] = 'article-link'
        
        return str(soup)
    
    def create_template_data(self, content):
        """Create data structure for template rendering"""
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Get articles and summaries
        articles = content.get('articles', [])
        summaries = content.get('summaries', [])
        
        # Categorize content
        categorized = self.categorize_articles_by_content(articles, summaries)
        
        # Process each category's content
        template_data = {
            'date': current_date,
            'intro': content.get('intro', ''),
            'editors_takes': content.get('editors_takes', [])
        }
        
        # Add categorized articles with processed content
        for category, articles_list in categorized.items():
            if articles_list:
                processed_articles = []
                for article in articles_list:
                    processed_article = {
                        'title': article['title'],
                        'url': article['url'],
                        'image_url': article['image_url'],
                        'content': self.process_markdown_content(article['content'])
                    }
                    processed_articles.append(processed_article)
                
                # Map category names to template variables
                category_mapping = {
                    'research': 'research_articles',
                    'tools': 'tools_articles',
                    'industry': 'industry_articles',
                    'use-case': 'usecase_articles',
                    'misc': 'misc_articles'
                }
                
                template_var = category_mapping.get(category, f"{category}_articles")
                template_data[template_var] = processed_articles
        
        return template_data
    
    def simple_template_render(self, template, data):
        """Improved template rendering that properly handles loops without nesting"""
        result = template
        
        # Replace simple variables first
        for key, value in data.items():
            if isinstance(value, str):
                result = result.replace(f"{{{{{key}}}}}", value)
        
        # Handle conditional sections properly
        for category in ['research_articles', 'tools_articles', 'industry_articles', 
                        'usecase_articles', 'misc_articles']:
            articles = data.get(category, [])
            
            if articles:
                # Find the section pattern
                section_pattern = f"{{{{#if {category}}}}}(.*?){{{{/if}}}}"
                section_match = re.search(section_pattern, result, re.DOTALL)
                if section_match:
                    section_content = section_match.group(1)
                    
                    # Extract the article template from within the section
                    # Look for the {{#each}} pattern within this section
                    each_pattern = f"{{{{#each {category}}}}}(.*?){{{{/each}}}}"
                    each_match = re.search(each_pattern, section_content, re.DOTALL)
                    
                    if each_match:
                        # Use the {{#each}} template
                        article_template = each_match.group(1)
                        
                        # Generate HTML for all articles
                        articles_html = ""
                        for article in articles:
                            article_html = article_template
                            
                            # Replace article variables
                            for key, value in article.items():
                                article_html = article_html.replace(f"{{{{{key}}}}}", str(value))
                            
                            # Handle image conditional
                            if article.get('image_url'):
                                article_html = re.sub(r'{{#if image_url}}(.*?){{/if}}', r'\1', article_html, flags=re.DOTALL)
                            else:
                                article_html = re.sub(r'{{#if image_url}}(.*?){{/if}}', '', article_html, flags=re.DOTALL)
                            
                            articles_html += article_html
                        
                        # Replace the {{#each}} block with the generated content
                        section_content = section_content.replace(each_match.group(0), articles_html)
                    
                    # Replace the entire section
                    result = result.replace(section_match.group(0), section_content)
            else:
                # Remove the entire section if no articles
                section_pattern = f"{{{{#if {category}}}}}(.*?){{{{/if}}}}"
                result = re.sub(section_pattern, '', result, flags=re.DOTALL)
        
        # Handle intro section
        if data.get('intro'):
            result = re.sub(r'{{#if intro}}(.*?){{/if}}', r'\1', result, flags=re.DOTALL)
            result = result.replace('{{intro}}', data['intro'])
        else:
            result = re.sub(r'{{#if intro}}(.*?){{/if}}', '', result, flags=re.DOTALL)
        
        # Handle editor's takes
        editors_takes = data.get('editors_takes', [])
        if editors_takes:
            result = re.sub(r'{{#if editors_takes}}(.*?){{/if}}', r'\1', result, flags=re.DOTALL)
            
            # Process each editor's take
            takes_pattern = r'{{#each editors_takes}}(.*?){{/each}}'
            takes_match = re.search(takes_pattern, result, re.DOTALL)
            if takes_match:
                take_template = takes_match.group(1)
                takes_html = ""
                
                for take in editors_takes:
                    take_html = take_template
                    take_html = take_html.replace('{{title}}', take.get('title', ''))
                    take_html = take_html.replace('{{take}}', take.get('take', ''))
                    takes_html += take_html
                
                result = result.replace(takes_match.group(0), takes_html)
        else:
            result = re.sub(r'{{#if editors_takes}}(.*?){{/if}}', '', result, flags=re.DOTALL)
        
        # Clean up any remaining template syntax
        result = re.sub(r'{{.*?}}', '', result)
        
        return result
    
    def generate_premium_html(self, content):
        """Generate premium HTML newsletter"""
        logger.info("🎨 Generating premium HTML newsletter...")
        
        # Load template
        template = self.load_template()
        
        # Create template data
        template_data = self.create_template_data(content)
        
        # Render template
        html_content = self.simple_template_render(template, template_data)
        
        # Save to file
        output_path = os.path.join(self.output_dir, "newsletter_premium.html")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"✅ Premium HTML newsletter saved to: {output_path}")
        return output_path
    
    def generate_email_optimized_html(self, content):
        """Generate email-optimized HTML (inline CSS)"""
        logger.info("📧 Generating email-optimized HTML...")
        
        # First generate premium HTML
        premium_path = self.generate_premium_html(content)
        
        # Read the generated HTML
        with open(premium_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract CSS from style tag
        style_tag = soup.find('style')
        if style_tag:
            css_content = style_tag.string
            
            # Simple CSS inlining (basic implementation)
            # In production, you'd use a proper CSS inliner like premailer
            
            # Remove animations and complex selectors for email compatibility
            css_lines = css_content.split('\n')
            email_safe_css = []
            
            skip_block = False
            for line in css_lines:
                line = line.strip()
                
                # Skip animation blocks
                if '@keyframes' in line or 'animation:' in line:
                    skip_block = True
                    continue
                elif skip_block and '}' in line:
                    skip_block = False
                    continue
                elif skip_block:
                    continue
                
                # Skip media queries for email
                if '@media' in line:
                    skip_block = True
                    continue
                
                # Keep basic styles
                if not skip_block:
                    email_safe_css.append(line)
            
            # Update style tag
            style_tag.string = '\n'.join(email_safe_css)
        
        # Save email-optimized version
        email_path = os.path.join(self.output_dir, "newsletter_email_premium.html")
        with open(email_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        
        logger.info(f"✅ Email-optimized HTML saved to: {email_path}")
        return email_path
    
    def generate_markdown_export(self, content):
        """Generate markdown export for Notion/Obsidian"""
        logger.info("📝 Generating markdown export...")
        
        markdown_content = []
        
        # Header
        current_date = datetime.now().strftime("%B %d, %Y")
        markdown_content.append(f"# 🧠 AI Daily Digest – {current_date}")
        markdown_content.append("")
        
        # Intro
        if content.get('intro'):
            markdown_content.append(content['intro'])
            markdown_content.append("")
        
        # Articles by category
        articles = content.get('articles', [])
        summaries = content.get('summaries', [])
        categorized = self.categorize_articles_by_content(articles, summaries)
        
        for category, articles_list in categorized.items():
            if articles_list:
                category_config = CATEGORIES.get(category, CATEGORIES['misc'])
                markdown_content.append(f"## {category_config['emoji']} {category_config['title']}")
                markdown_content.append("")
                
                for article in articles_list:
                    markdown_content.append(article['content'])
                    markdown_content.append("")
        
        # Editor's takes
        editors_takes = content.get('editors_takes', [])
        if editors_takes:
            markdown_content.append("## ✍️ Editor's Take")
            markdown_content.append("")
            
            for take in editors_takes:
                markdown_content.append(f"**{take['title']}**")
                markdown_content.append("")
                markdown_content.append(take['take'])
                markdown_content.append("")
        
        # Save markdown
        md_content = "\n".join(markdown_content)
        md_path = os.path.join(self.output_dir, "newsletter_premium.md")
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        logger.info(f"✅ Markdown export saved to: {md_path}")
        return md_path
    
    def generate_json_export(self, content):
        """Generate JSON export for API consumption"""
        import json
        
        logger.info("📊 Generating JSON export...")
        
        # Organize data for JSON export
        articles = content.get('articles', [])
        summaries = content.get('summaries', [])
        categorized = self.categorize_articles_by_content(articles, summaries)
        
        json_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'total_articles': len(articles),
                'categories': list(categorized.keys()),
                'llm_used': content.get('generation_info', {}).get('llm_used', 'unknown')
            },
            'intro': content.get('intro', ''),
            'categories': {},
            'editors_takes': content.get('editors_takes', [])
        }
        
        # Add categorized articles
        for category, articles_list in categorized.items():
            if articles_list:
                json_data['categories'][category] = {
                    'title': CATEGORIES.get(category, {}).get('title', category.title()),
                    'emoji': CATEGORIES.get(category, {}).get('emoji', '📄'),
                    'articles': articles_list
                }
        
        # Save JSON
        json_path = os.path.join(self.output_dir, "newsletter_premium.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ JSON export saved to: {json_path}")
        return json_path
    
    def save_all_formats(self, content):
        """Save newsletter in all available formats"""
        logger.info("💾 Saving newsletter in all formats...")
        
        saved_files = {}
        
        try:
            # Premium HTML
            saved_files['premium_html'] = self.generate_premium_html(content)
            
            # Email-optimized HTML
            saved_files['email_html'] = self.generate_email_optimized_html(content)
            
            # Markdown export
            saved_files['markdown'] = self.generate_markdown_export(content)
            
            # JSON export
            saved_files['json'] = self.generate_json_export(content)
            
            logger.info(f"✅ Saved {len(saved_files)} formats successfully")
            
        except Exception as e:
            logger.error(f"Error saving formats: {e}")
        
        return saved_files


# Main functions for backward compatibility
def save_premium_newsletter_files(content, output_dir=None):
    """Save premium newsletter files in multiple formats"""
    processor = PremiumHTMLProcessor()
    if output_dir:
        processor.output_dir = output_dir
    return processor.save_all_formats(content)

def generate_premium_html(content, output_dir=None):
    """Generate premium HTML newsletter"""
    processor = PremiumHTMLProcessor()
    if output_dir:
        processor.output_dir = output_dir
    return processor.generate_premium_html(content)
