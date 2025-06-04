#!/usr/bin/env python3
"""
Simulate GitHub Actions environment to test the newsletter generation
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulate GitHub Actions environment
os.environ['GITHUB_ACTIONS'] = 'true'
os.environ['GITHUB_WORKFLOW'] = 'AI Newsletter Daily Scheduler'
os.environ['GITHUB_RUN_ID'] = '15401398050'

def test_full_newsletter_generation():
    """Test full newsletter generation process"""
    try:
        from enhanced_newsletter_generator import generate_enhanced_newsletter
        
        logger.info("🧪 Testing full newsletter generation in simulated GitHub Actions...")
        
        # Generate newsletter with minimal articles for testing
        result = generate_enhanced_newsletter(
            max_articles=3,  # Small number for testing
            style="editorial",
            save_files=False,  # Don't save files for test
            fetch_images=False  # Skip images for speed
        )
        
        if result:
            logger.info("✅ Newsletter generation successful!")
            
            # Check content
            content = result.get('content', {})
            summaries = content.get('summaries', [])
            intro = content.get('intro', '')
            
            logger.info(f"📊 Generated {len(summaries)} summaries")
            logger.info(f"📝 Intro length: {len(intro)} characters")
            
            if summaries and intro:
                logger.info("✅ Content generation test PASSED")
                return True
            else:
                logger.error("❌ Content generation test FAILED - missing content")
                return False
        else:
            logger.error("❌ Newsletter generation returned None")
            return False
            
    except Exception as e:
        logger.error(f"❌ Newsletter generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_summarizer_with_multiple_articles():
    """Test summarizer with multiple articles"""
    try:
        from utils.enhanced_summarizer import EnhancedSummarizer
        
        logger.info("🧪 Testing summarizer with multiple articles...")
        
        summarizer = EnhancedSummarizer()
        
        # Test articles
        test_articles = [
            {
                'title': 'OpenAI Releases GPT-5 with Revolutionary Capabilities',
                'url': 'https://example.com/gpt5',
                'text': 'OpenAI has announced the release of GPT-5, featuring unprecedented language understanding and reasoning capabilities. The new model shows significant improvements in mathematical reasoning, code generation, and multimodal understanding.',
                'category': 'tools'
            },
            {
                'title': 'New Research Shows AI Can Predict Protein Folding with 99% Accuracy',
                'url': 'https://example.com/protein',
                'text': 'Researchers at DeepMind have developed an AI system that can predict protein folding structures with 99% accuracy, potentially revolutionizing drug discovery and biological research.',
                'category': 'research'
            },
            {
                'title': 'Microsoft Acquires AI Startup for $2.1 Billion',
                'url': 'https://example.com/acquisition',
                'text': 'Microsoft has acquired an AI startup specializing in enterprise automation for $2.1 billion, marking the largest AI acquisition this year.',
                'category': 'industry'
            }
        ]
        
        # Generate content
        content = summarizer.generate_newsletter_content(test_articles, style="editorial")
        
        if content:
            summaries = content.get('summaries', [])
            intro = content.get('intro', '')
            
            logger.info(f"✅ Generated {len(summaries)} summaries")
            logger.info(f"✅ Generated intro: {len(intro)} characters")
            
            if len(summaries) == len(test_articles) and intro:
                logger.info("✅ Multi-article summarization test PASSED")
                return True
            else:
                logger.error(f"❌ Expected {len(test_articles)} summaries, got {len(summaries)}")
                return False
        else:
            logger.error("❌ Content generation returned None")
            return False
            
    except Exception as e:
        logger.error(f"❌ Multi-article test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Run GitHub Actions simulation tests"""
    logger.info("🚀 Starting GitHub Actions simulation tests...")
    logger.info(f"🔧 Environment: GITHUB_ACTIONS={os.getenv('GITHUB_ACTIONS')}")
    logger.info(f"🔧 Workflow: {os.getenv('GITHUB_WORKFLOW')}")
    
    tests = [
        ("Multi-Article Summarizer Test", test_summarizer_with_multiple_articles),
        ("Full Newsletter Generation Test", test_full_newsletter_generation)
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"🔍 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"💥 {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    logger.info(f"\n📊 GitHub Actions Simulation Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All GitHub Actions simulation tests passed!")
        logger.info("✅ The newsletter should work correctly in GitHub Actions")
        return True
    else:
        logger.error("❌ Some GitHub Actions simulation tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
