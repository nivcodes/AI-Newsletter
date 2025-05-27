import feedparser
from newspaper import Article
import requests
import time

# === CONFIG ===
RSS_FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/feed/"
]

LLM_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_K_M"  # Replace with your model name


# === FUNCTIONS ===

def fetch_articles_from_rss():
    print("🔍 Fetching articles...")
    articles = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:3]:  # Limit for demo
            articles.append((entry.title, entry.link))
    return articles


def extract_full_text(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"❌ Failed to extract: {url} ({e})")
        return None


def summarize_with_local_llm(title, text, url):
    prompt = f"""
You are a smart but punchy AI news editor writing for a tech-savvy audience.

Summarize the following article for a newsletter in this format:

1. 🔥 **Headline**: A short, catchy 1-liner that's truthful and clicky
2. 🧠 **Tagline**: A 1-sentence teaser that makes readers want to know more
3. ✍️ **Summary**: 2–4 sentence digest of the article’s core info and implications
4. 🔗 **Link**: Include this exact markdown format: [Read more]({url})

Title: {title}

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


from datetime import datetime

def save_newsletter_markdown(summaries):
    date = datetime.today().strftime('%B %d, %Y')
    header = f"# 🗞️ AI News Digest\n**{date}**\n\n---\n"
    body = "\n\n---\n\n".join(summaries)

    with open("newsletter.md", "w") as f:
        f.write(header + body)

    print("✅ Markdown newsletter saved as: newsletter.md")


def save_newsletter_html(summaries):
    html_blocks = []
    for item in summaries:
        title, url, summary = item
        html_blocks.append(f"""
        <div class="article">
            <h2><a href="{url}">{title}</a></h2>
            <div class="summary-section">
                {summary.replace('\n', '<br>')}
            </div>
        </div>
        """)

    full_html = open("newsletter_template.html").read()
    full_html = full_html.replace("{{date}}", datetime.today().strftime('%B %d, %Y'))
    full_html = full_html.replace("{{content}}", "\n".join(html_blocks))

    with open("newsletter.html", "w") as f:
        f.write(full_html)

    print("✅ Newsletter saved as: newsletter.html")



def main():
    articles = fetch_articles_from_rss()
    summaries = []
    for title, url in articles:
        print(f"\n🔗 {title}\nURL: {url}")
        text = extract_full_text(url)
        if not text:
            continue

        print("🧠 Summarizing...")
        summary = summarize_with_local_llm(title, text, url)
        summaries.append(summary)
        time.sleep(3)

    save_newsletter_markdown(summaries)



if __name__ == "__main__":
    main()
