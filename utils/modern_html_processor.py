"""
Modern HTML processing utilities for beautiful, responsive newsletter generation
"""
import os
from datetime import datetime
from markdown import markdown
from bs4 import BeautifulSoup
import logging
from config import OUTPUT_DIR

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_modern_css():
    """Generate modern CSS with responsive design and beautiful styling"""
    return """
    <style>
        /* CSS Custom Properties for theming */
        :root {
            --primary-color: #6366f1;
            --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            --secondary-color: #f59e0b;
            --accent-color: #10b981;
            --text-primary: #1f2937;
            --text-secondary: #6b7280;
            --text-muted: #9ca3af;
            --bg-primary: #ffffff;
            --bg-secondary: #f9fafb;
            --bg-tertiary: #f3f4f6;
            --border-color: #e5e7eb;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
            --radius-sm: 0.375rem;
            --radius-md: 0.5rem;
            --radius-lg: 0.75rem;
            --radius-xl: 1rem;
        }

        /* Reset and base styles */
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: var(--text-primary);
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Container and layout */
        .newsletter-container {
            max-width: 800px;
            margin: 0 auto;
            background: var(--bg-primary);
            box-shadow: var(--shadow-xl);
            border-radius: var(--radius-xl);
            overflow: hidden;
            position: relative;
        }

        /* Hero header section */
        .newsletter-header {
            background: var(--primary-gradient);
            color: white;
            padding: 3rem 2rem 2rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .newsletter-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
            pointer-events: none;
        }

        .newsletter-title {
            font-size: 2.5rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            position: relative;
            z-index: 1;
        }

        .newsletter-date {
            font-size: 1.1rem;
            opacity: 0.9;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }

        .newsletter-subtitle {
            font-size: 1rem;
            opacity: 0.8;
            margin-top: 0.5rem;
            position: relative;
            z-index: 1;
        }

        /* Introduction section */
        .newsletter-intro {
            padding: 2rem;
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
        }

        .intro-text {
            font-size: 1.1rem;
            line-height: 1.7;
            color: var(--text-secondary);
            text-align: center;
            max-width: 600px;
            margin: 0 auto;
        }

        /* Article grid */
        .articles-grid {
            padding: 2rem;
            display: grid;
            gap: 2rem;
            background: var(--bg-primary);
        }

        /* Article cards */
        .article-card {
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow-md);
            overflow: hidden;
            transition: all 0.3s ease;
            border: 1px solid var(--border-color);
            position: relative;
        }

        .article-card:hover {
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }

        .article-image {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-bottom: 1px solid var(--border-color);
        }

        .article-content {
            padding: 1.5rem;
        }

        .article-category {
            display: inline-block;
            background: var(--primary-gradient);
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: var(--radius-sm);
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
        }

        .article-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            line-height: 1.4;
        }

        .article-rundown {
            font-size: 1rem;
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 1rem;
            padding: 1rem;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
            border-radius: var(--radius-md);
            border-left: 4px solid var(--primary-color);
        }

        .article-points {
            list-style: none;
            margin: 1rem 0;
        }

        .article-points li {
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: var(--text-secondary);
            line-height: 1.6;
        }

        .article-points li::before {
            content: '✨';
            position: absolute;
            left: 0;
            top: 0.5rem;
            font-size: 0.875rem;
        }

        .why-matters {
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.1) 100%);
            padding: 1rem;
            border-radius: var(--radius-md);
            border-left: 4px solid var(--accent-color);
            margin: 1rem 0;
        }

        .why-matters-title {
            font-weight: 700;
            color: var(--accent-color);
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .why-matters-text {
            color: var(--text-secondary);
            line-height: 1.6;
        }

        /* Call-to-action button */
        .read-more-btn {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: var(--primary-gradient);
            color: white;
            text-decoration: none;
            padding: 0.75rem 1.5rem;
            border-radius: var(--radius-md);
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-sm);
            margin-top: 1rem;
        }

        .read-more-btn:hover {
            transform: translateY(-1px);
            box-shadow: var(--shadow-md);
            text-decoration: none;
            color: white;
        }

        .read-more-btn::after {
            content: '→';
            transition: transform 0.3s ease;
        }

        .read-more-btn:hover::after {
            transform: translateX(2px);
        }

        /* Footer */
        .newsletter-footer {
            background: var(--bg-tertiary);
            padding: 2rem;
            text-align: center;
            border-top: 1px solid var(--border-color);
        }

        .footer-text {
            color: var(--text-muted);
            font-size: 0.875rem;
        }

        /* Responsive design */
        @media (max-width: 768px) {
            .newsletter-container {
                margin: 0;
                border-radius: 0;
            }

            .newsletter-header {
                padding: 2rem 1rem 1.5rem;
            }

            .newsletter-title {
                font-size: 2rem;
            }

            .newsletter-intro,
            .articles-grid {
                padding: 1.5rem;
            }

            .article-content {
                padding: 1rem;
            }

            .article-title {
                font-size: 1.125rem;
            }
        }

        @media (max-width: 480px) {
            .newsletter-header {
                padding: 1.5rem 1rem;
            }

            .newsletter-title {
                font-size: 1.75rem;
            }

            .newsletter-intro,
            .articles-grid {
                padding: 1rem;
            }

            .articles-grid {
                gap: 1.5rem;
            }
        }

        /* Print styles */
        @media print {
            .newsletter-container {
                box-shadow: none;
                border-radius: 0;
            }

            .article-card {
                break-inside: avoid;
                box-shadow: none;
                border: 1px solid var(--border-color);
            }
        }

        /* High contrast mode support */
        @media (prefers-contrast: high) {
            :root {
                --text-primary: #000000;
                --text-secondary: #333333;
                --border-color: #666666;
            }
        }

        /* Reduced motion support */
        @media (prefers-reduced-motion: reduce) {
            * {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
    """


