"""
LLM summarization utilities for AI Newsletter Generator
"""
import requests
import time
import logging
from config import LLM_API_URL, MODEL_NAME, DELAY_BETWEEN_SUMMARIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def call_local_llm(prompt, temperature=0.7):
    """Make a call to the local LLM API"""
    try:
        data = {
            "model": MODEL_NAME,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature
        }
        
        response = requests.post(LLM_API_URL, json=data)
        response.raise_for_status()
        
        return response.json()['choices'][0]['message']['content']
        
    except Exception as e:
        logger.error(f"LLM API call failed: {e}")
        return None


def get_rundown_summary(article):
    """Generate a Rundown-style summary for an article"""
    prompt = f"""
You are a newsletter writer summarizing AI news in a style similar to 'The Rundown AI'.

Write a markdown-formatted section for the article below with these parts:
1. A catchy title
2. A one-sentence bold summary prefixed by "The Rundown:"
3. 2–3 detailed bullet points (use emojis)
4. A 'Why it matters' paragraph
5. A markdown link saying "[👉 Read more]({article['url']})"

Use clean formatting and sound like a smart, concise human editor.

Title: {article['title']}
URL: {article['url']}
Article:
{article['text']}
"""
    
    logger.info(f"🧠 Summarizing: {article['title']}")
    summary = call_local_llm(prompt, temperature=0.7)
    
    if summary and article['image_url']:
        summary = f"![thumbnail]({article['image_url']})\n\n" + summary
    
    return summary


def get_intro_section(articles):
    """Generate an intro section for the newsletter"""
    titles = "\n".join([f"- {article['title']}" for article in articles])
    
    prompt = f"""
You are writing the intro section of a curated AI newsletter.

Here are the top article titles:
{titles}

Write a friendly, smart 2-paragraph intro summarizing today's AI news themes. Make it sound like a human editor, not a robot.
"""
    
    logger.info("✍️ Generating newsletter intro...")
    return call_local_llm(prompt, temperature=0.6)


def get_basic_summary(article):
    """Generate a basic summary for an article (alternative style)"""
    prompt = f"""
You are a smart but punchy AI news editor writing for a tech-savvy audience.

Summarize the following article for a newsletter in this format:

1. 🔥 **Headline**: A short, catchy 1-liner that's truthful and clicky
2. 🧠 **Tagline**: A 1-sentence teaser that makes readers want to know more
3. ✍️ **Summary**: 2–4 sentence digest of the article's core info and implications
4. 🔗 **Link**: Include this exact markdown format: [Read more]({article['url']})

Title: {article['title']}

Article:
{article['text']}
"""
    
    logger.info(f"🧠 Summarizing: {article['title']}")
    return call_local_llm(prompt, temperature=0.7)


def summarize_articles(articles, style="rundown"):
    """Summarize a list of articles"""
    summaries = []
    
    for article in articles:
        if style == "rundown":
            summary = get_rundown_summary(article)
        else:
            summary = get_basic_summary(article)
            
        if summary:
            summaries.append(summary)
            
        # Rate limiting
        time.sleep(DELAY_BETWEEN_SUMMARIES)
    
    logger.info(f"✅ Generated {len(summaries)} summaries")
    return summaries


def generate_newsletter_content(articles, style="rundown"):
    """Generate complete newsletter content"""
    # Generate intro
    intro = get_intro_section(articles)
    
    # Generate summaries
    summaries = summarize_articles(articles, style)
    
    return {
        'intro': intro,
        'summaries': summaries,
        'articles': articles
    }
