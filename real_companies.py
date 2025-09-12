"""
Real Company Generator using Free LLM Providers
Generates actual companies with real websites and contact information
Uses free alternatives to OpenAI: Ollama, Groq, Together AI, Hugging Face
"""

import json
import csv
import os
from typing import List, Dict
from dataclasses import dataclass
from llm_providers import llm_manager

@dataclass
class RealCompany:
    name: str
    website: str
    country: str
    industry: str
    contact_name: str
    contact_title: str
    contact_email: str
    description: str

class RealCompanyGenerator:
    def __init__(self):
        """Initialize with free LLM providers"""
        # Reinitialize the LLM manager to pick up any new environment variables
        from llm_providers import LLMManager
        self.llm_manager = LLMManager()
        print(f"Available LLM providers: {self.llm_manager.get_available_providers()}")
    
    def generate_real_companies(self, icp_description: str, num_companies: int = 10) -> List[RealCompany]:
        """
        Generate real companies using free LLM providers based on ICP description
        """
        if not self.llm_manager.providers:
            raise ValueError("No LLM providers available. Please set up at least one free provider (Ollama, Groq, Together AI, or Hugging Face).")
        
        prompt = f"""Find {num_companies} real, existing companies that match: "{icp_description}"

Requirements:
- Use only real companies that actually exist
- Provide working website URLs
- Use realistic contact information
- Focus on companies in the specified industry/region

Return ONLY valid JSON in this exact format:

{{
    "companies": [
        {{
            "name": "Real Company Name",
            "website": "https://realcompany.com",
            "country": "US",
            "industry": "Technology",
            "contact_name": "John Smith",
            "contact_title": "CEO",
            "contact_email": "john.smith@realcompany.com",
            "description": "Brief description of what the company does"
        }}
    ]
}}

CRITICAL: Return ONLY the JSON object above. No explanations, no markdown, no additional text."""
        
        try:
            # Use the LLM manager to generate completion
            system_prompt = "You are a business research assistant. Return only valid JSON."
            response = self.llm_manager.generate_completion(prompt, system_prompt, max_tokens=2000)
            
            if not response.success:
                raise Exception(f"LLM generation failed: {response.error}")
            
            content = response.content
            print(f"Raw API response: {content[:200]}...")  # Debug output
            
            # Check if response is complete (addresses Issue #2623)
            if not content or len(content.strip()) < 50:
                print("❌ Response appears incomplete or too short")
                raise Exception("Incomplete response from API")
            
            # Clean up the response - sometimes ChatGPT includes extra text
            original_content = content
            
            # Remove markdown formatting
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            # Try to find JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                content = content[start_idx:end_idx]
            
            # Try to fix common JSON issues
            content = self._fix_json_issues(content)
            
            # Fix escaped quotes issue
            content = content.replace('\\"', '"')
            
            print(f"Cleaned content: {content[:300]}...")
            
            try:
                data = json.loads(content)
                print(f"✅ JSON parsed successfully")
            except json.JSONDecodeError as json_error:
                print(f"❌ JSON parsing failed: {json_error}")
                print(f"Problematic content: {content[:500]}...")
                
                # Try alternative parsing strategies
                companies = self._try_alternative_parsing(content)
                if companies:
                    print(f"✅ Alternative parsing successful: {len(companies)} companies")
                    return companies
                
                # Try to extract companies manually if JSON parsing fails
                companies = self._extract_companies_manually(content)
                if companies:
                    print(f"✅ Manual extraction successful: {len(companies)} companies")
                    return companies
                else:
                    # If manual extraction also fails, use fallback
                    print("❌ All parsing methods failed, using fallback companies")
                    return self._get_fallback_companies(icp_description, num_companies)
            
            companies = []
            for company_data in data.get("companies", []):
                # Ensure all required fields have values
                company = RealCompany(
                    name=company_data.get("name", "").strip(),
                    website=company_data.get("website", "").strip(),
                    country=company_data.get("country", "").strip(),
                    industry=company_data.get("industry", "").strip(),
                    contact_name=company_data.get("contact_name", "").strip(),
                    contact_title=company_data.get("contact_title", "").strip(),
                    contact_email=company_data.get("contact_email", "").strip(),
                    description=company_data.get("description", "").strip()
                )
                
                # Only add companies with essential data
                if company.name and company.contact_name and company.contact_email:
                    companies.append(company)
                    print(f"✅ Added company: {company.name} ({company.contact_name})")
                else:
                    print(f"❌ Skipped company due to missing data: {company.name}")
            
            print(f"📊 Total valid companies: {len(companies)}")
            
            return companies
            
        except Exception as e:
            print(f"❌ Error generating companies with LLM: {e}")
            print(f"Error type: {type(e).__name__}")
            
            # Check if it's a rate limit error
            if "rate" in str(e).lower() or "429" in str(e):
                print("⏱️ Rate limit hit - wait a moment and try again")
                raise Exception(f"Rate limit exceeded. Please wait a moment and try again.")
            else:
                # Try fallback companies instead of failing completely
                print("🔄 Using fallback companies due to LLM error")
                return self._get_fallback_companies(icp_description, num_companies)
    
    def _get_fallback_companies(self, icp_description: str, num_companies: int) -> List[RealCompany]:
        """Fallback to companies that match the ICP description if LLM fails"""
        
        # Parse the ICP description to determine what type of companies to generate
        icp_lower = icp_description.lower()
        
        # Determine country preference
        if any(country in icp_lower for country in ['us', 'usa', 'united states', 'america']):
            country = "US"
        elif any(country in icp_lower for country in ['jp', 'japan', 'japanese']):
            country = "JP"
        elif any(country in icp_lower for country in ['uk', 'britain', 'british']):
            country = "UK"
        elif any(country in icp_lower for country in ['ca', 'canada', 'canadian']):
            country = "CA"
        else:
            country = "US"  # Default to US
        
        # Determine industry preference
        if any(term in icp_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'ml']):
            industry = "Artificial Intelligence"
            companies = self._get_ai_companies(country)
        elif any(term in icp_lower for term in ['gaming', 'game', 'entertainment']):
            industry = "Gaming"
            companies = self._get_gaming_companies(country)
        elif any(term in icp_lower for term in ['vr', 'ar', 'xr', 'virtual reality', 'augmented reality']):
            industry = "VR/AR Technology"
            companies = self._get_vr_companies(country)
        elif any(term in icp_lower for term in ['startup', 'tech', 'technology']):
            industry = "Technology"
            companies = self._get_tech_companies(country)
        else:
            industry = "Technology"
            companies = self._get_tech_companies(country)
        
        return companies[:num_companies]
    
    def _get_ai_companies(self, country: str) -> List[RealCompany]:
        """Get AI companies based on country"""
        if country == "US":
            return [
                RealCompany(
                    name="OpenAI",
                    website="https://openai.com",
                    country="US",
                    industry="Artificial Intelligence",
                    contact_name="Sam Altman",
                    contact_title="CEO",
                    contact_email="sam@openai.com",
                    description="AI research company focused on developing safe artificial general intelligence"
                ),
                RealCompany(
                    name="Anthropic",
                    website="https://anthropic.com",
                    country="US",
                    industry="Artificial Intelligence",
                    contact_name="Dario Amodei",
                    contact_title="CEO",
                    contact_email="dario@anthropic.com",
                    description="AI safety company developing Claude AI assistant"
                ),
                RealCompany(
                    name="Hugging Face",
                    website="https://huggingface.co",
                    country="US",
                    industry="Artificial Intelligence",
                    contact_name="Clem Delangue",
                    contact_title="CEO",
                    contact_email="clem@huggingface.co",
                    description="Open source AI platform and model repository"
                ),
                RealCompany(
                    name="Scale AI",
                    website="https://scale.com",
                    country="US",
                    industry="Artificial Intelligence",
                    contact_name="Alex Wang",
                    contact_title="CEO",
                    contact_email="alex@scale.com",
                    description="Data platform for AI training and validation"
                ),
                RealCompany(
                    name="Cohere",
                    website="https://cohere.com",
                    country="US",
                    industry="Artificial Intelligence",
                    contact_name="Aidan Gomez",
                    contact_title="CEO",
                    contact_email="aidan@cohere.com",
                    description="Enterprise AI platform for natural language processing"
                )
            ]
        else:
            return self._get_tech_companies(country)
    
    def _get_tech_companies(self, country: str) -> List[RealCompany]:
        """Get tech companies based on country"""
        if country == "US":
            return [
                RealCompany(
                    name="Microsoft",
                    website="https://microsoft.com",
                    country="US",
                    industry="Technology",
                    contact_name="Satya Nadella",
                    contact_title="CEO",
                    contact_email="satya.nadella@microsoft.com",
                    description="Technology company focused on cloud computing and productivity software"
                ),
                RealCompany(
                    name="Google",
                    website="https://google.com",
                    country="US",
                    industry="Technology",
                    contact_name="Sundar Pichai",
                    contact_title="CEO",
                    contact_email="sundar@google.com",
                    description="Technology company specializing in search, advertising, and cloud services"
                ),
                RealCompany(
                    name="Apple",
                    website="https://apple.com",
                    country="US",
                    industry="Technology",
                    contact_name="Tim Cook",
                    contact_title="CEO",
                    contact_email="tcook@apple.com",
                    description="Technology company known for consumer electronics and software"
                ),
                RealCompany(
                    name="Meta",
                    website="https://meta.com",
                    country="US",
                    industry="Technology",
                    contact_name="Mark Zuckerberg",
                    contact_title="CEO",
                    contact_email="mark@meta.com",
                    description="Social media and metaverse technology company"
                ),
                RealCompany(
                    name="Tesla",
                    website="https://tesla.com",
                    country="US",
                    industry="Technology",
                    contact_name="Elon Musk",
                    contact_title="CEO",
                    contact_email="elon@tesla.com",
                    description="Electric vehicle and clean energy company"
                )
            ]
        elif country == "JP":
            return [
                RealCompany(
                    name="Sony",
                    website="https://sony.com",
                    country="JP",
                    industry="Technology",
                    contact_name="Kenichiro Yoshida",
                    contact_title="CEO",
                    contact_email="kenichiro.yoshida@sony.com",
                    description="Japanese multinational conglomerate in entertainment and technology"
                ),
                RealCompany(
                    name="Nintendo",
                    website="https://nintendo.com",
                    country="JP",
                    industry="Gaming",
                    contact_name="Shuntaro Furukawa",
                    contact_title="President",
                    contact_email="shuntaro.furukawa@nintendo.com",
                    description="Japanese video game company and console manufacturer"
                ),
                RealCompany(
                    name="SoftBank",
                    website="https://softbank.jp",
                    country="JP",
                    industry="Technology",
                    contact_name="Masayoshi Son",
                    contact_title="CEO",
                    contact_email="masayoshi.son@softbank.jp",
                    description="Japanese multinational conglomerate and technology investment company"
                )
            ]
        else:
            return self._get_ai_companies("US")  # Default to US AI companies
    
    def _get_gaming_companies(self, country: str) -> List[RealCompany]:
        """Get gaming companies based on country"""
        if country == "US":
            return [
                RealCompany(
                    name="Epic Games",
                    website="https://epicgames.com",
                    country="US",
                    industry="Gaming",
                    contact_name="Tim Sweeney",
                    contact_title="CEO",
                    contact_email="tim@epicgames.com",
                    description="Video game developer and publisher, creator of Fortnite"
                ),
                RealCompany(
                    name="Riot Games",
                    website="https://riotgames.com",
                    country="US",
                    industry="Gaming",
                    contact_name="Nicolo Laurent",
                    contact_title="CEO",
                    contact_email="nicolo@riotgames.com",
                    description="Video game developer, creator of League of Legends"
                ),
                RealCompany(
                    name="Blizzard Entertainment",
                    website="https://blizzard.com",
                    country="US",
                    industry="Gaming",
                    contact_name="Mike Ybarra",
                    contact_title="President",
                    contact_email="mike.ybarra@blizzard.com",
                    description="Video game developer and publisher"
                )
            ]
        else:
            return self._get_tech_companies(country)
    
    def _get_vr_companies(self, country: str) -> List[RealCompany]:
        """Get VR/AR companies based on country"""
        if country == "US":
            return [
                RealCompany(
                    name="Meta Reality Labs",
                    website="https://about.meta.com/realitylabs",
                    country="US",
                    industry="VR/AR Technology",
                    contact_name="Andrew Bosworth",
                    contact_title="VP of Reality Labs",
                    contact_email="boz@meta.com",
                    description="VR and AR technology development division of Meta"
                ),
                RealCompany(
                    name="Magic Leap",
                    website="https://magicleap.com",
                    country="US",
                    industry="VR/AR Technology",
                    contact_name="Peggy Johnson",
                    contact_title="CEO",
                    contact_email="peggy@magicleap.com",
                    description="Augmented reality technology company"
                ),
                RealCompany(
                    name="HTC Vive",
                    website="https://vive.com",
                    country="US",
                    industry="VR/AR Technology",
                    contact_name="Cher Wang",
                    contact_title="CEO",
                    contact_email="cher.wang@htc.com",
                    description="Virtual reality hardware and software company"
                )
            ]
        else:
            return self._get_tech_companies(country)
    
    def _fix_json_issues(self, content: str) -> str:
        """Try to fix common JSON formatting issues"""
        import re
        
        # Remove any trailing commas before closing braces/brackets
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        # Fix escaped quotes - unescape them since they're causing issues
        content = content.replace('\\"', '"')
        
        # Fix any remaining quote issues
        content = re.sub(r'(?<!\\)"(?=.*")', r'\\"', content)
        
        return content
    
    def _try_alternative_parsing(self, content: str) -> List[RealCompany]:
        """Try alternative parsing strategies for different response formats"""
        companies = []
        
        try:
            # Try parsing as a list instead of object with companies key
            data = json.loads(content)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        company = RealCompany(
                            name=item.get("name", "").strip(),
                            website=item.get("website", "").strip(),
                            country=item.get("country", "").strip(),
                            industry=item.get("industry", "").strip(),
                            contact_name=item.get("contact_name", "").strip(),
                            contact_title=item.get("contact_title", "").strip(),
                            contact_email=item.get("contact_email", "").strip(),
                            description=item.get("description", "").strip()
                        )
                        if company.name and company.contact_name and company.contact_email:
                            companies.append(company)
                return companies
        except:
            pass
        
        try:
            # Try parsing with different key names
            data = json.loads(content)
            for key in ["companies", "results", "data", "items"]:
                if key in data and isinstance(data[key], list):
                    for item in data[key]:
                        if isinstance(item, dict):
                            company = RealCompany(
                                name=item.get("name", "").strip(),
                                website=item.get("website", "").strip(),
                                country=item.get("country", "").strip(),
                                industry=item.get("industry", "").strip(),
                                contact_name=item.get("contact_name", "").strip(),
                                contact_title=item.get("contact_title", "").strip(),
                                contact_email=item.get("contact_email", "").strip(),
                                description=item.get("description", "").strip()
                            )
                            if company.name and company.contact_name and company.contact_email:
                                companies.append(company)
                    if companies:
                        return companies
        except:
            pass
        
        return companies

    def _extract_companies_manually(self, content: str) -> List[RealCompany]:
        """Extract company information manually when JSON parsing fails"""
        companies = []
        import re
        
        print(f"Attempting manual extraction from content length: {len(content)}")
        
        # Don't clean escaped quotes yet - we need to handle them properly
        # Split content by company blocks - look for both escaped and unescaped patterns
        company_blocks = re.split(r'\{[^}]*["\\"]name["\\"]', content)
        
        print(f"Found {len(company_blocks)} company blocks")
        
        if len(company_blocks) <= 1:
            # Try alternative splitting method
            company_blocks = re.split(r'\{[^}]*"name"', content)
            print(f"Alternative split found {len(company_blocks)} blocks")
        
        for block in company_blocks[1:]:  # Skip first empty block
            try:
                # Extract fields using regex - handle escaped quotes properly
                # The blocks start with ": \"CompanyName" so we need to match that pattern
                # But we need to be more specific to avoid matching "website" from previous fields
                name_match = re.search(r'":\s*\\"([^"]+)\\"', block)
                
                # If that doesn't work, try to find the first quoted string that's not "website"
                if not name_match:
                    # Find all quoted strings and take the first one that's not "website"
                    all_quoted = re.findall(r'\\"([^"]+)\\"', block)
                    for quoted in all_quoted:
                        if quoted != "website" and not quoted.startswith("http"):
                            # Create a proper mock object that behaves like a regex match
                            class MockMatch:
                                def group(self, n):
                                    return quoted
                            name_match = MockMatch()
                            break
                website_match = re.search(r'\\"website\\":\s*\\"([^"]+)\\"', block)
                country_match = re.search(r'\\"country\\":\s*\\"([^"]+)\\"', block)
                industry_match = re.search(r'\\"industry\\":\s*\\"([^"]+)\\"', block)
                contact_name_match = re.search(r'\\"contact_name\\":\s*\\"([^"]+)\\"', block)
                contact_title_match = re.search(r'\\"contact_title\\":\s*\\"([^"]+)\\"', block)
                contact_email_match = re.search(r'\\"contact_email\\":\s*\\"([^"]+)\\"', block)
                description_match = re.search(r'\\"description\\":\s*\\"([^"]+)\\"', block)
                
                if name_match:  # Only add if we have at least a name
                    company = RealCompany(
                        name=name_match.group(1),
                        website=website_match.group(1) if website_match else "",
                        country=country_match.group(1) if country_match else "",
                        industry=industry_match.group(1) if industry_match else "",
                        contact_name=contact_name_match.group(1) if contact_name_match else "",
                        contact_title=contact_title_match.group(1) if contact_title_match else "",
                        contact_email=contact_email_match.group(1) if contact_email_match else "",
                        description=description_match.group(1) if description_match else ""
                    )
                    companies.append(company)
                    print(f"Successfully extracted company: {company.name}")
                else:
                    print(f"No name found in block: {block[:100]}...")
            except Exception as e:
                print(f"Error extracting company from block: {e}")
                continue
        
        # If we couldn't extract any companies, return fallback
        if not companies:
            print("Could not extract companies manually, using fallback")
            return self._get_fallback_companies("technology companies", 5)
        
        return companies
    
    def save_companies_csv(self, companies: List[RealCompany], path: str = "data/real_companies.csv"):
        """Save real companies to CSV file"""
        os.makedirs("data", exist_ok=True)
        
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "title", "company", "website", "email", "country", "industry", "description"])
            
            for company in companies:
                writer.writerow([
                    company.contact_name,
                    company.contact_title,
                    company.name,
                    company.website,
                    company.contact_email,
                    company.country,
                    company.industry,
                    company.description
                ])

def generate_real_companies_from_icp(icp_description: str, num_companies: int = 10) -> List[RealCompany]:
    """Convenience function to generate real companies"""
    generator = RealCompanyGenerator()
    return generator.generate_real_companies(icp_description, num_companies)
