#!/usr/bin/env python3
"""
Diagnostic script to test OpenAI API access
"""

import os
import openai
from dotenv import load_dotenv

load_dotenv()

def diagnose():
    api_key = os.getenv("OPENAI_API_KEY")
    print(f"API Key: {api_key[:20]}..." if api_key else "No key")
    print(f"Key type: {'Project' if api_key and api_key.startswith('sk-proj') else 'Service Account' if api_key and api_key.startswith('sk-svcacct') else 'Regular' if api_key and api_key.startswith('sk-') else 'Unknown'}")
    
    if not api_key:
        print("❌ No API key found")
        return
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Test 1: Simple request
        print("\n🔄 Test 1: Simple request...")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=1
        )
        print("✅ Simple request successful")
        
        # Test 2: Check available models
        print("\n🔄 Test 2: Check models...")
        models = client.models.list()
        available_models = [model.id for model in models.data if 'gpt' in model.id]
        print(f"Available GPT models: {available_models[:5]}...")
        
        # Test 3: Usage info
        print(f"\n✅ API is working! Response: {response.choices[0].message.content}")
        print(f"Model used: {response.model}")
        print(f"Usage: {response.usage}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print(f"Error type: {type(e).__name__}")
        
        # Detailed error analysis
        error_str = str(e).lower()
        if "quota" in error_str:
            print("💡 Quota issue - but you have credits, so this might be:")
            print("   - Rate limiting (too many requests)")
            print("   - Model access restrictions")
            print("   - Account type limitations")
        elif "rate" in error_str:
            print("💡 Rate limiting - wait a moment and try again")
        elif "model" in error_str:
            print("💡 Model access issue - try a different model")
        elif "key" in error_str:
            print("💡 API key issue - check if key is valid")

if __name__ == "__main__":
    diagnose()

