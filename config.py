"""
Centralized configuration for AI Newsletter Generator
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# === RSS FEEDS ===
RSS_FEEDS = [
    "https://www.theverge.com/rss/index.xml",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.technologyreview.com/feed/"
]

# === LLM CONFIGURATION ===
LLM_API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_K_M"

# === AI CONTENT FILTERING ===
AI_KEYWORDS = [
    "AI", "artificial intelligence", "machine learning", "LLM", "GPT", 
    "OpenAI", "Anthropic", "deep learning", "neural", "chatbot", "Claude",
    "transformer", "generative AI", "large language model", "computer vision",
    "natural language processing", "NLP", "automation", "robotics"
]

# === NEWSLETTER SETTINGS ===
MAX_ARTICLES = 3
ARTICLES_PER_FEED = 5
DELAY_BETWEEN_REQUESTS = 2  # seconds
DELAY_BETWEEN_SUMMARIES = 3  # seconds

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
