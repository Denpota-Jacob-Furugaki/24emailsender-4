#!/usr/bin/env python3
"""
Test script to check OpenAI API quota and access
"""

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_access():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key found: {'Yes' if api_key else 'No'}")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        print("🔄 Testing API access...")
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a very simple, low-cost request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hi"}
            ],
            max_tokens=5  # Very small to minimize cost
        )
        
        result = response.choices[0].message.content
        print(f"✅ API is working! Response: {result}")
        
        # Check usage
        print(f"✅ Model: {response.model}")
        print(f"✅ Usage: {response.usage}")
        return True
        
    except Exception as e:
        print(f"❌ API Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Check if it's a specific error
        error_str = str(e).lower()
        if "quota" in error_str:
            print("💡 This is a quota error - check your billing")
        elif "rate" in error_str:
            print("💡 This is a rate limit error - wait a moment and try again")
        elif "model" in error_str:
            print("💡 This might be a model access issue")
        
        return False

if __name__ == "__main__":
    test_api_access()

