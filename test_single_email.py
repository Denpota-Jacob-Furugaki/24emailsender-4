#!/usr/bin/env python3
"""
Test sending a single email to verify configuration
"""

from dotenv import load_dotenv
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

load_dotenv()

def test_single_email():
    """Test sending one email to verify setup"""
    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    
    if not sender_email or not sender_password:
        print("❌ SENDER_EMAIL and SENDER_PASSWORD not found in .env file")
        return False
    
    # Test email details
    to_email = input("Enter test email address (your own email): ").strip()
    if not to_email:
        print("❌ No email address provided")
        return False
    
    print(f"📧 Testing email from {sender_email} to {to_email}")
    
    try:
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = to_email
        message["Subject"] = "Test Email from 24hour Mailer"
        
        body = """This is a test email from your 24hour Mailer setup.

If you receive this email, your SMTP configuration is working correctly!

Best regards,
24hour Mailer System"""
        
        message.attach(MIMEText(body, "plain"))
        
        # Try Gmail first
        print("🔄 Trying Gmail SMTP...")
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls(context=context)
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            print("✅ Email sent successfully via Gmail!")
            return True
        except Exception as e:
            print(f"❌ Gmail failed: {e}")
        
        # Try Outlook as fallback
        print("🔄 Trying Outlook SMTP...")
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP("smtp-mail.outlook.com", 587) as server:
                server.starttls(context=context)
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, to_email, message.as_string())
            print("✅ Email sent successfully via Outlook!")
            return True
        except Exception as e:
            print(f"❌ Outlook failed: {e}")
        
        print("❌ Both Gmail and Outlook failed. Please check your credentials.")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Single Email Test")
    print("This will send one test email to verify your configuration.")
    print()
    
    success = test_single_email()
    
    if success:
        print("\n🎉 Test successful! Your email configuration is working.")
        print("You can now run the full campaign with: py simple_email_sender.py")
    else:
        print("\n❌ Test failed. Please check your email configuration.")
        print("Make sure:")
        print("1. 2FA is enabled on your Gmail account")
        print("2. You're using an App Password (not your regular password)")
        print("3. The App Password is correct in your .env file")