def generate_modern_newsletter_html(content):
    """Generate modern, beautiful HTML newsletter"""
    date_str = datetime.today().strftime('%B %d, %Y')
    
    # Start building the HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="en">',
        '<head>',
        '    <meta charset="UTF-8">',
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '    <meta http-equiv="X-UA-Compatible" content="IE=edge">',
        f'    <title>🧠 AI News Digest – {date_str}</title>',
        get_modern_css(),
        '</head>',
        '<body>',
        '    <div class="newsletter-container">',
        '        <!-- Header Section -->',
        '        <header class="newsletter-header">',
        '            <h1 class="newsletter-title">🧠 AI News Digest</h1>',
        f'            <p class="newsletter-date">{date_str}</p>',
        '            <p class="newsletter-subtitle">Your curated source for the latest in artificial intelligence</p>',
        '        </header>',
        '',
        '        <!-- Introduction Section -->',
        '        <section class="newsletter-intro">',
        f'            <div class="intro-text">{content.get("intro", "")}</div>',
        '        </section>',
        '',
        '        <!-- Articles Grid -->',
        '        <main class="articles-grid">',
    ]
    
    # Add articles
    for i, summary in enumerate(content.get('summaries', [])):
        article_html = process_article_summary(summary, i)
        html_parts.append(article_html)
    
    # Close the HTML
    html_parts.extend([
        '        </main>',
        '',
        '        <!-- Footer -->',
        '        <footer class="newsletter-footer">',
        '            <p class="footer-text">',
        '                Made with ❤️ by AI Newsletter Generator<br>',
        '                Stay curious, stay informed!',
        '            </p>',
        '        </footer>',
        '    </div>',
        '</body>',
        '</html>'
    ])
    
    return '\n'.join(html_parts)


