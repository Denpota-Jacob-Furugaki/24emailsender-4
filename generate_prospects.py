#!/usr/bin/env python3
"""
Generate new prospect data using the ICP generator
"""

from icp import parse_icp, generate_companies, save_companies_csv
import random

def generate_prospects_for_campaign(icp_description: str, num_companies: int = 20):
    """
    Generate prospect companies based on ICP description
    
    Args:
        icp_description: Description of your ideal customer profile
        num_companies: Number of companies to generate
    """
    print(f"Generating {num_companies} companies based on: {icp_description}")
    
    # Parse the ICP description
    filters = parse_icp(icp_description)
    print(f"Extracted filters: {filters}")
    
    # Generate companies
    companies = generate_companies(filters, num_companies)
    
    # Add more realistic contact names and titles
    first_names = ["John", "Jane", "Mike", "Sarah", "David", "Lisa", "Alex", "Emma", "Chris", "Maria", 
                   "Michael", "Jennifer", "Robert", "Jessica", "William", "Ashley", "James", "Emily", 
                   "Christopher", "Amanda", "Daniel", "Stephanie", "Matthew", "Melissa", "Anthony", "Nicole"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
    titles = ["CEO", "CTO", "VP Marketing", "Head of Sales", "Founder", "Product Manager", "Marketing Director", 
              "Sales Director", "VP Engineering", "Chief Technology Officer", "VP Business Development", 
              "Head of Product", "VP Operations", "Chief Marketing Officer", "VP Strategy"]
    
    # Create prospects with contact info
    prospects = []
    for company in companies:
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        title = random.choice(titles)
        
        # Create more realistic email patterns
        domain = company.website.split('//')[1].replace('www.', '')
        email_patterns = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name.lower()}@{domain}",
            f"{first_name[0].lower()}{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name[0].lower()}@{domain}",
            f"{first_name.lower()}@{domain}",
            f"{last_name.lower()}@{domain}"
        ]
        email = random.choice(email_patterns)
        
        prospects.append({
            "name": f"{first_name} {last_name}",
            "title": title,
            "company": company.name,
            "website": company.website,
            "email": email,
            "country": company.country
        })
    
    return prospects

def save_prospects_csv(prospects, filename="prospects.csv"):
    """Save prospects to CSV file"""
    import csv
    
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "title", "company", "website", "email", "country"])
        writer.writeheader()
        writer.writerows(prospects)
    
    print(f"Saved {len(prospects)} prospects to {filename}")

if __name__ == "__main__":
    # Example: Generate prospects for gaming companies in Japan
    icp_description = "gaming companies in Japan, esports, mobile games, entertainment tech"
    
    prospects = generate_prospects_for_campaign(icp_description, 15)
    save_prospects_csv(prospects)
    
    print("\nGenerated prospects:")
    for i, prospect in enumerate(prospects[:5], 1):
        print(f"{i}. {prospect['name']} ({prospect['title']}) at {prospect['company']}")
        print(f"   Email: {prospect['email']}")
        print(f"   Website: {prospect['website']}")
        print()
