import os
import openai
from dotenv import load_dotenv

load_dotenv()

def test_direct():
    print("Testing direct API call...")
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = """Find 2 real gaming companies in Japan. Return JSON like this:
{
    "companies": [
        {
            "name": "Nintendo",
            "website": "https://nintendo.com",
            "country": "JP",
            "industry": "Gaming",
            "contact_name": "Shuntaro Furukawa",
            "contact_title": "President",
            "contact_email": "president@nintendo.com",
            "description": "Video game company"
        }
    ]
}"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        print("API Response:")
        print(content)
        print("\n" + "="*50)
        
        # Try to parse
        import json
        try:
            data = json.loads(content)
            companies = data.get("companies", [])
            print(f"Found {len(companies)} companies")
            for company in companies:
                print(f"- {company.get('name')} ({company.get('contact_name')})")
        except Exception as e:
            print(f"JSON parse error: {e}")
            
    except Exception as e:
        print(f"API error: {e}")

if __name__ == "__main__":
    test_direct()

