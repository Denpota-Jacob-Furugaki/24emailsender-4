#!/usr/bin/env python3
"""
Restore company data when it gets corrupted
"""

import csv
import os

def restore_company_data():
    """Restore the company data to the CSV files"""
    
    sample_companies = [
        {
            'name': 'Yuki Tanaka',
            'title': 'CEO',
            'company': 'CyberConnect',
            'website': 'https://cyberconnect.co.jp',
            'email': 'yuki.tanaka@cyberconnect.co.jp',
            'country': 'JP',
            'industry': 'Gaming Technology',
            'description': 'Leading VR gaming platform developer'
        },
        {
            'name': 'Hiroshi Sato',
            'title': 'CTO',
            'company': 'GameForge Studios',
            'website': 'https://gameforge.jp',
            'email': 'hiroshi.sato@gameforge.jp',
            'country': 'JP',
            'industry': 'Game Development',
            'description': 'Mobile game development studio specializing in RPGs'
        },
        {
            'name': 'Akiko Yamamoto',
            'title': 'VP Marketing',
            'company': 'TechVision',
            'website': 'https://techvision.co.jp',
            'email': 'akiko.yamamoto@techvision.co.jp',
            'country': 'JP',
            'industry': 'Technology',
            'description': 'AI and machine learning solutions provider'
        },
        {
            'name': 'Takeshi Nakamura',
            'title': 'Founder',
            'company': 'VirtualReality Inc',
            'website': 'https://vr-inc.jp',
            'email': 'takeshi.nakamura@vr-inc.jp',
            'country': 'JP',
            'industry': 'VR/AR Technology',
            'description': 'Immersive VR experiences and hardware development'
        },
        {
            'name': 'Mika Suzuki',
            'title': 'Head of Business Development',
            'company': 'Digital Dreams',
            'website': 'https://digitaldreams.co.jp',
            'email': 'mika.suzuki@digitaldreams.co.jp',
            'country': 'JP',
            'industry': 'Digital Entertainment',
            'description': 'Digital content creation and distribution platform'
        },
        {
            'name': 'Kenji Ito',
            'title': 'CEO',
            'company': 'Innovation Labs',
            'website': 'https://innovationlabs.jp',
            'email': 'kenji.ito@innovationlabs.jp',
            'country': 'JP',
            'industry': 'Technology Innovation',
            'description': 'Research and development in emerging technologies'
        },
        {
            'name': 'Sakura Kimura',
            'title': 'VP Operations',
            'company': 'FutureTech Solutions',
            'website': 'https://futuretech.jp',
            'email': 'sakura.kimura@futuretech.jp',
            'country': 'JP',
            'industry': 'Technology Solutions',
            'description': 'Enterprise technology solutions and consulting'
        },
        {
            'name': 'Ryo Takahashi',
            'title': 'Founder & CEO',
            'company': 'NextGen Gaming',
            'website': 'https://nextgengaming.jp',
            'email': 'ryo.takahashi@nextgengaming.jp',
            'country': 'JP',
            'industry': 'Gaming',
            'description': 'Next-generation gaming experiences and platforms'
        },
        {
            'name': 'Yui Matsumoto',
            'title': 'Head of Product',
            'company': 'SmartTech Innovations',
            'website': 'https://smarttech.jp',
            'email': 'yui.matsumoto@smarttech.jp',
            'country': 'JP',
            'industry': 'Smart Technology',
            'description': 'IoT and smart technology solutions for businesses'
        }
    ]
    
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Save to real_companies.csv
    with open("data/real_companies.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "title", "company", "website", "email", "country", "industry", "description"])
        
        for company in sample_companies:
            writer.writerow([
                company['name'],
                company['title'],
                company['company'],
                company['website'],
                company['email'],
                company['country'],
                company['industry'],
                company['description']
            ])
    
    # Also save to prospects.csv for compatibility
    with open("prospects.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "title", "company", "website", "email", "country"])
        
        for company in sample_companies:
            writer.writerow([
                company['name'],
                company['title'],
                company['company'],
                company['website'],
                company['email'],
                company['country']
            ])
    
    print(f"✅ Restored {len(sample_companies)} companies to CSV files")
    print("📁 Files updated:")
    print("   - data/real_companies.csv")
    print("   - prospects.csv")

if __name__ == "__main__":
    restore_company_data()

