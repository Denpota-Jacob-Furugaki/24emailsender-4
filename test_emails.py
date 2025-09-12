#!/usr/bin/env python3
"""Test script for the emails module"""

import emails

# Test context
context = {
    'first_name': 'John',
    'company': 'TechCorp',
    'personal_line': 'your recent work on TechCorp caught my eye',
    'relevant_industry': 'gaming & entertainment',
    'trend_or_need': 'immersive experiences',
    'industry_type': 'entertainment and tech',
    'idea_1': 'Partner with LBE venues',
    'idea_2': 'Launch esports campaigns',
    'idea_3': 'Collaborate with influencers',
    'scheduling_link': 'https://calendly.com/test'
}

# Test the compose_email function
result = emails.compose_email(context)

print("=== EMAIL COMPOSITION TEST ===")
print(f"Subject: {result['subject']}")
print(f"Body:\n{result['body']}")
print("=== TEST COMPLETED ===")
