#!/usr/bin/env python3
"""
Test script to check OpenAI installation and fix the issue
"""

import sys
import os

def test_openai():
    try:
        import openai
        print(f"OpenAI version: {openai.__version__}")
        
        # Test if OpenAI class exists
        if hasattr(openai, 'OpenAI'):
            print("✓ openai.OpenAI class exists")
            client = openai.OpenAI(api_key="test-key")
            print("✓ Successfully created OpenAI client")
        else:
            print("✗ openai.OpenAI class not found")
            print("Available attributes:", [attr for attr in dir(openai) if not attr.startswith('_')])
            
    except ImportError as e:
        print(f"✗ Failed to import openai: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")

if __name__ == "__main__":
    test_openai()

