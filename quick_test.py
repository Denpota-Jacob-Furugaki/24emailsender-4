#!/usr/bin/env python3
"""
Quick test to verify OpenAI setup
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_setup():
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key or api_key == "your_openai_api_key_here":
        print("❌ Please set your OpenAI API key in the .env file")
        print("   Get your API key from: https://platform.openai.com/api-keys")
        return False
    
    try:
        import openai
        print(f"✅ OpenAI library version: {openai.__version__}")
        
        if hasattr(openai, 'OpenAI'):
            print("✅ OpenAI client class available")
            return True
        else:
            print("❌ OpenAI client class not found")
            return False
            
    except ImportError:
        print("❌ OpenAI library not installed. Run: python -m pip install openai")
        return False

if __name__ == "__main__":
    test_setup()

