"""
BART-CNN based summarization utilities for GitHub Actions
Uses facebook/bart-large-cnn for high-quality, free AI newsletter generation
Optimized specifically for news summarization
"""
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional
import torch
from transformers import BartForConditionalGeneration, BartTokenizer
from config import CATEGORIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BartNewsletterSummarizer:
    """
    BART-CNN based summarizer optimized for news content
    Perfect for AI newsletter generation with editorial quality
    """
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🤖 Initializing BART summarizer with device: {self.device}")
        
    def load_model(self):
        """Load BART model and tokenizer with memory optimization"""
        if self.model is not None:
            return  # Already loaded
            
        try:
            logger.info(f"📥 Loading {self.model_name}...")
            
            # Load tokenizer
            self.tokenizer = BartTokenizer.from_pretrained(self.model_name)
            
            # Load model with memory optimization
            self.model = BartForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            logger.info(f"✅ BART model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load BART model: {e}")
            raise
    
    def summarize_text(self, text: str, max_length: int = 200, min_length: int = 50) -> str:
        """Generate summary using BART's native summarization capabilities"""
        if self.model is None:
            self.load_model()
        
        try:
            # Tokenize input
            inputs = self.tokenizer.encode(
                text, 
                return_tensors="pt", 
                max_length=1024, 
                truncation=True
            ).to(self.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True,
                    do_sample=False
                )
            
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary.strip()
            
        except Exception as e:
            logger.error(f"❌ BART summarization failed: {e}")
            return None
    
    def get_editorial_summary(self, article: Dict) -> str:
        """Generate editorial-style summary using BART's summarization + formatting"""
        category = article.get('category', 'misc')
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        # First, get a high-quality summary from BART
        article_text = article['text'][:2000]  # Use more text for better context
        base_summary = self.summarize_text(article_text, max_length=150, min_length=50)
        
        if not base_summary:
            return None
        
        # Create editorial structure around the BART summary
        title = article['title']
        
        # Extract key points from the summary
        sentences = base_summary.split('. ')
        
        # Create compelling headline (truncate title if too long)
        headline = title[:55] + "..." if len(title) > 55 else title
        
        # Build editorial format
        summary = f"""## {category_config['emoji']} **{headline}**

**The Rundown:** {sentences[0] if sentences else base_summary[:100]}

"""
        
        # Add bullet points from remaining sentences
        if len(sentences) > 1:
            for i, sentence in enumerate(sentences[1:4]):  # Up to 3 bullet points
                if sentence.strip():
                    summary += f"• {sentence.strip()}\n"
        else:
            # If only one sentence, create bullet points from key phrases
            summary += f"• {base_summary[:80]}...\n"
            summary += f"• Key development in {category_config['title'].lower()}\n"
        
        # Add "Why it matters" section
        summary += f"""
**Why it matters:** This development in {category_config['title'].lower()} represents a significant advancement for AI developers and researchers. The implications could reshape how we approach {category.replace('-', ' ')} in the AI ecosystem.

[👉 Read more]({article['url']})

---"""
        
        return summary
    
    def get_editors_take(self, article: Dict) -> Optional[str]:
        """Generate Editor's Take using BART summarization"""
        if article.get('popularity_score', 0) < 50:
            return None
        
        # Use BART to create a concise, insightful take
        article_text = article['text'][:1500]
        take = self.summarize_text(
            f"Editorial analysis: {article_text}", 
            max_length=80, 
            min_length=30
        )
        
        if take:
            # Add editorial voice
            take = f"Editor's Take: {take}"
        
        return take
    
    def generate_newsletter_intro(self, articles: List[Dict]) -> str:
        """Generate newsletter introduction using article summaries"""
        # Get top categories
        categories = {}
        for article in articles:
            cat = article.get('category', 'misc')
            categories[cat] = categories.get(cat, 0) + 1
        
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Create intro text for BART to summarize
        intro_text = f"""Today's AI newsletter covers {len(articles)} key developments across {len(categories)} categories. 
        
Main focus areas: {', '.join([CATEGORIES[cat]['title'] for cat, _ in top_categories])}. 
        
Top stories include: {'. '.join([article['title'] for article in articles[:3]])}.
        
These developments represent significant advances in artificial intelligence, machine learning, and related technologies that will impact developers, founders, and researchers."""
        
        # Use BART to create a polished intro
        intro = self.summarize_text(intro_text, max_length=120, min_length=60)
        
        if not intro:
            # Fallback intro
            intro = f"Today's AI digest highlights {len(articles)} key developments across {', '.join([CATEGORIES[cat]['title'] for cat, _ in top_categories[:2]])} and more. From breakthrough research to industry moves, here's what's shaping the AI landscape today."
        
        return intro
    
    def summarize_articles(self, articles: List[Dict], style: str = "editorial") -> tuple:
        """Summarize articles using BART"""
        summaries = []
        editors_takes = []
        
        # Load model once for all summaries
        self.load_model()
        
        for i, article in enumerate(articles):
            try:
                logger.info(f"📝 Processing article {i+1}/{len(articles)}: {article['title'][:50]}...")
                
                # Generate summary
                if style == "editorial":
                    summary = self.get_editorial_summary(article)
                else:
                    summary = self.get_basic_summary(article)
                
                if summary:
                    summaries.append(summary)
                    
                    # Generate Editor's Take for high-impact stories
                    editors_take = self.get_editors_take(article)
                    if editors_take:
                        editors_takes.append({
                            'title': article['title'],
                            'take': editors_take
                        })
                
                # Small delay to prevent overwhelming the system
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"❌ Error summarizing article {article.get('title', 'Unknown')}: {e}")
                continue
        
        logger.info(f"✅ Generated {len(summaries)} summaries and {len(editors_takes)} editor's takes")
        return summaries, editors_takes
    
    def get_basic_summary(self, article: Dict) -> str:
        """Generate basic summary using BART"""
        base_summary = self.summarize_text(article['text'][:2000], max_length=120, min_length=40)
        
        if not base_summary:
            return None
        
        summary = f"""**{article['title']}**

{base_summary}

**Why it matters:** This development has significant implications for the AI community and could influence future research and applications.

[Read more]({article['url']})"""
        
        return summary
    
    def generate_newsletter_content(self, articles: List[Dict], style: str = "editorial") -> Dict:
        """Generate complete newsletter content using BART"""
        logger.info("🚀 Starting BART-based newsletter generation...")
        
        # Generate introduction
        intro = self.generate_newsletter_intro(articles)
        
        # Generate summaries
        summaries, editors_takes = self.summarize_articles(articles, style)
        
        # Organize by category
        categorized_summaries = {}
        for i, article in enumerate(articles):
            if i < len(summaries):
                category = article.get('category', 'misc')
                if category not in categorized_summaries:
                    categorized_summaries[category] = []
                categorized_summaries[category].append(summaries[i])
        
        result = {
            'intro': intro,
            'summaries': summaries,
            'categorized_summaries': categorized_summaries,
            'editors_takes': editors_takes,
            'articles': articles,
            'generation_info': {
                'llm_used': f'bart-{self.model_name}',
                'timestamp': datetime.now().isoformat(),
                'total_articles': len(articles),
                'categories': list(categorized_summaries.keys()),
                'device': self.device
            }
        }
        
        logger.info("🎉 BART-based newsletter generation completed!")
        return result


# Global instance for reuse
_bart_summarizer_instance = None

def get_bart_summarizer():
    """Get or create the global BART summarizer instance"""
    global _bart_summarizer_instance
    if _bart_summarizer_instance is None:
        _bart_summarizer_instance = BartNewsletterSummarizer()
    return _bart_summarizer_instance
