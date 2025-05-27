"""
Test script to generate a modern newsletter design using existing content
"""
import os
from utils.modern_html_processor import save_modern_newsletter_files

# Sample content to test the modern design
sample_content = {
    'intro': """
    Welcome to our latest edition of the AI Newsletter, where we curate the most intriguing and thought-provoking stories in the ever-evolving world of artificial intelligence. Today's selection promises a fascinating mix of topics, ranging from breakthrough research to industry developments that are shaping our future.
    """,
    'summaries': [
        """
![thumbnail](https://example.com/image1.jpg)

# OpenAI Releases Revolutionary GPT-5 Model

The Rundown: OpenAI has unveiled GPT-5, a groundbreaking language model that demonstrates unprecedented reasoning capabilities and multimodal understanding.

- **Enhanced Reasoning**: The model shows significant improvements in complex problem-solving and logical reasoning tasks
- **Multimodal Integration**: GPT-5 can seamlessly process text, images, audio, and video in a unified framework
- **Efficiency Gains**: Despite increased capabilities, the model requires 40% less computational resources than its predecessor

Why it matters: This advancement represents a major leap forward in AI capabilities, potentially revolutionizing how we interact with artificial intelligence across industries. The improved efficiency could make advanced AI more accessible to smaller organizations and developers worldwide.

👉 [Read more](https://example.com/gpt5-release)
        """,
        """
![thumbnail](https://example.com/image2.jpg)

# Google DeepMind Achieves Breakthrough in Protein Folding

The Rundown: Google DeepMind's latest AlphaFold iteration has successfully predicted the structure of over 200 million proteins, covering nearly every known protein in existence.

- **Universal Coverage**: The new model covers proteins from over 1 million species
- **Medical Applications**: Researchers are already using the data to develop new treatments for rare diseases
- **Open Access**: All protein structures are freely available to the global research community

Why it matters: This breakthrough could accelerate drug discovery by decades, potentially leading to treatments for diseases that have puzzled scientists for generations. The open-access approach ensures that researchers worldwide can benefit from this advancement.

👉 [Read more](https://example.com/alphafold-breakthrough)
        """,
        """
![thumbnail](https://example.com/image3.jpg)

# Meta Introduces Advanced AI Safety Framework

The Rundown: Meta has announced a comprehensive AI safety framework designed to address alignment, robustness, and ethical considerations in large-scale AI systems.

- **Multi-layered Approach**: The framework includes technical safeguards, ethical guidelines, and continuous monitoring systems
- **Industry Collaboration**: Meta is working with other tech giants to establish industry-wide safety standards
- **Transparency Initiative**: Regular safety reports will be published to maintain public accountability

Why it matters: As AI systems become more powerful, robust safety frameworks are essential for maintaining public trust and ensuring beneficial outcomes. Meta's proactive approach could set new industry standards for responsible AI development.

👉 [Read more](https://example.com/meta-ai-safety)
        """
    ]
}

def main():
    print("🎨 Testing Modern Newsletter Design...")
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Generate modern newsletter
    try:
        files = save_modern_newsletter_files(sample_content, 'output')
        
        print("✅ Modern newsletter generated successfully!")
        print(f"📄 File saved: {files['modern_html']}")
        print("\n🌟 Open the generated file in your browser to see the beautiful design!")
        print("💡 The newsletter features:")
        print("   • Responsive design that works on all devices")
        print("   • Beautiful gradient headers and modern typography")
        print("   • Interactive hover effects and smooth animations")
        print("   • Categorized articles with visual hierarchy")
        print("   • Professional styling optimized for engagement")
        
    except Exception as e:
        print(f"❌ Error generating modern newsletter: {e}")

if __name__ == "__main__":
    main()
