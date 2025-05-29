"""
Test script to generate newsletter with improved HTML structure
"""
import sys
import os
from datetime import datetime

# Add utils to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

from improved_html_processor import save_improved_newsletter_files

def create_sample_content():
    """Create sample newsletter content for testing"""
    return {
        'intro': '''Welcome to this week's edition of our premium AI newsletter! As the digital landscape continues to evolve at an unprecedented pace, we're here to help you stay ahead of the curve. Today, we've curated a thrilling array of insights that delves deep into the world of AI tools, industry trends, and groundbreaking research.

First up, Mistral's innovative API promises to revolutionize AI agent building by allowing Python, image generation, and RAG capabilities. Meanwhile, Spott's $3.2M fundraise signifies a significant leap in AI-native recruiting platforms, aiming to end the chaos that often plagues traditional hiring software.''',
        
        'articles': [
            {
                'title': 'Mistral launches API for building AI agents that run Python, generate images, perform RAG and more',
                'url': 'https://venturebeat.com/ai/mistral-launches-api-for-building-ai-agents-that-run-python-generate-images-perform-rag-and-more/',
                'image_url': 'https://venturebeat.com/wp-content/uploads/2025/05/mistral-ai-agents.jpg',
                'category': 'tools',
                'popularity_score': 95
            },
            {
                'title': 'Spott\'s AI-native recruiting platform scores $3.2M to end hiring software chaos',
                'url': 'https://venturebeat.com/ai/spotts-ai-native-recruiting-platform-scores-32m-to-end-hiring-software-chaos/',
                'image_url': 'https://venturebeat.com/wp-content/uploads/2025/05/spott-recruiting.jpg',
                'category': 'industry',
                'popularity_score': 88
            },
            {
                'title': 'FrodoKEM: A conservative quantum-safe cryptographic algorithm',
                'url': 'https://www.microsoft.com/en-us/research/blog/frodokem-a-conservative-quantum-safe-cryptographic-algorithm/',
                'image_url': 'https://www.microsoft.com/en-us/research/wp-content/uploads/2025/05/FrodoKEM-TWLIFB-1200x627-1.jpg',
                'category': 'research',
                'popularity_score': 82
            },
            {
                'title': 'The AI Hype Index: College students are hooked on ChatGPT',
                'url': 'https://www.technologyreview.com/2025/05/28/ai-hype-index-college-students-chatgpt/',
                'image_url': 'https://wp.technologyreview.com/wp-content/uploads/2025/05/May-Thumb.png',
                'category': 'use-case',
                'popularity_score': 76
            },
            {
                'title': 'Everyone\'s looking to get in on vibe coding — and Google is no different with Stitch',
                'url': 'https://venturebeat.com/ai/everyones-looking-to-get-in-on-vibe-coding-and-google-is-no-different-with-stitch/',
                'image_url': 'https://venturebeat.com/wp-content/uploads/2024/10/colorful-pc.jpg',
                'category': 'tools',
                'popularity_score': 71
            }
        ],
        
        'summaries': [
            'Mistral has launched a groundbreaking API that enables developers to build sophisticated AI agents capable of running Python code, generating images, and performing Retrieval-Augmented Generation (RAG). This comprehensive platform represents a significant leap forward in AI agent development, offering unprecedented flexibility and functionality.',
            
            'Spott has secured $3.2M in funding to revolutionize the recruiting industry with its AI-native platform designed to eliminate the chaos of fragmented hiring software. The platform promises to streamline recruitment processes through intelligent automation and unified workflow management.',
            
            'Microsoft Research introduces FrodoKEM, a conservative approach to quantum-safe cryptography that prioritizes security and reliability. This key encapsulation mechanism is designed to protect against future quantum computing threats while maintaining practical implementation standards.',
            
            'MIT Technology Review\'s AI Hype Index reveals that college students have become increasingly dependent on ChatGPT for academic work, raising questions about educational integrity and the long-term impact of AI assistance on learning outcomes.',
            
            'Google enters the "vibe coding" space with Stitch, a follow-up to their Jules project that aims to make programming more intuitive and accessible through natural language interfaces and contextual understanding.'
        ],
        
        'editors_takes': [
            {
                'title': 'Mistral launches API for building AI agents that run Python, generate images, perform RAG and more',
                'take': 'This move by Mistral signals a significant leap forward in the democratization of advanced AI capabilities. By offering an API that enables seamless integration of autonomous generative AI agents, they are breaking down barriers for both enterprises and independent developers. This could potentially spark a wave of innovative applications, transcending the text-generation limitations of traditional language models.'
            },
            {
                'title': 'Spott\'s AI-native recruiting platform scores $3.2M to end hiring software chaos',
                'take': 'This $3.2M investment in Spott signifies a bold challenge to the fragmented recruitment tech landscape, promising to streamline processes and boost efficiency with its AI-native platform. As we\'ve seen generative AI tools proliferate since 2022, it\'s refreshing to see an all-in-one solution that tackles the entire workflow rather than merely addressing single pain points.'
            }
        ]
    }

def main():
    """Generate improved newsletter for testing"""
    print("🚀 Testing Improved Newsletter Generator...")
    
    # Create sample content
    content = create_sample_content()
    
    # Generate improved newsletter
    try:
        saved_files = save_improved_newsletter_files(content)
        
        if saved_files and 'improved_html' in saved_files:
            print(f"✅ Newsletter generated successfully!")
            print(f"📄 HTML file: {saved_files['improved_html']}")
            
            # Show file size
            file_size = os.path.getsize(saved_files['improved_html'])
            print(f"📊 File size: {file_size:,} bytes")
            
            print("\n🎉 You can now open the HTML file to see the improved structure!")
            print(f"💡 Try: open {saved_files['improved_html']}")
            
        else:
            print("❌ Failed to generate newsletter")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
