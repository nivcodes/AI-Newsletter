import feedparser
from newspaper import Article
import requests
import time
import os
from datetime import datetime

# === CONFIG ===
RSS_FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/feed/"
]
LLM_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_K_M"  # Replace with your actual model name
AI_KEYWORDS = ["AI", "artificial intelligence", "machine learning", "LLM", "GPT", "OpenAI", "Anthropic", "deep learning", "neural", "chatbot"]

# === FUNCTIONS ===

def is_ai_related(text):
    return any(keyword.lower() in text.lower() for keyword in AI_KEYWORDS)

def fetch_articles_from_rss():
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:5]:  # Grab top 5 per feed
            articles.append((entry.title, entry.link))
    return articles

def extract_article_content(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text, article.top_image or ""
    except Exception as e:
        print(f"❌ Failed to process {url}: {e}")
        return None, ""

def get_rundown_summary(title, text, url):
    prompt = f"""
You are a newsletter writer summarizing AI news in a style similar to 'The Rundown AI'.

Write a markdown-formatted section for the article below with these parts:
1. A catchy title
2. A one-sentence bold summary prefixed by "The Rundown:"
3. 2–3 detailed bullet points (use emojis)
4. A 'Why it matters' paragraph
5. A markdown link saying "[👉 Read more]({url})"

Use clean formatting and sound like a smart, concise human editor.

Title: {title}
URL: {url}
Article:
{text}
"""
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(LLM_API_URL, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

def save_newsletter_markdown(intro, sections):
    date_str = datetime.today().strftime('%B %d, %Y')
    header = f"# 🗞️ AI News Digest\n**{date_str}**\n\n{intro}\n\n---\n"
    content = "\n\n---\n\n".join(sections)
    with open("newsletter.md", "w") as f:
        f.write(header + content)
    return "newsletter.md"

def get_intro_section(articles_info):
    titles = "\n".join([f"- {title}" for title, _, _ in articles_info])
    prompt = f"""
You are writing the intro section of a curated AI newsletter.

Here are the top article titles:
{titles}

Write a friendly, smart 2-paragraph intro summarizing today’s AI news themes. Make it sound like a human editor, not a robot.
"""
    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.6
    }
    response = requests.post(LLM_API_URL, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content']

# === MAIN RUN ===
MAX_ARTICLES = 3

articles = fetch_articles_from_rss()
ai_articles = []

for title, url in articles:
    if len(ai_articles) >= MAX_ARTICLES:
        break
    print(f"🔗 {title}")
    text, image_url = extract_article_content(url)
    if not text or not is_ai_related(title + " " + text):
        continue
    ai_articles.append((title, url, image_url))
    time.sleep(2)

summaries = []
for title, url, image_url in ai_articles:
    print(f"🧠 Summarizing: {title}")
    summary = get_rundown_summary(title, text, url)
    if image_url:
        summary = f"![thumbnail]({image_url})\n\n" + summary
    summaries.append(summary)
    time.sleep(3)

intro = get_intro_section(ai_articles)
output_path = save_newsletter_markdown(intro, summaries)
