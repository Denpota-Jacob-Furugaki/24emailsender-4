#!/usr/bin/env python3
"""
Test script to check if OpenAI API is working
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def test_openai_api():
    """Test if OpenAI API is working"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    print(f"API Key found: {api_key[:10]}..." if api_key else "No API key found")
    
    if not api_key:
        print("❌ No OpenAI API key found in .env file")
        return False
    
    try:
        # Initialize the OpenAI client with the API key
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Say 'Hello, API is working!' if you can read this."}
            ],
            max_tokens=50
        )
        
        result = response.choices[0].message.content
        print(f"✅ API is working! Response: {result}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI API...")
    test_openai_api()
