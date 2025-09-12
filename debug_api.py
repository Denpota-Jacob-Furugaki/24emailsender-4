#!/usr/bin/env python3
"""
Debug script to test OpenAI API call directly
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_call():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        print("🔄 Testing API call...")
        client = openai.OpenAI(api_key=api_key)
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
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_api_call()
