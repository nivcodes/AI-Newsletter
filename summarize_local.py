import requests

def summarize_article(text):
    url = "http://localhost:1234/v1/chat/completions"  # LM Studio local API
    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert AI analyst.

Summarize the following article in two formats:
1. Technical Summary
2. Business Summary

ARTICLE:
{text}
"""

    data = {
        "model": "mistral-7b-instruct-v0.3",  # replace with your model's name
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# Example usage
if __name__ == "__main__":
    example_text = "OpenAI has released a new version of its GPT model that includes improved multi-modal capabilities..."
    summary = summarize_article(example_text)
    print(summary)
