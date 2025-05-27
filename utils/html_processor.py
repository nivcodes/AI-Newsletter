"""
HTML processing utilities for newsletter generation and styling
"""
import os
from datetime import datetime
from markdown import markdown
from bs4 import BeautifulSoup
import logging
from config import NEWSLETTER_TEMPLATE, OUTPUT_DIR

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_markdown_to_html(md_content):
    """Convert markdown content to HTML"""
    try:
        html_content = markdown(md_content, extensions=['extra', 'smarty'])
        return html_content
    except Exception as e:
        logger.error(f"Failed to convert markdown to HTML: {e}")
        return None


def generate_markdown_newsletter(content):
    """Generate markdown newsletter from content"""
    date_str = datetime.today().strftime('%B %d, %Y')
    
    # Build markdown content
    md_parts = [
        f"# 🗞️ AI News Digest",
        f"**{date_str}**",
        "",
        content['intro'] if content['intro'] else "",
        "",
        "---",
        ""
    ]
    
    # Add summaries
    for summary in content['summaries']:
        md_parts.extend([summary, "", "---", ""])
    
    return "\n".join(md_parts)


def apply_inline_styles(html_content):
    """Apply inline CSS styles for email compatibility"""
    soup = BeautifulSoup(html_content, "lxml")
    
    # Define inline styles
    styles = {
        "body": {
            "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif",
            "line-height": "1.6",
            "padding": "30px",
            "background-color": "#f9f9f9",
            "color": "#2c2c2c",
            "max-width": "720px",
            "margin": "auto",
            "box-shadow": "0 10px 30px rgba(0, 0, 0, 0.05)",
            "border-radius": "12px"
        },
        "h1": {
            "color": "#1a73e8",
            "font-size": "1.75em",
            "border-bottom": "2px solid #eee",
            "padding-bottom": "5px",
            "margin-top": "1.5em",
            "margin-bottom": "0.6em",
            "font-weight": "600"
        },
        "h2": {
            "color": "#1a73e8",
            "font-size": "1.4em",
            "margin-top": "1.5em",
            "margin-bottom": "0.6em",
            "font-weight": "600"
        },
        "h3": {
            "color": "#1a73e8",
            "font-size": "1.2em",
            "margin-top": "1.5em",
            "margin-bottom": "0.6em",
            "font-weight": "600"
        },
        "p": {
            "margin": "1em 0"
        },
        "ul": {
            "padding-left": "20px",
            "margin-top": "0.5em",
            "margin-bottom": "1.5em",
            "line-height": "1.6"
        },
        "img": {
            "display": "block",
            "margin": "24px auto",
            "max-width": "100%",
            "height": "auto",
            "border-radius": "12px",
            "box-shadow": "0 4px 12px rgba(0, 0, 0, 0.05)"
        },
        "a": {
            "color": "#1a73e8",
            "text-decoration": "none",
            "font-weight": "500"
        },
        "hr": {
            "border": "none",
            "border-top": "1px solid #ddd",
            "margin": "2.5em 0"
        },
        ".section": {
            "background": "#ffffff",
            "padding": "20px",
            "border-radius": "12px",
            "margin-bottom": "30px",
            "box-shadow": "0 4px 10px rgba(0,0,0,0.03)"
        }
    }
    
    # Apply inline styles
    for selector, style_dict in styles.items():
        if selector.startswith('.'):
            # Handle class selectors
            class_name = selector[1:]
            elements = soup.find_all(class_=class_name)
        else:
            # Handle tag selectors
            elements = soup.find_all(selector)
            
        for element in elements:
            style_string = "; ".join([f"{k}: {v}" for k, v in style_dict.items()])
            element["style"] = style_string
    
    return str(soup)


def wrap_content_in_sections(html_content):
    """Wrap article content in section divs for better styling"""
    soup = BeautifulSoup(html_content, "lxml")
    
    # Find all hr tags to identify article boundaries
    hrs = soup.find_all('hr')
    
    if not hrs:
        return html_content
    
    # Process content between hr tags
    current_section = []
    new_body = soup.new_tag('body')
    
    for element in soup.body.children if soup.body else []:
        if element.name == 'hr':
            if current_section:
                # Create section div
                section_div = soup.new_tag('div', class_='section')
                for item in current_section:
                    section_div.append(item)
                new_body.append(section_div)
                current_section = []
            new_body.append(element)
        else:
            current_section.append(element)
    
    # Handle remaining content
    if current_section:
        section_div = soup.new_tag('div', class_='section')
        for item in current_section:
            section_div.append(item)
        new_body.append(section_div)
    
    if soup.body:
        soup.body.replace_with(new_body)
    
    return str(soup)


def generate_html_newsletter(content, apply_styling=True):
    """Generate complete HTML newsletter"""
    logger.info("📄 Generating HTML newsletter...")
    
    # Generate markdown first
    md_content = generate_markdown_newsletter(content)
    
    # Convert to HTML
    html_content = convert_markdown_to_html(md_content)
    if not html_content:
        return None
    
    # Add basic HTML structure
    full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🗞️ AI News Digest – {datetime.today().strftime('%B %d, %Y')}</title>
</head>
<body>
{html_content}
</body>
</html>
"""
    
    if apply_styling:
        # Wrap in sections
        full_html = wrap_content_in_sections(full_html)
        
        # Apply inline styles
        full_html = apply_inline_styles(full_html)
    
    return full_html


def save_newsletter_files(content, output_dir=None):
    """Save newsletter in both markdown and HTML formats"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate content
    md_content = generate_markdown_newsletter(content)
    html_content = generate_html_newsletter(content, apply_styling=False)
    styled_html_content = generate_html_newsletter(content, apply_styling=True)
    
    # Save files
    files_saved = {}
    
    # Save markdown
    md_path = os.path.join(output_dir, "newsletter.md")
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
    files_saved['markdown'] = md_path
    logger.info(f"✅ Saved markdown: {md_path}")
    
    # Save basic HTML
    html_path = os.path.join(output_dir, "newsletter.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    files_saved['html'] = html_path
    logger.info(f"✅ Saved HTML: {html_path}")
    
    # Save styled HTML
    styled_path = os.path.join(output_dir, "newsletter_styled.html")
    with open(styled_path, 'w', encoding='utf-8') as f:
        f.write(styled_html_content)
    files_saved['styled_html'] = styled_path
    logger.info(f"✅ Saved styled HTML: {styled_path}")
    
    return files_saved
