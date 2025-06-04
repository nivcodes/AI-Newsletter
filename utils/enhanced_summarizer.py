"""
Enhanced LLM summarization utilities with external API support and editorial prompts
"""
import os
import requests
import time
import logging
from datetime import datetime
from config import (
    LLM_API_URL, MODEL_NAME, DELAY_BETWEEN_SUMMARIES,
    OPENAI_API_KEY, ANTHROPIC_API_KEY, USE_EXTERNAL_LLM, PREFERRED_LLM,
    USE_TRANSFORMER, TRANSFORMER_MODEL, CATEGORIES,
    AWS_REGION, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, 
    AWS_BEDROCK_MODEL_ID, USE_AWS_BEDROCK
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import external LLM libraries if available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI library not available. Install with: pip install openai")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic library not available. Install with: pip install anthropic")

try:
    import boto3
    AWS_BEDROCK_AVAILABLE = True
except ImportError:
    AWS_BEDROCK_AVAILABLE = False
    logger.warning("AWS boto3 library not available. Install with: pip install boto3")


class EnhancedSummarizer:
    """Enhanced summarizer with multiple LLM backends and editorial prompts"""
    
    def __init__(self):
        self.setup_llm_clients()
    
    def setup_llm_clients(self):
        """Initialize LLM clients based on configuration"""
        self.openai_client = None
        self.anthropic_client = None
        self.bedrock_client = None
        
        if OPENAI_AVAILABLE and OPENAI_API_KEY:
            try:
                self.openai_client = openai.OpenAI(api_key=OPENAI_API_KEY)
                logger.info("✅ OpenAI client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
        
        if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
                logger.info("✅ Anthropic client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic client: {e}")
        
        if AWS_BEDROCK_AVAILABLE and USE_AWS_BEDROCK:
            try:
                if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY:
                    self.bedrock_client = boto3.client(
                        'bedrock-runtime',
                        region_name=AWS_REGION,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
                    )
                else:
                    # Use default AWS credentials (IAM role, profile, etc.)
                    self.bedrock_client = boto3.client(
                        'bedrock-runtime',
                        region_name=AWS_REGION
                    )
                logger.info("✅ AWS Bedrock client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize AWS Bedrock client: {e}")
    
    def call_local_llm(self, prompt, temperature=0.7):
        """Call local LLM API (fallback)"""
        try:
            data = {
                "model": MODEL_NAME,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temperature
            }
            
            response = requests.post(LLM_API_URL, json=data, timeout=30)
            response.raise_for_status()
            
            return response.json()['choices'][0]['message']['content']
            
        except Exception as e:
            logger.error(f"Local LLM API call failed: {e}")
            return None
    
    def call_openai(self, prompt, temperature=0.7, model="gpt-4"):
        """Call OpenAI API"""
        if not self.openai_client:
            return None
        
        try:
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}")
            return None
    
    def call_anthropic(self, prompt, temperature=0.7, model="claude-3-sonnet-20240229"):
        """Call Anthropic API"""
        if not self.anthropic_client:
            return None
        
        try:
            response = self.anthropic_client.messages.create(
                model=model,
                max_tokens=1000,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Anthropic API call failed: {e}")
            return None
    
    def call_aws_bedrock(self, prompt, temperature=0.7, model_id=None):
        """Call AWS Bedrock API for Anthropic Claude"""
        if not self.bedrock_client:
            return None
        
        try:
            import json
            
            model_id = model_id or AWS_BEDROCK_MODEL_ID
            
            # Format request for Anthropic Claude via Bedrock
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "temperature": temperature,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=model_id,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
            
        except Exception as e:
            logger.error(f"AWS Bedrock API call failed: {e}")
            return None
    
    def call_best_available_llm(self, prompt, temperature=0.7):
        """Call the best available LLM based on configuration"""
        # Debug configuration
        logger.info(f"🔧 Configuration: USE_TRANSFORMER={USE_TRANSFORMER}, PREFERRED_LLM={PREFERRED_LLM}")
        logger.info(f"🔧 External APIs: USE_EXTERNAL_LLM={USE_EXTERNAL_LLM}, USE_AWS_BEDROCK={USE_AWS_BEDROCK}")
        
        # Try preferred LLM first
        if PREFERRED_LLM == "aws-anthropic" and self.bedrock_client:
            logger.info("🤖 Using preferred AWS Bedrock (Anthropic)...")
            result = self.call_aws_bedrock(prompt, temperature)
            if result:
                logger.info("✅ AWS Bedrock generated response successfully")
                return result
            else:
                logger.warning("⚠️ AWS Bedrock failed, trying other options...")
        elif PREFERRED_LLM == "openai" and self.openai_client:
            logger.info("🤖 Using preferred OpenAI...")
            result = self.call_openai(prompt, temperature)
            if result:
                logger.info("✅ OpenAI generated response successfully")
                return result
            else:
                logger.warning("⚠️ OpenAI failed, trying other options...")
        elif PREFERRED_LLM == "anthropic" and self.anthropic_client:
            logger.info("🤖 Using preferred Anthropic...")
            result = self.call_anthropic(prompt, temperature)
            if result:
                logger.info("✅ Anthropic generated response successfully")
                return result
            else:
                logger.warning("⚠️ Anthropic failed, trying other options...")
        elif PREFERRED_LLM == "transformer" and USE_TRANSFORMER:
            logger.info("🤖 Using preferred transformer model...")
            try:
                from .transformer_summarizer import get_summarizer
                logger.info("✅ Transformer summarizer imported successfully")
                transformer_summarizer = get_summarizer()
                logger.info("✅ Transformer summarizer instance created")
                result = transformer_summarizer.generate_text(prompt, temperature=temperature)
                if result:
                    logger.info("✅ Transformer model generated response successfully")
                    return result
                else:
                    logger.warning("⚠️ Transformer model returned empty result")
            except Exception as e:
                logger.warning(f"⚠️ Transformer model failed: {e}")
                logger.info("⚠️ Falling back to external APIs...")
        
        # Try other available external APIs as fallback
        if USE_EXTERNAL_LLM or USE_AWS_BEDROCK:
            logger.info("🔄 Trying fallback external APIs...")
            
            # Try AWS Bedrock if not already tried
            if PREFERRED_LLM != "aws-anthropic" and self.bedrock_client:
                logger.info("🔄 Trying AWS Bedrock as fallback...")
                result = self.call_aws_bedrock(prompt, temperature)
                if result:
                    logger.info("✅ AWS Bedrock fallback successful")
                    return result
            
            # Try OpenAI if not already tried
            if PREFERRED_LLM != "openai" and self.openai_client:
                logger.info("🔄 Trying OpenAI as fallback...")
                result = self.call_openai(prompt, temperature)
                if result:
                    logger.info("✅ OpenAI fallback successful")
                    return result
            
            # Try Anthropic if not already tried
            if PREFERRED_LLM != "anthropic" and self.anthropic_client:
                logger.info("🔄 Trying Anthropic as fallback...")
                result = self.call_anthropic(prompt, temperature)
                if result:
                    logger.info("✅ Anthropic fallback successful")
                    return result
        
        # Try transformer as last resort if not already tried and available
        if PREFERRED_LLM != "transformer" and USE_TRANSFORMER:
            logger.info("🔄 Trying transformer model as fallback...")
            try:
                from .transformer_summarizer import get_summarizer
                transformer_summarizer = get_summarizer()
                result = transformer_summarizer.generate_text(prompt, temperature=temperature)
                if result:
                    logger.info("✅ Transformer fallback successful")
                    return result
            except Exception as e:
                logger.warning(f"⚠️ Transformer fallback failed: {e}")
        
        # Check if we're in GitHub Actions environment - avoid local LLM
        if os.getenv('GITHUB_ACTIONS') == 'true':
            logger.error("❌ All LLM options exhausted in GitHub Actions environment.")
            return None
        
        # Fallback to local LLM only if not in GitHub Actions
        logger.info("🔄 Trying local LLM as final fallback...")
        return self.call_local_llm(prompt, temperature)
    
    def get_editorial_summary(self, article):
        """Generate editorial-style summary with enhanced prompts"""
        category = article.get('category', 'misc')
        category_config = CATEGORIES.get(category, CATEGORIES['misc'])
        
        prompt = f"""
You are the editor of a premium AI newsletter read by developers, founders, and researchers. Your audience is technical but values clear, insightful analysis.

Article Details:
- Title: {article['title']}
- URL: {article['url']}
- Category: {category_config['title']}
- Popularity Score: {article.get('popularity_score', 0)}

Article Content:
{article['text'][:2000]}...

Generate a newsletter section with this EXACT structure:

## {category_config['emoji']} **[Compelling Headline - max 60 chars]**

**The Rundown:** [One punchy sentence that captures the essence]

• [Key point 1 with specific detail or number]
• [Key point 2 with impact or implication] 
• [Key point 3 with context or significance]

**Why it matters:** [2-3 sentences explaining the broader significance for AI developers, founders, or researchers. Focus on practical implications, competitive landscape, or technical advancement.]

[👉 Read more]({article['url']})

---

Style Guidelines:
- Write like a sharp, knowledgeable human editor (think Paul Graham meets Benedict Evans)
- Use specific numbers, percentages, or metrics when available
- Avoid marketing fluff - be direct and insightful
- Make technical concepts accessible but don't dumb them down
- Focus on "so what?" - why should busy professionals care?
"""
        
        logger.info(f"🧠 Generating editorial summary for: {article['title']}")
        summary = self.call_best_available_llm(prompt, temperature=0.7)
        
        # Fallback if LLM fails - create a basic summary
        if not summary:
            logger.warning(f"⚠️ LLM failed for {article['title']}, creating fallback summary")
            summary = self.create_fallback_summary(article, category_config)
        
        return summary
    
    def create_fallback_summary(self, article, category_config):
        """Create a basic fallback summary when LLM fails"""
        title = article['title']
        headline = title[:55] + "..." if len(title) > 55 else title
        
        # Extract first few sentences from article text
        text = article.get('text', '')[:500]
        sentences = [s.strip() for s in text.split('.') if s.strip() and len(s.strip()) > 20]
        
        # Create basic summary structure
        summary = f"""## {category_config['emoji']} **{headline}**

**The Rundown:** {sentences[0] if sentences else 'New development in AI technology'}.  

• Key development in {category_config['title'].lower()}
• Significant implications for the AI community
• Worth monitoring for future developments

**Why it matters:** This development represents an important advancement in the AI space that could influence future technology decisions and research directions.

[👉 Read more]({article['url']})

---"""
        
        return summary
    
    def get_editors_take(self, article):
        """Generate special 'Editor's Take' for high-impact stories"""
        if article.get('popularity_score', 0) < 50:  # Only for high-scoring articles
            return None
        
        prompt = f"""
You are a seasoned AI industry analyst writing a hot take on a major development.

Article: {article['title']}
Content: {article['text'][:1500]}...

Write a brief "Editor's Take" (2-3 sentences max) that provides:
1. Your informed opinion on what this really means
2. A prediction or implication others might miss
3. Context about why this matters in the bigger AI landscape

Style: Confident, insightful, slightly provocative. Think of a smart tweet thread condensed into a paragraph.

Format: Just the take itself, no headers or formatting.
"""
        
        logger.info(f"✍️ Generating Editor's Take for: {article['title']}")
        take = self.call_best_available_llm(prompt, temperature=0.8)
        
        return take
    
    def generate_newsletter_intro(self, articles):
        """Generate compelling newsletter introduction"""
        # Get top categories and themes
        categories = {}
        for article in articles:
            cat = article.get('category', 'misc')
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        top_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Extract key themes from titles
        titles = [article['title'] for article in articles[:5]]
        
        prompt = f"""
You are writing a crisp executive brief for a premium AI newsletter read by busy developers, founders, and researchers.

Today's top categories: {', '.join([f"{CATEGORIES[cat]['title']} ({count} stories)" for cat, count in top_categories])}

Top story headlines:
{chr(10).join([f"• {title}" for title in titles])}

Write a sharp, punchy introduction (2-3 sentences max) that:
1. Captures the day's key AI development or trend in one compelling statement
2. Sets up why these stories matter for your technical audience
3. Creates urgency to read on

Style: 
- Direct and authoritative (think Wall Street Journal meets TechCrunch)
- No fluff or generic newsletter language
- Lead with the most significant insight or trend
- Sound like a sharp industry insider

Keep it under 75 words total. Start strong.
"""
        
        logger.info("✍️ Generating newsletter introduction...")
        intro = self.call_best_available_llm(prompt, temperature=0.6)
        
        # Fallback if LLM fails
        if not intro:
            logger.warning("⚠️ LLM failed for newsletter intro, creating fallback")
            intro = self.create_fallback_intro(articles, top_categories)
        
        return intro
    
    def create_fallback_intro(self, articles, top_categories):
        """Create a basic fallback introduction when LLM fails"""
        total_articles = len(articles)
        category_names = [CATEGORIES.get(cat, {}).get('title', cat.title()) for cat, _ in top_categories[:2]]
        
        if total_articles >= 8:
            intensity = "packed"
        elif total_articles >= 5:
            intensity = "busy"
        else:
            intensity = "focused"
        
        if len(category_names) >= 2:
            categories_text = f"{category_names[0]} and {category_names[1]}"
        elif len(category_names) == 1:
            categories_text = category_names[0]
        else:
            categories_text = "AI developments"
        
        intro = f"""Today brings {total_articles} key developments in AI, with a {intensity} focus on {categories_text}. From breakthrough research to industry moves, here's what developers, founders, and researchers need to know about the latest advances shaping the AI landscape."""
        
        return intro
    
    def summarize_articles(self, articles, style="editorial"):
        """Summarize a list of articles with enhanced editorial style"""
        summaries = []
        editors_takes = []
        
        for article in articles:
            try:
                if style == "editorial":
                    summary = self.get_editorial_summary(article)
                else:
                    # Fallback to basic style for compatibility
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
                
                # Rate limiting
                time.sleep(DELAY_BETWEEN_SUMMARIES)
                
            except Exception as e:
                logger.error(f"Error summarizing article {article.get('title', 'Unknown')}: {e}")
                continue
        
        logger.info(f"✅ Generated {len(summaries)} summaries and {len(editors_takes)} editor's takes")
        return summaries, editors_takes
    
    def get_basic_summary(self, article):
        """Generate basic summary (fallback for compatibility)"""
        prompt = f"""
Summarize this AI article for a tech newsletter:

Title: {article['title']}
Content: {article['text'][:1500]}...

Format:
**{article['title']}**

[2-3 sentence summary of key points and implications]

**Why it matters:** [1-2 sentences on significance for AI community]

[Read more]({article['url']})
"""
        
        return self.call_best_available_llm(prompt, temperature=0.7)
    
    def generate_newsletter_content(self, articles, style="editorial"):
        """Generate complete newsletter content with enhanced editorial approach"""
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
        
        return {
            'intro': intro,
            'summaries': summaries,
            'categorized_summaries': categorized_summaries,
            'editors_takes': editors_takes,
            'articles': articles,
            'generation_info': {
                'llm_used': PREFERRED_LLM if USE_EXTERNAL_LLM else 'local',
                'timestamp': datetime.now().isoformat(),
                'total_articles': len(articles),
                'categories': list(categorized_summaries.keys())
            }
        }


# Main functions for backward compatibility
def generate_newsletter_content(articles, style="editorial"):
    """Enhanced main function to generate newsletter content"""
    summarizer = EnhancedSummarizer()
    return summarizer.generate_newsletter_content(articles, style)

def get_rundown_summary(article):
    """Backward compatibility function"""
    summarizer = EnhancedSummarizer()
    return summarizer.get_editorial_summary(article)

def get_basic_summary(article):
    """Backward compatibility function"""
    summarizer = EnhancedSummarizer()
    return summarizer.get_basic_summary(article)
