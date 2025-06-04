#!/usr/bin/env python3
"""
Test script to verify AWS Bedrock configuration and connectivity
Run this locally to test your AWS Bedrock setup before using in GitHub Actions
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_aws_bedrock():
    """Test AWS Bedrock connectivity and configuration"""
    print("🧪 Testing AWS Bedrock Configuration...")
    print("=" * 50)
    
    # Check environment variables
    required_vars = [
        'USE_AWS_BEDROCK',
        'AWS_ACCESS_KEY_ID', 
        'AWS_SECRET_ACCESS_KEY',
        'AWS_REGION'
    ]
    
    print("📋 Checking environment variables:")
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            if 'KEY' in var:
                print(f"  ✅ {var}: {'*' * 8}...{value[-4:]}")  # Mask sensitive data
            else:
                print(f"  ✅ {var}: {value}")
        else:
            print(f"  ❌ {var}: Not set")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file or environment configuration.")
        return False
    
    # Test boto3 import
    print("\n📦 Testing boto3 import:")
    try:
        import boto3
        print("  ✅ boto3 imported successfully")
    except ImportError as e:
        print(f"  ❌ boto3 import failed: {e}")
        print("  Run: pip install boto3")
        return False
    
    # Test AWS credentials and Bedrock client
    print("\n🔐 Testing AWS Bedrock client:")
    try:
        bedrock_client = boto3.client(
            'bedrock-runtime',
            region_name=os.getenv('AWS_REGION'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        print("  ✅ Bedrock client created successfully")
    except Exception as e:
        print(f"  ❌ Bedrock client creation failed: {e}")
        return False
    
    # Test actual API call
    print("\n🤖 Testing Bedrock API call:")
    try:
        import json
        
        model_id = os.getenv('AWS_BEDROCK_MODEL_ID', 'anthropic.claude-3-sonnet-20240229-v1:0')
        print(f"  Using model: {model_id}")
        
        # Simple test prompt
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": "Hello! Please respond with 'AWS Bedrock is working correctly' to confirm the connection."
                }
            ]
        }
        
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        result = response_body['content'][0]['text']
        
        print(f"  ✅ API call successful!")
        print(f"  📝 Response: {result}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ API call failed: {e}")
        print("\nPossible issues:")
        print("  - Check AWS credentials are correct")
        print("  - Verify model access is enabled in AWS Bedrock console")
        print("  - Ensure region supports Bedrock")
        print("  - Check IAM permissions (need bedrock:InvokeModel)")
        return False

def test_enhanced_summarizer():
    """Test the enhanced summarizer with AWS Bedrock"""
    print("\n🧠 Testing Enhanced Summarizer with AWS Bedrock...")
    print("=" * 50)
    
    try:
        from utils.enhanced_summarizer import EnhancedSummarizer
        
        summarizer = EnhancedSummarizer()
        
        # Test article
        test_article = {
            'title': 'Test Article: AI Newsletter Generation',
            'text': 'This is a test article about AI newsletter generation using AWS Bedrock and Claude. The system should be able to generate high-quality summaries using the Anthropic Claude model via AWS Bedrock service.',
            'url': 'https://example.com/test-article',
            'category': 'tools',
            'popularity_score': 75
        }
        
        print("📝 Generating test summary...")
        summary = summarizer.get_editorial_summary(test_article)
        
        if summary:
            print("✅ Summary generated successfully!")
            print("\n📄 Generated Summary:")
            print("-" * 30)
            print(summary)
            print("-" * 30)
            return True
        else:
            print("❌ Summary generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Enhanced summarizer test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AWS Bedrock Test Suite")
    print("=" * 50)
    
    # Test 1: Basic AWS Bedrock connectivity
    bedrock_test = test_aws_bedrock()
    
    if bedrock_test:
        print("\n" + "=" * 50)
        # Test 2: Enhanced summarizer integration
        summarizer_test = test_enhanced_summarizer()
        
        if summarizer_test:
            print("\n🎉 All tests passed! AWS Bedrock is ready for newsletter generation.")
            print("\n📋 Next steps:")
            print("  1. Add the same environment variables to GitHub Secrets")
            print("  2. Run a test workflow in GitHub Actions")
            print("  3. Check the logs for 'Using preferred AWS Bedrock (Anthropic)...'")
        else:
            print("\n⚠️  Basic AWS Bedrock works, but summarizer integration failed.")
            print("Check the enhanced_summarizer.py configuration.")
    else:
        print("\n❌ AWS Bedrock test failed. Please fix the configuration before proceeding.")
        sys.exit(1)
