"""
Email-optimized HTML processing utilities for Gmail-compatible newsletters
"""
import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import logging
from config import OUTPUT_DIR

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_email_optimized_newsletter(content):
    """Generate Gmail-compatible HTML newsletter with inline styles"""
    date_str = datetime.today().strftime('%B %d, %Y')
    
    # Process articles to clean up formatting issues
    processed_articles = []
    for summary in content.get('summaries', []):
        processed_article = process_and_clean_article(summary)
        if processed_article:
            processed_articles.append(processed_article)
    
    # Build the email-optimized HTML
    html = f'''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>🧠 AI News Digest – {date_str}</title>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f7fa; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;">
    
    <!-- Main Container -->
    <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%" style="background-color: #f5f7fa;">
        <tr>
            <td align="center" style="padding: 20px 0;">
                
                <!-- Newsletter Container -->
                <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="600" style="max-width: 600px; background-color: #ffffff; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 30px; text-align: center; border-radius: 12px 12px 0 0;">
                            <h1 style="margin: 0; color: #ffffff; font-size: 32px; font-weight: 800; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                🧠 AI News Digest
                            </h1>
                            <p style="margin: 8px 0 0 0; color: #ffffff; font-size: 16px; opacity: 0.9;">
                                {date_str}
                            </p>
                            <p style="margin: 4px 0 0 0; color: #ffffff; font-size: 14px; opacity: 0.8;">
                                Your curated source for the latest in artificial intelligence
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Introduction -->
                    <tr>
                        <td style="padding: 30px; background-color: #f9fafb; border-bottom: 1px solid #e5e7eb;">
                            <p style="margin: 0; font-size: 16px; line-height: 1.6; color: #6b7280; text-align: center;">
                                {content.get("intro", "Welcome to your AI news digest with the latest developments in artificial intelligence.")}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Articles -->
                    {generate_articles_html(processed_articles)}
                    
                    <!-- Footer -->
                    <tr>
                        <td style="padding: 30px; background-color: #f3f4f6; text-align: center; border-radius: 0 0 12px 12px;">
                            <p style="margin: 0; color: #9ca3af; font-size: 14px;">
                                Made with ❤️ by AI Newsletter Generator<br>
                                Stay curious, stay informed!
                            </p>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>
    '''
    
    return html


def process_and_clean_article(summary):
    """Process and clean article summary, fixing formatting issues"""
    lines = summary.strip().split('\n')
    
    article_data = {
        'image_url': '',
        'title': '',
        'rundown': '',
        'points': [],
        'why_matters': '',
        'read_more_url': '',
        'category': 'AI News'
    }
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Extract image
        if line.startswith('![thumbnail]'):
            match = re.search(r'\((.*?)\)', line)
            if match:
                article_data['image_url'] = match.group(1)
            continue
            
        # Extract title - clean up markdown formatting
        if line.startswith('#') and not article_data['title']:
            title = line.lstrip('#').strip()
            # Remove any remaining markdown formatting
            title = re.sub(r'\*\*(.*?)\*\*', r'\1', title)  # Remove bold
            title = re.sub(r'\*(.*?)\*', r'\1', title)      # Remove italic
            article_data['title'] = title
            continue
            
        # Extract rundown - clean formatting
        if line.startswith('The Rundown:') or 'The Rundown:' in line:
            rundown = line.replace('The Rundown:', '').strip()
            # Clean up markdown formatting
            rundown = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', rundown)
            rundown = re.sub(r'\*(.*?)\*', r'<em>\1</em>', rundown)
            article_data['rundown'] = rundown
            current_section = 'rundown'
            continue
            
        # Extract bullet points - clean formatting
        if line.startswith('-') or line.startswith('*'):
            point = line.lstrip('-*').strip()
            # Clean up markdown formatting
            point = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', point)
            point = re.sub(r'\*(.*?)\*', r'<em>\1</em>', point)
            article_data['points'].append(point)
            current_section = 'points'
            continue
            
        # Extract why it matters - clean formatting
        if 'Why it matters' in line or 'why it matters' in line:
            why_text = line
            # Remove markdown headers
            why_text = re.sub(r'^#+\s*', '', why_text)
            why_text = why_text.replace('Why it matters:', '').replace('**Why it matters:**', '').strip()
            # Clean up markdown formatting
            why_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', why_text)
            why_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', why_text)
            article_data['why_matters'] = why_text
            current_section = 'why_matters'
            continue
            
        # Extract read more link
        if '👉' in line and '[' in line and '](' in line:
            match = re.search(r'\]\((.*?)\)', line)
            if match:
                article_data['read_more_url'] = match.group(1)
            continue
            
        # Continue building sections
        if current_section == 'why_matters' and line and not line.startswith('['):
            additional_text = line
            # Clean up markdown formatting
            additional_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', additional_text)
            additional_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', additional_text)
            article_data['why_matters'] += ' ' + additional_text
        elif current_section == 'rundown' and line and not line.startswith('-') and not line.startswith('*'):
            additional_text = line
            # Clean up markdown formatting
            additional_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', additional_text)
            additional_text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', additional_text)
            article_data['rundown'] += ' ' + additional_text
    
    # Determine category
    article_data['category'] = get_smart_category(article_data['title'] + ' ' + article_data['rundown'])
    
    return article_data


