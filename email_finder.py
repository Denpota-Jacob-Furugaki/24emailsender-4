#!/usr/bin/env python3
"""
Email finder using external services to get real contact information
"""

import requests
import csv
import os
from typing import List, Dict, Optional

class EmailFinder:
    def __init__(self, hunter_api_key: Optional[str] = None):
        """
        Initialize email finder with API keys
        
        Args:
            hunter_api_key: Hunter.io API key (optional)
        """
        self.hunter_api_key = hunter_api_key or os.getenv('HUNTER_API_KEY')
        self.hunter_base_url = "https://api.hunter.io/v2"
    
    def find_email_with_hunter(self, domain: str, first_name: str, last_name: str) -> Optional[str]:
        """
        Find email using Hunter.io API
        
        Args:
            domain: Company domain (e.g., 'company.com')
            first_name: Contact's first name
            last_name: Contact's last name
            
        Returns:
            Email address if found, None otherwise
        """
        if not self.hunter_api_key:
            print("Hunter.io API key not provided. Skipping email lookup.")
            return None
        
        try:
            # Hunter.io email finder endpoint
            url = f"{self.hunter_base_url}/email-finder"
            params = {
                'domain': domain,
                'first_name': first_name,
                'last_name': last_name,
                'api_key': self.hunter_api_key
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('data', {}).get('email'):
                email = data['data']['email']
                confidence = data['data'].get('confidence', 0)
                print(f"Found email: {email} (confidence: {confidence}%)")
                return email
            else:
                print(f"No email found for {first_name} {last_name} at {domain}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error with Hunter.io API: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None
    
    def find_company_emails(self, domain: str) -> List[Dict[str, str]]:
        """
        Find all emails for a company domain using Hunter.io
        
        Args:
            domain: Company domain
            
        Returns:
            List of email addresses with metadata
        """
        if not self.hunter_api_key:
            print("Hunter.io API key not provided. Skipping email lookup.")
            return []
        
        try:
            # Hunter.io domain search endpoint
            url = f"{self.hunter_base_url}/domain-search"
            params = {
                'domain': domain,
                'api_key': self.hunter_api_key,
                'limit': 10  # Limit to 10 emails per domain
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            emails = []
            
            for email_data in data.get('data', {}).get('emails', []):
                emails.append({
                    'email': email_data.get('value'),
                    'first_name': email_data.get('first_name', ''),
                    'last_name': email_data.get('last_name', ''),
                    'position': email_data.get('position', ''),
                    'confidence': email_data.get('confidence', 0)
                })
            
            print(f"Found {len(emails)} emails for {domain}")
            return emails
            
        except requests.exceptions.RequestException as e:
            print(f"Error with Hunter.io API: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    def enhance_prospects_with_real_emails(self, prospects_file: str, output_file: str = "enhanced_prospects.csv"):
        """
        Enhance existing prospects with real email addresses
        
        Args:
            prospects_file: Path to existing prospects CSV
            output_file: Path to save enhanced prospects
        """
        enhanced_prospects = []
        
        with open(prospects_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            prospects = list(reader)
        
        for prospect in prospects:
            print(f"\nProcessing: {prospect['name']} at {prospect['company']}")
            
            # Extract domain from website
            website = prospect.get('website', '')
            if website.startswith('http'):
                domain = website.split('//')[1].replace('www.', '')
            else:
                domain = website.replace('www.', '')
            
            # Try to find real emails for this domain
            company_emails = self.find_company_emails(domain)
            
            if company_emails:
                # Use the highest confidence email
                best_email = max(company_emails, key=lambda x: x.get('confidence', 0))
                prospect['email'] = best_email['email']
                prospect['email_confidence'] = best_email['confidence']
                print(f"Enhanced with real email: {best_email['email']}")
            else:
                # Keep original email but mark as generic
                prospect['email_confidence'] = 0
                print(f"Keeping original email: {prospect['email']}")
            
            enhanced_prospects.append(prospect)
        
        # Save enhanced prospects
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = list(enhanced_prospects[0].keys())
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(enhanced_prospects)
        
        print(f"\nEnhanced prospects saved to {output_file}")

def main():
    """Example usage of the email finder"""
    
    # Initialize email finder (you'll need to set HUNTER_API_KEY environment variable)
    finder = EmailFinder()
    
    # Example: Find email for a specific person
    email = finder.find_email_with_hunter('openai.com', 'Sam', 'Altman')
    if email:
        print(f"Found email: {email}")
    
    # Example: Find all emails for a company
    emails = finder.find_company_emails('openai.com')
    for email_data in emails:
        print(f"Email: {email_data['email']}, Position: {email_data['position']}, Confidence: {email_data['confidence']}%")
    
    # Example: Enhance existing prospects
    # finder.enhance_prospects_with_real_emails('prospects.csv', 'enhanced_prospects.csv')

if __name__ == "__main__":
    main()
