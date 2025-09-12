#!/usr/bin/env python3
"""
Test Groq API integration (clean version)
"""

import os
from real_companies import RealCompanyGenerator

def main():
    print("🚀 Testing: Groq Integration")
    print("=" * 50)
    
    # Check if API key is set
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ Please set GROQ_API_KEY environment variable")
        print("   Get your free API key at: https://console.groq.com/")
        return
    
    try:
        generator = RealCompanyGenerator()
        
        icp_description = "AI startups from the US"
        print(f"🔄 Generating companies for: {icp_description}")
        
        companies = generator.generate_real_companies(icp_description, 3)
        
        if companies:
            print(f"✅ Generated {len(companies)} companies:")
            for i, company in enumerate(companies, 1):
                print(f"  {i}. {company.name} - {company.contact_name}")
                print(f"     Email: {company.contact_email}")
                print(f"     Website: {company.website}")
                print(f"     Country: {company.country}")
                print(f"     Industry: {company.industry}")
                print()
        else:
            print("❌ No companies generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
