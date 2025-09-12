#!/usr/bin/env python3
"""
Test script for real company generation
"""

import os
from dotenv import load_dotenv
from real_companies import RealCompanyGenerator

# Load environment variables
load_dotenv()

def test_company_generation():
    """Test the real company generation functionality"""
    print("=== Testing Real Company Generation ===")
    
    # Check if API key exists
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ No OpenAI API key found in .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        # Initialize the generator
        generator = RealCompanyGenerator()
        
        # Test with a simple ICP description
        icp_description = "Gaming companies in Japan that develop mobile games"
        num_companies = 3
        
        print(f"🔄 Generating {num_companies} companies for: {icp_description}")
        
        companies = generator.generate_real_companies(icp_description, num_companies)
        
        print(f"✅ Generated {len(companies)} companies:")
        for i, company in enumerate(companies, 1):
            print(f"  {i}. {company.name} ({company.website})")
            print(f"     Contact: {company.contact_name} ({company.contact_title})")
            print(f"     Email: {company.contact_email}")
            print(f"     Industry: {company.industry}")
            print()
        
        # Test saving to CSV
        print("🔄 Testing CSV save functionality...")
        generator.save_companies_csv(companies, "test_companies.csv")
        print("✅ Companies saved to test_companies.csv")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_company_generation()