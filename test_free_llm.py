#!/usr/bin/env python3
"""
Test script for free LLM providers
Tests all available free LLM alternatives to OpenAI
"""

import os
from dotenv import load_dotenv
from llm_providers import llm_manager, OllamaProvider, GroqProvider, TogetherAIProvider, HuggingFaceProvider

# Load environment variables
load_dotenv()

def test_individual_providers():
    """Test each provider individually"""
    print("🧪 Testing individual LLM providers...\n")
    
    # Test Ollama
    print("1. Testing Ollama (Local)...")
    ollama = OllamaProvider()
    if ollama.is_available():
        print("✅ Ollama is available")
        response = ollama.generate_completion("Say 'Hello from Ollama!' if you can read this.")
        if response.success:
            print(f"✅ Ollama response: {response.content[:100]}...")
        else:
            print(f"❌ Ollama failed: {response.error}")
    else:
        print("❌ Ollama not available (install Ollama and pull a model)")
    
    print()
    
    # Test Groq
    print("2. Testing Groq...")
    groq = GroqProvider()
    if groq.is_available():
        print("✅ Groq is available")
        response = groq.generate_completion("Say 'Hello from Groq!' if you can read this.")
        if response.success:
            print(f"✅ Groq response: {response.content[:100]}...")
        else:
            print(f"❌ Groq failed: {response.error}")
    else:
        print("❌ Groq not available (set GROQ_API_KEY)")
    
    print()
    
    # Test Together AI
    print("3. Testing Together AI...")
    together = TogetherAIProvider()
    if together.is_available():
        print("✅ Together AI is available")
        response = together.generate_completion("Say 'Hello from Together AI!' if you can read this.")
        if response.success:
            print(f"✅ Together AI response: {response.content[:100]}...")
        else:
            print(f"❌ Together AI failed: {response.error}")
    else:
        print("❌ Together AI not available (set TOGETHER_API_KEY)")
    
    print()
    
    # Test Hugging Face
    print("4. Testing Hugging Face...")
    hf = HuggingFaceProvider()
    if hf.is_available():
        print("✅ Hugging Face is available")
        response = hf.generate_completion("Say 'Hello from Hugging Face!' if you can read this.")
        if response.success:
            print(f"✅ Hugging Face response: {response.content[:100]}...")
        else:
            print(f"❌ Hugging Face failed: {response.error}")
    else:
        print("❌ Hugging Face not available (set HUGGINGFACE_API_KEY)")

def test_llm_manager():
    """Test the LLM manager with fallback"""
    print("\n🧪 Testing LLM Manager with fallback...\n")
    
    available_providers = llm_manager.get_available_providers()
    print(f"Available providers: {available_providers}")
    
    if not available_providers:
        print("❌ No providers available. Please set up at least one provider.")
        return
    
    # Test company generation prompt
    prompt = """Find 3 real, existing technology companies in Japan.

Requirements:
- Use only real companies that actually exist
- Provide working website URLs
- Use realistic contact information
- Focus on technology companies in Japan

Return ONLY valid JSON in this exact format:

{
    "companies": [
        {
            "name": "Real Company Name",
            "website": "https://realcompany.com",
            "country": "JP",
            "industry": "Technology",
            "contact_name": "John Smith",
            "contact_title": "CEO",
            "contact_email": "john.smith@realcompany.com",
            "description": "Brief description of what the company does"
        }
    ]
}

CRITICAL: Return ONLY the JSON object above. No explanations, no markdown, no additional text."""
    
    system_prompt = "You are a business research assistant. Return only valid JSON."
    
    print("🔄 Generating companies using LLM manager...")
    response = llm_manager.generate_completion(prompt, system_prompt, max_tokens=1000)
    
    if response.success:
        print(f"✅ Success with {response.provider} ({response.model})")
        print(f"Response: {response.content[:200]}...")
        
        # Try to parse as JSON
        try:
            import json
            data = json.loads(response.content)
            if "companies" in data:
                print(f"✅ JSON parsed successfully - found {len(data['companies'])} companies")
            else:
                print("⚠️ JSON parsed but no 'companies' key found")
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
    else:
        print(f"❌ LLM Manager failed: {response.error}")

def test_real_company_generator():
    """Test the real company generator with new LLM providers"""
    print("\n🧪 Testing Real Company Generator...\n")
    
    try:
        from real_companies import RealCompanyGenerator
        
        generator = RealCompanyGenerator()
        
        # Test with a simple ICP
        icp_description = "technology companies in Japan, gaming, AI startups"
        print(f"🔄 Generating companies for: {icp_description}")
        
        companies = generator.generate_real_companies(icp_description, 3)
        
        if companies:
            print(f"✅ Generated {len(companies)} companies:")
            for i, company in enumerate(companies, 1):
                print(f"  {i}. {company.name} - {company.contact_name} ({company.contact_email})")
                print(f"     Website: {company.website}")
                print(f"     Industry: {company.industry}")
        else:
            print("❌ No companies generated")
            
    except Exception as e:
        print(f"❌ Real Company Generator test failed: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing Free LLM Providers for 24-Hour Mailer\n")
    print("=" * 60)
    
    # Test individual providers
    test_individual_providers()
    
    # Test LLM manager
    test_llm_manager()
    
    # Test real company generator
    test_real_company_generator()
    
    print("\n" + "=" * 60)
    print("🏁 Testing complete!")
    
    # Provide setup instructions
    print("\n📋 Setup Instructions:")
    print("1. Ollama (Recommended - completely free):")
    print("   - Install: https://ollama.ai/")
    print("   - Run: ollama pull llama3.2")
    print("   - No API key needed!")
    
    print("\n2. Groq (Very fast, free tier):")
    print("   - Sign up: https://console.groq.com/")
    print("   - Get free API key")
    print("   - Add GROQ_API_KEY to .env")
    
    print("\n3. Together AI (Free tier):")
    print("   - Sign up: https://api.together.xyz/")
    print("   - Get free API key")
    print("   - Add TOGETHER_API_KEY to .env")
    
    print("\n4. Hugging Face (Free tier):")
    print("   - Sign up: https://huggingface.co/")
    print("   - Get API token: https://huggingface.co/settings/tokens")
    print("   - Add HUGGINGFACE_API_KEY to .env")

if __name__ == "__main__":
    main()
