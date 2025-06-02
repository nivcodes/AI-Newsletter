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
    
    def generate_text(self, prompt: str, max_length: int = 200, temperature: float = 0.7) -> str:
        """Generate text using BART (compatibility method for enhanced_summarizer)"""
        # For BART, we'll use the prompt as input text and summarize it
        return self.summarize_text(prompt, max_length=max_length, min_length=max_length//4)
    
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
        """Generate editorial-style summary using BART's summarization + proper formatting"""
        category = article.get('category', 'misc')
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        # Get a clean summary from BART (no prompts, just the article text)
        article_text = article['text'][:2000]
        base_summary = self.summarize_text(article_text, max_length=120, min_length=40)
        
        if not base_summary:
            return None
        
        # Clean up the summary (remove any prompt artifacts)
        base_summary = base_summary.replace('You are the editor', '').replace('Write like a sharp', '').strip()
        
        # Create editorial structure
        title = article['title']
        headline = title[:55] + "..." if len(title) > 55 else title
        
        # Split summary into sentences for bullet points
        sentences = [s.strip() for s in base_summary.split('.') if s.strip()]
        
        # Build the editorial format
        summary = f"""## {category_config['emoji']} **{headline}**

**The Rundown:** {sentences[0] if sentences else base_summary[:100]}.

"""
        
        # Create bullet points from key information
        if len(sentences) > 1:
            for sentence in sentences[1:4]:  # Up to 3 more sentences as bullets
                if sentence and len(sentence) > 10:  # Only meaningful sentences
                    summary += f"• {sentence}.\n"
        
        # Add contextual bullet if we don't have enough
        if len(sentences) <= 2:
            summary += f"• Significant development in {category_config['title'].lower()}\n"
        
        # Create a meaningful "Why it matters" based on category
        why_matters = self._get_why_it_matters(category, article['title'])
        
        summary += f"""
**Why it matters:** {why_matters}

[👉 Read more]({article['url']})

---"""
        
        return summary
    
    def _get_why_it_matters(self, category: str, title: str) -> str:
        """Generate contextual 'why it matters' based on category and title"""
        category_insights = {
            'research': "This research could influence future AI model development and provide insights for developers building next-generation applications.",
            'tools': "This tool development could streamline AI workflows and provide new capabilities for developers and researchers in their projects.",
            'industry': "This industry move signals broader market trends that could impact AI funding, partnerships, and strategic decisions for founders and companies.",
            'use-case': "This application demonstrates practical AI implementation strategies that developers can adapt for their own use cases.",
            'misc': "This development highlights emerging trends in the AI ecosystem that could influence future technology decisions."
        }
        
        base_insight = category_insights.get(category, category_insights['misc'])
        
        # Add specific context based on title keywords
        if any(word in title.lower() for word in ['funding', 'investment', 'raises']):
            base_insight += " The funding landscape provides signals about which AI approaches investors see as most promising."
        elif any(word in title.lower() for word in ['open source', 'open-source']):
            base_insight += " Open source developments often accelerate innovation and provide accessible alternatives for developers."
        elif any(word in title.lower() for word in ['model', 'llm', 'ai']):
            base_insight += " Model improvements directly impact the capabilities available to AI practitioners and researchers."
        
        return base_insight
    
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
        """Generate clean newsletter introduction"""
        # Get top categories
        categories = {}
        for article in articles:
            cat = article.get('category', 'misc')
            categories[cat] = categories.get(cat, 0) + 1
        
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Create a clean, professional intro without using BART (to avoid prompt artifacts)
        category_names = [CATEGORIES[cat]['title'] for cat, _ in top_categories]
        
        # Build intro based on the day's content
        if len(articles) >= 8:
            intensity = "packed"
        elif len(articles) >= 5:
            intensity = "busy"
        else:
            intensity = "focused"
        
        intro = f"""It's a {intensity} day in AI with {len(articles)} key developments spanning {', '.join(category_names[:2])}{',' if len(category_names) > 2 else ' and'} {category_names[-1] if len(category_names) > 2 else ''}.

From {self._get_intro_theme(articles)} to {self._get_secondary_theme(articles)}, today's digest captures the moves shaping AI's trajectory. Here's what developers, founders, and researchers need to know."""
        
        return intro
    
    def _get_intro_theme(self, articles: List[Dict]) -> str:
        """Get primary theme for intro based on articles"""
        # Look for common themes in titles
        titles_text = ' '.join([article['title'].lower() for article in articles[:5]])
        
        if any(word in titles_text for word in ['funding', 'raises', 'investment']):
            return "major funding rounds"
        elif any(word in titles_text for word in ['model', 'llm', 'gpt']):
            return "breakthrough model releases"
        elif any(word in titles_text for word in ['tool', 'api', 'platform']):
            return "new developer tools"
        elif any(word in titles_text for word in ['research', 'study', 'paper']):
            return "cutting-edge research"
        else:
            return "industry developments"
    
    def _get_secondary_theme(self, articles: List[Dict]) -> str:
        """Get secondary theme for intro"""
        titles_text = ' '.join([article['title'].lower() for article in articles])
        
        if any(word in titles_text for word in ['partnership', 'acquisition', 'deal']):
            return "strategic partnerships"
        elif any(word in titles_text for word in ['open source', 'open-source']):
            return "open source innovations"
        elif any(word in titles_text for word in ['regulation', 'policy', 'government']):
            return "policy developments"
        else:
            return "technical breakthroughs"
    
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
