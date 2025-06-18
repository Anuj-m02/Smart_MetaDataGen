import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")  # store your OpenRouter key as OPENROUTER_API_KEY in .env
model = "meta-llama/llama-3-8b-instruct"  # Change this to your preferred model, e.g., "deepseek-ai/deepseek-coder-6.7b-instruct"

def generate_rich_metadata(text):
    prompt = f"""
You are a document analysis assistant.

Extract the following metadata from the document content below:

1. Title (always required if u can)
2. Keywords (5–10)
3. Short Summary (2–3 lines)
4. Document Category (e.g., Legal, Academic, Finance, Health, etc.)
5. Language
6. Sentiment (Positive, Negative, Neutral)
7. Named Entities (People, Organizations, Locations)
8. Is this document confidential? (Yes/No)
9. Important Dates mentioned (if any)
10. High-level Sections present (e.g., Introduction, Conclusion, etc.)
11. Author (if found)
12. Intended Audience
13. Estimated Reading Time (in minutes)
14. Presence of Tables/Charts/Images (Eg tables yes , charts , yes )
15. Topic Tags / Subject Areas (Example: ["Data Science", "Resume", "Hackathons", "Education"])
16. Summary Bullet Points


Content:
{text}

Return all metadata in JSON format.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"OpenRouter API error: {response.status_code} - {response.text}")


def generate_metadata(text):
    return generate_rich_metadata(text)
