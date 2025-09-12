#!/usr/bin/env python3
"""
Simple test to check OpenAI API access
"""

import os
import openai
from dotenv import load_dotenv

load_dotenv()

def test_simple():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key: {api_key[:15]}..." if api_key else "No key")
    
    if not api_key:
        return
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Try the simplest possible request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=1
        )
        
        print("SUCCESS!")
        print(f"Response: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Type: {type(e).__name__}")

if __name__ == "__main__":
    test_simple()