def process_article_summary(summary, index):
    """Process individual article summary into modern HTML card"""
    # Parse the markdown summary to extract components
    lines = summary.strip().split('\n')
    
    # Extract image URL if present
    image_url = ""
    title = ""
    rundown = ""
    points = []
    why_matters = ""
    read_more_url = ""
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Extract image
        if line.startswith('![thumbnail]'):
            image_url = line.split('(')[1].split(')')[0] if '(' in line else ""
            continue
            
        # Extract title (usually starts with #)
        if line.startswith('#') and not title:
            title = line.lstrip('#').strip()
            continue
            
        # Extract rundown
        if line.startswith('The Rundown:'):
            rundown = line.replace('The Rundown:', '').strip()
            current_section = 'rundown'
            continue
            
        # Extract bullet points
        if line.startswith('-') or line.startswith('*'):
            points.append(line.lstrip('-*').strip())
            current_section = 'points'
            continue
            
        # Extract why it matters
        if 'Why it matters' in line or 'why it matters' in line:
            current_section = 'why_matters'
            why_matters = line.replace('Why it matters:', '').replace('**Why it matters:**', '').strip()
            continue
            
        # Extract read more link
        if '👉' in line and '[' in line and '](' in line:
            # Extract URL from markdown link
            start = line.find('](') + 2
            end = line.find(')', start)
            if start > 1 and end > start:
                read_more_url = line[start:end]
            continue
            
        # Continue building sections
        if current_section == 'why_matters' and line and not line.startswith('['):
            why_matters += ' ' + line
        elif current_section == 'rundown' and line and not line.startswith('-') and not line.startswith('*'):
            rundown += ' ' + line
    
    # Generate category based on content
    category = get_article_category(title + ' ' + rundown)
    
    # Build the article card HTML
    card_html = f'''
            <article class="article-card">
                {f'<img src="{image_url}" alt="Article thumbnail" class="article-image" loading="lazy">' if image_url else ''}
                <div class="article-content">
                    <span class="article-category">{category}</span>
                    <h2 class="article-title">{title}</h2>
                    {f'<div class="article-rundown">{rundown}</div>' if rundown else ''}
                    
                    {generate_points_html(points) if points else ''}
                    
                    {f'''<div class="why-matters">
                        <div class="why-matters-title">Why it matters</div>
                        <div class="why-matters-text">{why_matters}</div>
                    </div>''' if why_matters else ''}
                    
                    {f'<a href="{read_more_url}" class="read-more-btn">Read Full Article</a>' if read_more_url else ''}
                </div>
            </article>
    '''
    
    return card_html


def generate_points_html(points):
    """Generate HTML for article bullet points"""
    if not points:
        return ""
    
    points_html = '<ul class="article-points">'
    for point in points:
        # Clean up the point text
        clean_point = point.replace('**', '').replace('*', '').strip()
        points_html += f'<li>{clean_point}</li>'
    points_html += '</ul>'
    
    return points_html


def get_article_category(text):
    """Determine article category based on content"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['anthropic', 'claude', 'openai', 'gpt']):
        return 'AI Models'
    elif any(word in text_lower for word in ['google', 'microsoft', 'apple', 'meta']):
        return 'Big Tech'
    elif any(word in text_lower for word in ['startup', 'funding', 'investment', 'venture']):
        return 'Startups'
    elif any(word in text_lower for word in ['research', 'study', 'paper', 'university']):
        return 'Research'
    elif any(word in text_lower for word in ['regulation', 'policy', 'government', 'law']):
        return 'Policy'
    elif any(word in text_lower for word in ['data', 'center', 'cloud', 'infrastructure']):
        return 'Infrastructure'
    else:
        return 'AI News'


def save_modern_newsletter_files(content, output_dir=None):
    """Save modern newsletter files"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate modern HTML
    modern_html = generate_modern_newsletter_html(content)
    
    # Save modern HTML
    modern_path = os.path.join(output_dir, "newsletter_modern.html")
    with open(modern_path, 'w', encoding='utf-8') as f:
        f.write(modern_html)
    
    logger.info(f"✅ Saved modern newsletter: {modern_path}")
    
    return {
        'modern_html': modern_path
    }