def generate_articles_html(articles):
    """Generate HTML for all articles"""
    if not articles:
        return ""
    
    articles_html = ""
    
    for i, article in enumerate(articles):
        # Category colors
        category_colors = {
            'AI Models': '#8b5cf6',
            'Big Tech': '#3b82f6', 
            'Research': '#10b981',
            'Policy': '#f59e0b',
            'Infrastructure': '#6b7280',
            'Startups': '#ef4444',
            'AI News': '#6366f1'
        }
        
        category_color = category_colors.get(article['category'], '#6366f1')
        
        # Generate points HTML
        points_html = ""
        if article['points']:
            points_html = '<ul style="margin: 16px 0; padding-left: 0; list-style: none;">'
            for point in article['points']:
                points_html += f'''
                    <li style="margin: 8px 0; padding-left: 24px; position: relative; color: #6b7280; line-height: 1.6;">
                        <span style="position: absolute; left: 0; top: 0; color: #f59e0b;">✨</span>
                        {point}
                    </li>
                '''
            points_html += '</ul>'
        
        # Generate article HTML
        article_html = f'''
                    <!-- Article {i+1} -->
                    <tr>
                        <td style="padding: 0;">
                            <table role="presentation" cellspacing="0" cellpadding="0" border="0" width="100%">
                                
                                {f'''<!-- Article Image -->
                                <tr>
                                    <td style="padding: 0;">
                                        <img src="{article['image_url']}" alt="Article thumbnail" style="width: 100%; height: 200px; object-fit: cover; display: block; border: none;" />
                                    </td>
                                </tr>''' if article['image_url'] else ''}
                                
                                <!-- Article Content -->
                                <tr>
                                    <td style="padding: 30px;">
                                        
                                        <!-- Category Badge -->
                                        <div style="margin-bottom: 16px;">
                                            <span style="display: inline-block; background-color: {category_color}; color: #ffffff; padding: 4px 12px; border-radius: 6px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">
                                                {article['category']}
                                            </span>
                                        </div>
                                        
                                        <!-- Title -->
                                        <h2 style="margin: 0 0 16px 0; color: #1f2937; font-size: 24px; font-weight: 700; line-height: 1.3;">
                                            {article['title']}
                                        </h2>
                                        
                                        {f'''<!-- Rundown -->
                                        <div style="margin: 16px 0; padding: 16px; background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); border-radius: 8px; border-left: 4px solid #6366f1;">
                                            <p style="margin: 0; color: #6366f1; font-weight: 600; font-size: 16px;">
                                                {article['rundown']}
                                            </p>
                                        </div>''' if article['rundown'] else ''}
                                        
                                        {points_html}
                                        
                                        {f'''<!-- Why It Matters -->
                                        <div style="margin: 16px 0; padding: 16px; background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%); border-radius: 8px; border-left: 4px solid #10b981;">
                                            <p style="margin: 0 0 8px 0; color: #10b981; font-weight: 700; font-size: 12px; text-transform: uppercase; letter-spacing: 0.5px;">
                                                Why it matters
                                            </p>
                                            <p style="margin: 0; color: #6b7280; line-height: 1.6;">
                                                {article['why_matters']}
                                            </p>
                                        </div>''' if article['why_matters'] else ''}
                                        
                                        {f'''<!-- Read More Button -->
                                        <div style="margin-top: 20px;">
                                            <a href="{article['read_more_url']}" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; text-decoration: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 14px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                                                Read Full Article →
                                            </a>
                                        </div>''' if article['read_more_url'] else ''}
                                        
                                    </td>
                                </tr>
                                
                            </table>
                        </td>
                    </tr>
                    
                    <!-- Separator -->
                    <tr>
                        <td style="padding: 0 30px;">
                            <div style="height: 1px; background-color: #e5e7eb; margin: 20px 0;"></div>
                        </td>
                    </tr>
        '''
        
        articles_html += article_html
    
    return articles_html


def get_smart_category(text):
    """Determine article category with improved logic"""
    text_lower = text.lower()
    
    # More specific categorization
    if any(word in text_lower for word in ['anthropic', 'claude', 'openai', 'gpt', 'llm', 'language model']):
        return 'AI Models'
    elif any(word in text_lower for word in ['google', 'microsoft', 'apple', 'meta', 'amazon', 'nvidia']):
        return 'Big Tech'
    elif any(word in text_lower for word in ['startup', 'funding', 'investment', 'venture', 'series a', 'series b']):
        return 'Startups'
    elif any(word in text_lower for word in ['research', 'study', 'paper', 'university', 'mit', 'stanford']):
        return 'Research'
    elif any(word in text_lower for word in ['regulation', 'policy', 'government', 'law', 'congress', 'senate']):
        return 'Policy'
    elif any(word in text_lower for word in ['data center', 'cloud', 'infrastructure', 'server', 'computing']):
        return 'Infrastructure'
    else:
        return 'AI News'


def save_email_optimized_newsletter(content, output_dir=None):
    """Save email-optimized newsletter"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate email-optimized HTML
    email_html = generate_email_optimized_newsletter(content)
    
    # Save email-optimized HTML
    email_path = os.path.join(output_dir, "newsletter_email_optimized.html")
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_html)
    
    logger.info(f"✅ Saved email-optimized newsletter: {email_path}")
    
    return {
        'email_optimized_html': email_path
    }
