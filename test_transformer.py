#!/usr/bin/env python3
"""
Test script to verify transformer model functionality
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set environment variable to simulate GitHub Actions
os.environ['GITHUB_ACTIONS'] = 'true'

def test_transformer_import():
    """Test if transformer modules can be imported"""
    try:
        from utils.transformer_summarizer import get_summarizer
        logger.info("✅ Transformer summarizer imported successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to import transformer summarizer: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_transformer_instance():
    """Test if transformer instance can be created"""
    try:
        from utils.transformer_summarizer import get_summarizer
        summarizer = get_summarizer()
        logger.info("✅ Transformer summarizer instance created successfully")
        return True, summarizer
    except Exception as e:
        logger.error(f"❌ Failed to create transformer instance: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False, None

def test_simple_generation():
    """Test simple text generation"""
    try:
        from utils.transformer_summarizer import get_summarizer
        summarizer = get_summarizer()
        
        test_prompt = "Summarize this: AI technology is advancing rapidly with new models being released."
        result = summarizer.generate_text(test_prompt, temperature=0.7)
        
        if result:
            logger.info(f"✅ Text generation successful: {result[:100]}...")
            return True
        else:
            logger.error("❌ Text generation returned empty result")
            return False
    except Exception as e:
        logger.error(f"❌ Text generation failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_enhanced_summarizer():
    """Test enhanced summarizer with fallback"""
    try:
        from utils.enhanced_summarizer import EnhancedSummarizer
        
        summarizer = EnhancedSummarizer()
        
        # Test article
        test_article = {
            'title': 'Test AI Article',
            'url': 'https://example.com/test',
            'text': 'This is a test article about artificial intelligence developments. AI is making significant progress in various fields including natural language processing and computer vision.',
            'category': 'research'
        }
        
        summary = summarizer.get_editorial_summary(test_article)
        
        if summary:
            logger.info(f"✅ Enhanced summarizer successful: {summary[:100]}...")
            return True
        else:
            logger.error("❌ Enhanced summarizer returned empty result")
            return False
    except Exception as e:
        logger.error(f"❌ Enhanced summarizer failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting transformer functionality tests...")
    
    tests = [
        ("Import Test", test_transformer_import),
        ("Instance Test", lambda: test_transformer_instance()[0]),
        ("Generation Test", test_simple_generation),
        ("Enhanced Summarizer Test", test_enhanced_summarizer)
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
    
    logger.info(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed!")
        return True
    else:
        logger.error("❌ Some tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
