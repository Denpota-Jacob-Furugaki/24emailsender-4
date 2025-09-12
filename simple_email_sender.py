#!/usr/bin/env python3
"""
Simple email sender that works without Mailgun
Uses SMTP for sending emails (Gmail, Outlook, etc.)
"""

import smtplib
import ssl
import csv
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict
import time

class SimpleEmailSender:
    def __init__(self):
        """Initialize with SMTP settings"""
        # Gmail SMTP settings (you can change to your email provider)
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("SENDER_EMAIL")  # Your email
        self.sender_password = os.getenv("SENDER_PASSWORD")  # Your app password
        
        if not self.sender_email or not self.sender_password:
            print("⚠️  Please set SENDER_EMAIL and SENDER_PASSWORD environment variables")
            print("   For Gmail: Use an App Password (not your regular password)")
            print("   Enable 2FA and generate App Password at: https://myaccount.google.com/apppasswords")
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email using SMTP"""
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject
            
            # Add body to email
            message.attach(MIMEText(body, "plain"))
            
            # Create secure connection and send email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            print(f"✅ Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email to {to_email}: {e}")
            return False
    
    def send_campaign(self, prospects_file: str = "prospects.csv") -> Dict:
        """Send email campaign to all prospects"""
        results = {
            "emails_sent": 0,
            "emails_failed": 0,
            "errors": []
        }
        
        if not self.sender_email or not self.sender_password:
            results["errors"].append("Email configuration not set. Please set SENDER_EMAIL and SENDER_PASSWORD")
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
        
        print(f"📧 Starting email campaign to {len(prospects)} prospects...")
        
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
            
            # Rate limiting - wait between emails
            if i < len(prospects):
                print("⏳ Waiting 3 seconds before next email...")
                time.sleep(3)
        
        print(f"\n🎉 Campaign completed!")
        print(f"✅ Emails sent: {results['emails_sent']}")
        print(f"❌ Emails failed: {results['emails_failed']}")
        
        return results

def main():
    """Example usage"""
    sender = SimpleEmailSender()
    results = sender.send_campaign()
    
    print(f"\n📊 Final Results:")
    print(f"Emails sent: {results['emails_sent']}")
    print(f"Emails failed: {results['emails_failed']}")
    if results['errors']:
        print(f"Errors: {len(results['errors'])}")
        for error in results['errors']:
            print(f"  - {error}")

if __name__ == "__main__":
    main()
