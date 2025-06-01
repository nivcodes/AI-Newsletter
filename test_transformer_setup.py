#!/usr/bin/env python3
"""
Test script to verify the transformer-based newsletter generation works
"""
import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_transformer_import():
    """Test if transformer dependencies can be imported"""
    try:
        import torch
        import transformers
        logger.info(f"✅ PyTorch version: {torch.__version__}")
        logger.info(f"✅ Transformers version: {transformers.__version__}")
        logger.info(f"✅ CUDA available: {torch.cuda.is_available()}")
        return True
    except ImportError as e:
        logger.error(f"❌ Failed to import transformer dependencies: {e}")
        return False

def test_transformer_summarizer():
    """Test the transformer summarizer"""
    try:
        from utils.transformer_summarizer import HuggingFaceTransformerSummarizer
        
        logger.info("🧪 Testing transformer summarizer initialization...")
        summarizer = HuggingFaceTransformerSummarizer()
        
        # Test with a simple prompt
        test_prompt = "Summarize this: AI is transforming how we work and live."
        logger.info("🧪 Testing text generation...")
        
        result = summarizer.generate_text(test_prompt, max_length=100, temperature=0.7)
        
        if result:
            logger.info(f"✅ Transformer test successful!")
            logger.info(f"📝 Generated text: {result[:100]}...")
            return True
        else:
            logger.error("❌ Transformer generated no output")
            return False
            
    except Exception as e:
        logger.error(f"❌ Transformer test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_config_setup():
    """Test configuration setup"""
    try:
        from config import USE_TRANSFORMER, TRANSFORMER_MODEL, PREFERRED_LLM
        
        logger.info(f"📋 USE_TRANSFORMER: {USE_TRANSFORMER}")
        logger.info(f"📋 TRANSFORMER_MODEL: {TRANSFORMER_MODEL}")
        logger.info(f"📋 PREFERRED_LLM: {PREFERRED_LLM}")
        
        if USE_TRANSFORMER and PREFERRED_LLM == "transformer":
            logger.info("✅ Configuration is set to use transformers")
            return True
        else:
            logger.warning("⚠️ Configuration not set to use transformers by default")
            return True  # Not a failure, just different config
            
    except Exception as e:
        logger.error(f"❌ Config test failed: {e}")
        return False

def test_enhanced_summarizer_integration():
    """Test that enhanced summarizer can use transformers"""
    try:
        from utils.enhanced_summarizer import EnhancedSummarizer
        
        logger.info("🧪 Testing enhanced summarizer with transformer backend...")
        
        # Create a mock article
        mock_article = {
            'title': 'Test AI Article',
            'url': 'https://example.com/test',
            'text': 'This is a test article about artificial intelligence and machine learning developments.',
            'category': 'research',
            'popularity_score': 75
        }
        
        summarizer = EnhancedSummarizer()
        
        # Test basic summary generation
        logger.info("🧪 Testing basic summary generation...")
        summary = summarizer.get_basic_summary(mock_article)
        
        if summary:
            logger.info("✅ Enhanced summarizer integration test successful!")
            logger.info(f"📝 Generated summary: {summary[:100]}...")
            return True
        else:
            logger.error("❌ Enhanced summarizer generated no output")
            return False
            
    except Exception as e:
        logger.error(f"❌ Enhanced summarizer integration test failed: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def main():
    """Run all tests"""
    logger.info("🚀 Starting transformer setup tests...")
    logger.info("=" * 60)
    
    tests = [
        ("Import Test", test_transformer_import),
        ("Config Test", test_config_setup),
        ("Transformer Summarizer Test", test_transformer_summarizer),
        ("Enhanced Summarizer Integration Test", test_enhanced_summarizer_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n🧪 Running {test_name}...")
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                logger.info(f"✅ {test_name} PASSED")
            else:
                logger.error(f"❌ {test_name} FAILED")
        except Exception as e:
            logger.error(f"❌ {test_name} CRASHED: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
    
    logger.info(f"\n📈 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Your transformer setup is ready for GitHub Actions!")
        return 0
    else:
        logger.error("⚠️ Some tests failed. Check the logs above for details.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
