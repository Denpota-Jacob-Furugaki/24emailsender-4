#!/usr/bin/env python3
"""
Mailgun email sender using your existing configuration
"""

import requests
import csv
import os
from dotenv import load_dotenv
import time

load_dotenv()

class MailgunSender:
    def __init__(self):
        """Initialize with Mailgun settings from .env"""
        self.api_key = os.getenv("MAILGUN_API_KEY")
        self.domain = os.getenv("MAILGUN_DOMAIN")
        self.from_email = os.getenv("FROM_EMAIL")
        
        if not self.api_key or not self.domain:
            print("❌ Mailgun configuration not found in .env file")
            return
        
        self.mailgun_url = f"https://api.mailgun.net/v3/{self.domain}/messages"
        print(f"📧 Using Mailgun domain: {self.domain}")
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email using Mailgun API"""
        try:
            email_data = {
                "from": f"Omnilinks <{self.from_email}>",
                "to": to_email,
                "subject": subject,
                "text": body
            }
            
            response = requests.post(
                self.mailgun_url,
                auth=("api", self.api_key),
                data=email_data
            )
            
            if response.status_code == 200:
                print(f"✅ Email sent successfully to {to_email}")
                return True
            else:
                print(f"❌ Failed to send to {to_email}: Status {response.status_code}")
                print(f"   Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Error sending to {to_email}: {e}")
            return False
    
    def send_campaign(self, prospects_file: str = "prospects.csv") -> dict:
        """Send email campaign to prospects"""
        results = {
            "emails_sent": 0,
            "emails_failed": 0,
            "errors": []
        }
        
        if not self.api_key or not self.domain:
            results["errors"].append("Mailgun configuration not found")
            return results
        
        # Read prospects
        prospects = []
        try:
            with open(prospects_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                prospects = list(reader)
        except FileNotFoundError:
            results["errors"].append(f"Prospects file {prospects_file} not found")
            return results
        
        print(f"📧 Starting Mailgun campaign to {len(prospects)} prospects...")
        
        for i, prospect in enumerate(prospects, 1):
            print(f"\n📤 Sending email {i}/{len(prospects)} to {prospect['name']} at {prospect['email']}")
            
            # Create email content
            subject = f"Quick intro: Omnilinks × {prospect['company']}"
            body = f"""Hi {prospect['name']},

I noted {prospect['company']}'s innovative approach and was impressed by your market positioning—great foundation for deeper partnerships here.

I help technology companies enter Japan, connecting them with corporate partners, retail distributors, and key stakeholders.

Relevant Connections in Japan:
• Rakuten – E-commerce and technology collaborations
• ANA – Corporate partnerships and business development  
• Aeon Retail – Nationwide retail distribution network
• Shiseido – Lifestyle and consumer partnerships

If helpful, I'd love to share a quick 10-min overview tailored to {prospect['company']}.

Best,
Omnilinks

Schedule a call: https://timerex.net/s/jake_aff6/ee8be5cd/
Unsubscribe: https://yourapp.example.com/unsubscribe"""
            
            # Send email
            if self.send_email(prospect['email'], subject, body):
                results["emails_sent"] += 1
            else:
                results["emails_failed"] += 1
                results["errors"].append(f"Failed to send to {prospect['email']}")
            
            # Rate limiting
            if i < len(prospects):
                print("⏳ Waiting 3 seconds before next email...")
                time.sleep(3)
        
        print(f"\n🎉 Campaign completed!")
        print(f"✅ Emails sent: {results['emails_sent']}")
        print(f"❌ Emails failed: {results['emails_failed']}")
        
        return results

def main():
    """Test Mailgun sender"""
    sender = MailgunSender()
    
    if not sender.api_key:
        print("❌ Mailgun not configured. Please check your .env file.")
        return
    
    # Test with a single email first
    test_email = input("Enter a test email address (or press Enter to skip): ").strip()
    
    if test_email:
        print(f"\n🧪 Testing single email to {test_email}")
        success = sender.send_email(
            test_email,
            "Test Email from 24hour Mailer",
            "This is a test email to verify your Mailgun configuration is working."
        )
        
        if success:
            print("✅ Test successful! Running full campaign...")
            results = sender.send_campaign()
        else:
            print("❌ Test failed. Please check your Mailgun configuration.")
            print("💡 Tip: For sandbox domains, add recipients to 'Authorized Recipients' in Mailgun dashboard")
    else:
        print("🚀 Running full campaign...")
        results = sender.send_campaign()
    
    print(f"\n📊 Final Results:")
    print(f"Emails sent: {results['emails_sent']}")
    print(f"Emails failed: {results['emails_failed']}")
    if results['errors']:
        print(f"Errors: {len(results['errors'])}")
        for error in results['errors'][:3]:  # Show first 3 errors
            print(f"  - {error}")

if __name__ == "__main__":
    main()
