"""
Hugging Face Transformer-based summarization utilities for GitHub Actions
Uses FLAN-T5-Large for high-quality, free AI newsletter generation
"""
import logging
import time
from datetime import datetime
from typing import List, Dict, Optional
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
from config import CATEGORIES

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HuggingFaceTransformerSummarizer:
    """
    Free transformer-based summarizer using FLAN-T5-Large
    Optimized for GitHub Actions with caching and memory management
    """
    
    def __init__(self, model_name="google/flan-t5-large"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        logger.info(f"🤖 Initializing transformer summarizer with device: {self.device}")
        
    def load_model(self):
        """Load the model and tokenizer with memory optimization"""
        if self.model is not None:
            return  # Already loaded
            
        try:
            logger.info(f"📥 Loading {self.model_name}...")
            
            # Load tokenizer
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            
            # Load model with memory optimization
            self.model = T5ForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            logger.info(f"✅ Model loaded successfully on {self.device}")
            
        except Exception as e:
            logger.error(f"❌ Failed to load model: {e}")
            raise
    
    def generate_text(self, prompt: str, max_length: int = 512, temperature: float = 0.7) -> str:
        """Generate text using the loaded model"""
        if self.model is None:
            self.load_model()
        
        try:
            # Tokenize input
            inputs = self.tokenizer.encode(
                prompt, 
                return_tensors="pt", 
                max_length=512, 
                truncation=True
            ).to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    temperature=temperature,
                    do_sample=True,
                    top_p=0.9,
                    pad_token_id=self.tokenizer.eos_token_id,
                    num_return_sequences=1
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response.strip()
            
        except Exception as e:
            logger.error(f"❌ Text generation failed: {e}")
            return None
    
    def get_editorial_summary(self, article: Dict) -> str:
        """Generate editorial-style summary optimized for FLAN-T5"""
        category = article.get('category', 'misc')
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        # Optimized prompt for FLAN-T5's instruction-following capabilities
        prompt = f"""Write a newsletter summary for tech professionals about this AI article.

Article: {article['title']}
Category: {category_config['title']}
Content: {article['text'][:1500]}

Format your response exactly like this:

## {category_config['emoji']} **[Write a compelling 50-character headline]**

**The Rundown:** [One punchy sentence summarizing the key development]

• [First key point with specific detail]
• [Second key point with impact/implication]
• [Third key point with context/significance]

**Why it matters:** [2-3 sentences explaining why AI developers and founders should care about this. Focus on practical implications.]

Requirements:
- Write like a knowledgeable tech editor
- Use specific numbers/metrics when available
- Be direct and insightful, avoid marketing fluff
- Focus on practical significance for professionals
"""
        
        logger.info(f"🧠 Generating editorial summary for: {article['title'][:50]}...")
        summary = self.generate_text(prompt, max_length=400, temperature=0.7)
        
        if summary:
            # Add the read more link
            summary += f"\n\n[👉 Read more]({article['url']})\n\n---"
        
        return summary
    
    def get_editors_take(self, article: Dict) -> Optional[str]:
        """Generate Editor's Take for high-impact stories"""
        if article.get('popularity_score', 0) < 50:
            return None
        
        prompt = f"""Write a brief "Editor's Take" about this major AI development.

Article: {article['title']}
Content: {article['text'][:1200]}

Write 2-3 sentences that provide:
1. Your informed opinion on what this really means
2. A prediction or implication others might miss  
3. Context about why this matters in the AI landscape

Style: Confident, insightful, slightly provocative. Like a smart industry analyst's hot take.

Write only the take itself, no headers or extra formatting."""
        
        logger.info(f"✍️ Generating Editor's Take for: {article['title'][:50]}...")
        take = self.generate_text(prompt, max_length=200, temperature=0.8)
        
        return take
    
    def generate_newsletter_intro(self, articles: List[Dict]) -> str:
        """Generate compelling newsletter introduction"""
        # Get top categories
        categories = {}
        for article in articles:
            cat = article.get('category', 'misc')
            categories[cat] = categories.get(cat, 0) + 1
        
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        top_titles = [article['title'] for article in articles[:5]]
        
        prompt = f"""Write an engaging introduction for an AI newsletter read by developers, founders, and researchers.

Today's coverage includes:
{chr(10).join([f"• {CATEGORIES[cat]['title']}: {count} stories" for cat, count in top_categories])}

Top headlines:
{chr(10).join([f"• {title}" for title in top_titles])}

Write a compelling 2-paragraph introduction (under 150 words) that:
1. Sets an energetic, insightful tone for today's digest
2. Highlights key themes emerging from today's stories
3. Makes readers excited to dive into the content

Style: Conversational but authoritative, forward-looking, analytical. Sound like a human curator who deeply understands AI trends.

Avoid generic phrases like "in today's newsletter" or "we cover". Be specific about what's happening in AI today."""
        
        logger.info("✍️ Generating newsletter introduction...")
        intro = self.generate_text(prompt, max_length=300, temperature=0.6)
        
        return intro
    
    def summarize_articles(self, articles: List[Dict], style: str = "editorial") -> tuple:
        """Summarize a list of articles with editorial style"""
        summaries = []
        editors_takes = []
        
        # Load model once for all summaries
        self.load_model()
        
        for i, article in enumerate(articles):
            try:
                logger.info(f"📝 Processing article {i+1}/{len(articles)}")
                
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
        """Generate basic summary (fallback)"""
        prompt = f"""Summarize this AI article for a tech newsletter:

Title: {article['title']}
Content: {article['text'][:1500]}

Write a clear summary with:
- **Bold title**
- 2-3 sentences covering key points and implications
- **Why it matters:** section explaining significance for AI community

Keep it concise and professional."""
        
        summary = self.generate_text(prompt, max_length=300, temperature=0.7)
        
        if summary:
            summary += f"\n\n[Read more]({article['url']})"
        
        return summary
    
    def generate_newsletter_content(self, articles: List[Dict], style: str = "editorial") -> Dict:
        """Generate complete newsletter content"""
        logger.info("🚀 Starting transformer-based newsletter generation...")
        
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
                'llm_used': f'transformer-{self.model_name}',
                'timestamp': datetime.now().isoformat(),
                'total_articles': len(articles),
                'categories': list(categorized_summaries.keys()),
                'device': self.device
            }
        }
        
        logger.info("🎉 Transformer-based newsletter generation completed!")
        return result


# Global instance for reuse
_summarizer_instance = None

def get_summarizer():
    """Get or create the global summarizer instance"""
    global _summarizer_instance
    if _summarizer_instance is None:
        _summarizer_instance = HuggingFaceTransformerSummarizer()
    return _summarizer_instance


# Main functions for backward compatibility
def generate_newsletter_content(articles: List[Dict], style: str = "editorial") -> Dict:
    """Main function to generate newsletter content using transformers"""
    summarizer = get_summarizer()
    return summarizer.generate_newsletter_content(articles, style)

def get_rundown_summary(article: Dict) -> str:
    """Backward compatibility function"""
    summarizer = get_summarizer()
    return summarizer.get_editorial_summary(article)

def get_basic_summary(article: Dict) -> str:
    """Backward compatibility function"""
    summarizer = get_summarizer()
    return summarizer.get_basic_summary(article)
