#!/usr/bin/env python3
"""
Quick Outreach App - Mailgun Email Campaign

SETUP INSTRUCTIONS:
1. Install dependencies:
   pip install requests python-dotenv

2. Create .env file in the same directory with:
   MAILGUN_API_KEY=your_mailgun_api_key_here
   MAILGUN_DOMAIN=your_mailgun_domain_here
   FROM_EMAIL=your_email@yourdomain.com

3. Prepare prospects.csv with headers:
   name,title,company,website,email,country

   Sample data:
   name,title,company,website,email,country
   John Smith,CEO,TechCorp,https://techcorp.com,john@techcorp.com,USA
   Jane Doe,CTO,StartupXYZ,https://startupxyz.com,jane@startupxyz.com,Canada

4. Run the script:
   python quick_send.py
"""

import csv
import os
import time
import logging
import requests
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class OutreachApp:
    def __init__(self):
        self.api_key = os.getenv('MAILGUN_API_KEY')
        self.domain = os.getenv('MAILGUN_DOMAIN')
        self.from_email = os.getenv('FROM_EMAIL')
        
        if not self.api_key:
            raise ValueError("MAILGUN_API_KEY environment variable is required")
        if not self.domain:
            raise ValueError("MAILGUN_DOMAIN environment variable is required")
        if not self.from_email:
            raise ValueError("FROM_EMAIL environment variable is required")
        
        self.mailgun_url = f"https://api.mailgun.net/v3/{self.domain}/messages"
        self.rate_limit_delay = 3  # 3 seconds per email for rate limiting
        
    def read_prospects(self, csv_file: str) -> List[Dict[str, str]]:
        """Read prospects from CSV file"""
        prospects = []
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                required_headers = ['name', 'title', 'company', 'website', 'email', 'country']
                
                # Validate headers
                if not all(header in reader.fieldnames for header in required_headers):
                    missing_headers = [h for h in required_headers if h not in reader.fieldnames]
                    raise ValueError(f"Missing required headers: {missing_headers}")
                
                for row_num, row in enumerate(reader, start=2):  # Start at 2 because header is row 1
                    # Skip empty rows
                    if not any(row.values()):
                        continue
                    
                    # Validate required fields
                    if not row.get('email') or not row.get('name') or not row.get('company'):
                        logger.warning(f"Row {row_num}: Skipping incomplete record (missing email, name, or company)")
                        continue
                    
                    prospects.append(row)
                    
            logger.info(f"Successfully loaded {len(prospects)} prospects from {csv_file}")
            return prospects
            
        except FileNotFoundError:
            logger.error(f"CSV file '{csv_file}' not found")
            raise
        except Exception as e:
            logger.error(f"Error reading CSV file: {str(e)}")
            raise
    
    def generate_email_content(self, prospect: Dict[str, str]) -> tuple[str, str]:
        """Generate email subject and body with placeholders replaced"""
        subject = f"Quick intro: Omnilinks × {prospect['company']}"
        
        body = f"""Hi {prospect['name']},

We help fast-growing teams expand in Japan with AI-powered go-to-market.
If helpful, I'd love to share a quick 10-min overview tailored to {prospect['company']}.

Best,
Omnilinks
Unsubscribe: https://yourapp.example.com/unsubscribe"""
        
        return subject, body
    
    def send_email(self, prospect: Dict[str, str]) -> bool:
        """Send email to a single prospect"""
        try:
            subject, body = self.generate_email_content(prospect)
            
            # Prepare email data for Mailgun
            email_data = {
                "from": f"Omnilinks <{self.from_email}>",
                "to": prospect['email'],
                "subject": subject,
                "text": body
            }
            
            # Send email via Mailgun API
            response = requests.post(
                self.mailgun_url,
                auth=("api", self.api_key),
                data=email_data
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Email sent successfully to {prospect['name']} ({prospect['email']}) at {prospect['company']}")
                return True
            else:
                logger.error(f"❌ Failed to send email to {prospect['name']} ({prospect['email']}): Status {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error sending email to {prospect['name']} ({prospect['email']}): {str(e)}")
            return False
    
    def run_campaign(self, csv_file: str = 'prospects.csv'):
        """Run the email campaign"""
        logger.info("🚀 Starting outreach campaign...")
        
        try:
            prospects = self.read_prospects(csv_file)
            
            if not prospects:
                logger.warning("No valid prospects found in CSV file")
                return
            
            successful_sends = 0
            failed_sends = 0
            
            logger.info(f"📧 Sending emails to {len(prospects)} prospects with rate limiting (20 emails/minute)")
            
            for i, prospect in enumerate(prospects, 1):
                logger.info(f"📤 Processing prospect {i}/{len(prospects)}: {prospect['name']} at {prospect['company']}")
                
                if self.send_email(prospect):
                    successful_sends += 1
                else:
                    failed_sends += 1
                
                # Rate limiting: wait between emails (except for the last one)
                if i < len(prospects):
                    logger.info(f"⏳ Rate limiting: waiting {self.rate_limit_delay} seconds...")
                    time.sleep(self.rate_limit_delay)
            
            # Final summary
            logger.info("=" * 50)
            logger.info("📊 CAMPAIGN SUMMARY")
            logger.info("=" * 50)
            logger.info(f"✅ Successful sends: {successful_sends}")
            logger.info(f"❌ Failed sends: {failed_sends}")
            logger.info(f"📈 Success rate: {(successful_sends / len(prospects) * 100):.1f}%")
            logger.info("=" * 50)
            
        except Exception as e:
            logger.error(f"💥 Campaign failed: {str(e)}")
            raise

def main():
    """Main function"""
    try:
        app = OutreachApp()
        app.run_campaign()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())