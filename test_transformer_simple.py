#!/usr/bin/env python3
"""
Simple test to verify transformer model works
"""
import os
import sys

# Set environment variables for testing
os.environ['USE_TRANSFORMER'] = 'true'
os.environ['PREFERRED_LLM'] = 'transformer'
os.environ['TRANSFORMER_MODEL'] = 'google/flan-t5-large'

def test_transformer_directly():
    """Test the transformer model directly"""
    try:
        print("🧪 Testing transformer model directly...")
        
        # Import and test
        from utils.transformer_summarizer import HuggingFaceTransformerSummarizer
        
        print("✅ Transformer summarizer imported successfully")
        
        # Create instance
        summarizer = HuggingFaceTransformerSummarizer()
        print("✅ Transformer summarizer instance created")
        
        # Test simple generation
        test_prompt = "Summarize this AI news: OpenAI released a new model that improves reasoning capabilities."
        print(f"🧪 Testing with prompt: {test_prompt}")
        
        result = summarizer.generate_text(test_prompt, max_length=200, temperature=0.7)
        
        if result:
            print("✅ SUCCESS! Transformer model generated response:")
            print(f"📝 Response: {result}")
            return True
        else:
            print("❌ FAILED: Transformer model returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_summarizer():
    """Test the enhanced summarizer with transformer backend"""
    try:
        print("\n🧪 Testing enhanced summarizer with transformer backend...")
        
        from utils.enhanced_summarizer import EnhancedSummarizer
        
        # Create mock article
        mock_article = {
            'title': 'Test AI Article: New Model Breakthrough',
            'url': 'https://example.com/test',
            'text': 'Researchers have developed a new AI model that significantly improves performance on reasoning tasks. The model uses advanced techniques to better understand context and provide more accurate responses. This breakthrough could have major implications for AI applications.',
            'category': 'research',
            'popularity_score': 75
        }
        
        summarizer = EnhancedSummarizer()
        print("✅ Enhanced summarizer created")
        
        # Test basic summary
        summary = summarizer.get_basic_summary(mock_article)
        
        if summary:
            print("✅ SUCCESS! Enhanced summarizer generated response:")
            print(f"📝 Summary: {summary[:200]}...")
            return True
        else:
            print("❌ FAILED: Enhanced summarizer returned empty result")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 Testing Free Transformer Model Setup")
    print("=" * 50)
    
    # Check if dependencies are available
    try:
        import torch
        import transformers
        print(f"✅ Dependencies available - PyTorch: {torch.__version__}, Transformers: {transformers.__version__}")
        deps_available = True
    except ImportError as e:
        print(f"⚠️ Dependencies not installed: {e}")
        print("💡 To install: pip install torch transformers tokenizers sentencepiece")
        deps_available = False
    
    if not deps_available:
        print("\n❌ Cannot test without dependencies. Install them first or test in GitHub Actions.")
        return 1
    
    # Test transformer directly
    success1 = test_transformer_directly()
    
    # Test enhanced summarizer integration
    success2 = test_enhanced_summarizer()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"✅ Direct transformer test: {'PASS' if success1 else 'FAIL'}")
    print(f"✅ Enhanced summarizer test: {'PASS' if success2 else 'FAIL'}")
    
    if success1 and success2:
        print("\n🎉 All tests passed! Your free transformer setup is working!")
        return 0
    else:
        print("\n⚠️ Some tests failed. Check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
