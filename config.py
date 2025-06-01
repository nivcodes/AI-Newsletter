"""
Centralized configuration for AI Newsletter Generator
Enhanced for curated daily digest with multiple sources and categorization
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === ENHANCED DATA SOURCES ===
RSS_FEEDS = {
    'research': [
        "https://rss.arxiv.org/rss/cs.AI",
        "https://rss.arxiv.org/rss/cs.LG", 
        "https://rss.arxiv.org/rss/cs.CL",
        "https://ai.googleblog.com/feeds/posts/default",
        "https://www.microsoft.com/en-us/research/feed/"
    ],
    'tools': [
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/news/rss.xml",
        "https://blog.langchain.dev/rss.xml",
        "https://huggingface.co/blog/feed.xml"
    ],
    'industry': [
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        "https://venturebeat.com/category/ai/feed/",
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "https://www.technologyreview.com/feed/"
    ],
    'misc': [
        "https://www.theverge.com/rss/index.xml",
        "https://spectrum.ieee.org/rss/fulltext",
        "https://www.wired.com/feed/tag/ai/latest/rss"
    ]
}

# === API ENDPOINTS ===
API_SOURCES = {
    'hackernews': 'https://hacker-news.firebaseio.com/v0',
    'reddit': 'https://www.reddit.com/r/MachineLearning/hot.json',
    'papers_with_code': 'https://paperswithcode.com/api/v1/papers/',
    'arxiv': 'http://export.arxiv.org/api/query'
}

# === LLM CONFIGURATION ===
# Local LLM (fallback)
LLM_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_K_M"

# External LLM APIs (optional - now using free transformers by default)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
USE_EXTERNAL_LLM = os.getenv("USE_EXTERNAL_LLM", "false").lower() == "true"
PREFERRED_LLM = os.getenv("PREFERRED_LLM", "transformer")  # transformer, local, openai, anthropic

# Transformer Model Configuration (free alternative)
USE_TRANSFORMER = os.getenv("USE_TRANSFORMER", "true").lower() == "true"
TRANSFORMER_MODEL = os.getenv("TRANSFORMER_MODEL", "google/flan-t5-large")

# === ENHANCED AI CONTENT FILTERING ===
AI_KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "LLM", "GPT", 
    "OpenAI", "Anthropic", "deep learning", "neural", "chatbot", "Claude",
    "transformer", "generative AI", "large language model", "computer vision",
    "natural language processing", "NLP", "automation", "robotics", "AGI",
    "foundation model", "multimodal", "diffusion", "stable diffusion",
    "midjourney", "dall-e", "gpt-4", "claude-3", "gemini", "llama",
    "hugging face", "langchain", "vector database", "embedding", "RAG",
    "fine-tuning", "prompt engineering", "agents", "autonomous", "reasoning"
]

# === HIGH-IMPACT KEYWORDS FOR SCORING ===
HIGH_IMPACT_KEYWORDS = [
    "launch", "launches", "released", "open-source", "open source", 
    "benchmark", "outperforms", "breakthrough", "state-of-the-art",
    "SOTA", "beats", "surpasses", "record", "first", "new model",
    "funding", "acquisition", "partnership", "integration", "API",
    "agents", "autonomous", "reasoning", "planning", "multimodal"
]

# === ARTICLE CATEGORIES ===
CATEGORIES = {
    'research': {
        'keywords': ['arxiv', 'paper', 'research', 'study', 'analysis', 'benchmark', 'dataset'],
        'sources': ['arxiv.org', 'ai.googleblog.com', 'research.microsoft.com'],
        'emoji': '🧠',
        'title': 'Research & Models'
    },
    'tools': {
        'keywords': ['api', 'tool', 'library', 'framework', 'sdk', 'platform', 'service'],
        'sources': ['openai.com', 'anthropic.com', 'langchain.dev', 'huggingface.co'],
        'emoji': '⚙️',
        'title': 'Tools & APIs'
    },
    'industry': {
        'keywords': ['funding', 'acquisition', 'partnership', 'company', 'startup', 'investment'],
        'sources': ['techcrunch.com', 'venturebeat.com', 'theverge.com'],
        'emoji': '📢',
        'title': 'Industry News'
    },
    'use-case': {
        'keywords': ['implementation', 'case study', 'application', 'deployment', 'real-world'],
        'sources': [],
        'emoji': '🎯',
        'title': 'Use Cases'
    },
    'misc': {
        'keywords': ['opinion', 'analysis', 'tutorial', 'guide', 'interview'],
        'sources': [],
        'emoji': '🧵',
        'title': 'Quick Hits'
    }
}

# === NEWSLETTER SETTINGS ===
MAX_ARTICLES = 12  # Increased for better curation
MAX_ARTICLES_PER_CATEGORY = 3
ARTICLES_PER_FEED = 10  # Increased to get more options
DELAY_BETWEEN_REQUESTS = 1  # Reduced for faster processing
DELAY_BETWEEN_SUMMARIES = 2  # Reduced for faster processing
MIN_ARTICLE_LENGTH = 200  # Minimum article length in characters
MAX_ARTICLE_AGE_HOURS = 48  # Only include articles from last 48 hours

# === EMAIL CONFIGURATION ===
EMAIL_CONFIG = {
    'from_email': os.getenv("EMAIL_FROM"),
    'to_email': os.getenv("EMAIL_TO"),
    'smtp_server': os.getenv("SMTP_SERVER"),
    'smtp_port': int(os.getenv("SMTP_PORT", 465)),
    'smtp_user': os.getenv("EMAIL_USER"),
    'smtp_password': os.getenv("EMAIL_PASSWORD")
}

# === OUTPUT PATHS ===
OUTPUT_DIR = "output"
NEWSLETTER_MD = f"{OUTPUT_DIR}/newsletter.md"
NEWSLETTER_HTML = f"{OUTPUT_DIR}/newsletter.html"
NEWSLETTER_STYLED = f"{OUTPUT_DIR}/newsletter_styled.html"

# === TEMPLATES ===
TEMPLATE_DIR = "templates"
NEWSLETTER_TEMPLATE = f"{TEMPLATE_DIR}/newsletter_template.html"
