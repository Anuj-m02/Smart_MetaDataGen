import os
import requests
from dotenv import load_dotenv
import json
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "meta-llama/llama-3-8b-instruct"  # You can change this to other models
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def validate_api_setup():
    """
    Validate that API key is configured
    """
    if not API_KEY:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please set it in your .env file.")
    return True

def generate_rich_metadata(text):
    """
    Generate comprehensive metadata from document text using OpenRouter API
    """
    validate_api_setup()
    
    # Truncate text if too long to avoid token limits
    max_chars = 8000  # Adjust based on your model's context window
    if len(text) > max_chars:
        text = text[:max_chars] + "... [truncated]"
        logger.warning(f"Text truncated to {max_chars} characters due to length")
    
    prompt = f"""
You are an expert document analysis assistant. Analyze the following document content and extract comprehensive metadata.

Please provide a detailed analysis in valid JSON format with the following fields:

{{
    "title": "Document title (infer if not explicitly stated)",
    "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
    "summary": "2-3 sentence summary of the document",
    "document_category": "Category (e.g., Legal, Academic, Finance, Health, Technical, Business, Personal, etc.)",
    "language": "Primary language of the document",
    "sentiment": "Overall sentiment (Positive, Negative, Neutral)",
    "named_entities": {{
        "people": ["person1", "person2"],
        "organizations": ["org1", "org2"],
        "locations": ["location1", "location2"]
    }},
    "confidential": "Assessment if document contains sensitive information (Yes/No/Uncertain)",
    "important_dates": ["date1", "date2"],
    "document_structure": ["section1", "section2", "section3"],
    "author": "Author name if mentioned or 'Not specified'",
    "intended_audience": "Target audience (e.g., General Public, Professionals, Students, etc.)",
    "estimated_reading_time": "Reading time in minutes (integer)",
    "content_features": {{
        "has_tables": "Yes/No",
        "has_charts": "Yes/No", 
        "has_images": "Yes/No",
        "has_references": "Yes/No"
    }},
    "topic_tags": ["tag1", "tag2", "tag3"],
    "key_points": ["point1", "point2", "point3"],
    "document_quality": "Assessment of document quality (High/Medium/Low)",
    "technical_level": "Technical complexity (Beginner/Intermediate/Advanced)",
    "word_count": "Estimated word count (integer)"
}}

Document Content:
{text}

Important: Return ONLY the JSON object, properly formatted and valid. Do not include any additional text, explanations, or markdown formatting.
    """
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://smartmeta-app.com",  # Optional: Add your app URL
        "X-Title": "SmartMeta Document Analyzer"  # Optional: Add app name
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system", 
                "content": "You are a professional document analysis assistant. Always respond with valid JSON format only."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "temperature": 0.3,  # Lower temperature for more consistent outputs
        "max_tokens": 1500,
        "top_p": 0.9
    }
    
    try:
        logger.info(f"Sending request to OpenRouter API using model: {MODEL}")
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Log token usage if available
            if "usage" in result:
                usage = result["usage"]
                logger.info(f"Token usage - Prompt: {usage.get('prompt_tokens', 'N/A')}, "
                          f"Completion: {usage.get('completion_tokens', 'N/A')}, "
                          f"Total: {usage.get('total_tokens', 'N/A')}")
            
            return content
            
        elif response.status_code == 429:
            logger.warning("Rate limit exceeded. Waiting 5 seconds before retry...")
            time.sleep(5)
            # Retry once
            response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                raise Exception(f"API rate limit error: {response.status_code} - {response.text}")
                
        else:
            error_msg = f"OpenRouter API error: {response.status_code}"
            try:
                error_detail = response.json()
                if "error" in error_detail:
                    error_msg += f" - {error_detail['error'].get('message', response.text)}"
            except:
                error_msg += f" - {response.text}"
            
            logger.error(error_msg)
            raise Exception(error_msg)
    
    except requests.exceptions.Timeout:
        raise Exception("API request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise Exception("Failed to connect to OpenRouter API. Please check your internet connection.")
    except Exception as e:
        logger.error(f"Error calling OpenRouter API: {str(e)}")
        raise Exception(f"API call failed: {str(e)}")

def generate_metadata(text):
    """
    Main function to generate metadata
    """
    if not text or len(text.strip()) < 10:
        raise ValueError("Text is too short for meaningful metadata generation")
    
    logger.info(f"Generating metadata for text of length: {len(text)} characters")
    
    try:
        return generate_rich_metadata(text)
    except Exception as e:
        logger.error(f"Metadata generation failed: {str(e)}")
        raise

def test_metadata_generation():
    """
    Test function to verify metadata generation works
    """
    test_text = """
    This is a sample document about artificial intelligence and machine learning.
    It discusses the applications of AI in various industries including healthcare,
    finance, and education. The document was written in 2024 and provides an
    overview of current trends and future developments in the field.
    
    The document covers topics such as natural language processing, computer vision,
    and deep learning algorithms. It is intended for business professionals and
    technical managers who want to understand AI implementation strategies.
    """
    
    try:
        print("Testing metadata generation...")
        result = generate_metadata(test_text)
        print("✅ Metadata generation successful!")
        print(f"Result preview: {result[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Metadata generation failed: {str(e)}")
        return False

def validate_json_response(response_text):
    """
    Validate and clean JSON response from API
    """
    try:
        # Try to parse as-is first
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON from markdown code blocks
        import re
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL | re.IGNORECASE)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON object in the text
        json_match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        raise ValueError("No valid JSON found in response")

# Alternative models you can use (uncomment to switch):
# MODEL = "openai/gpt-3.5-turbo"
# MODEL = "anthropic/claude-3-haiku"
# MODEL = "google/gemini-pro"
# MODEL = "mistralai/mistral-7b-instruct"

if __name__ == "__main__":
    print("Metadata Generation Module")
    print(f"Using model: {MODEL}")
    
    # Test API setup
    try:
        validate_api_setup()
        print("✅ API configuration validated")
    except Exception as e:
        print(f"❌ API configuration error: {str(e)}")
    
    # Test metadata generation
    test_metadata_generation()