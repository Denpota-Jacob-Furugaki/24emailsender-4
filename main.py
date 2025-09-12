from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import csv
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
import emails
from icp import parse_icp, generate_companies, save_companies_csv
from real_companies import RealCompanyGenerator

app = FastAPI(title="Outreach Email Campaign", version="1.0.0")

# Load environment variables
load_dotenv()

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

class Prospect(BaseModel):
    name: str
    title: str
    company: str
    website: str
    email: str
    country: str
    personalization: Optional[str] = ""

class EmailPreview(BaseModel):
    prospect: Prospect
    subject: str
    body: str
    cc: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with upload form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload-csv")
async def upload_csv(request: Request, csv_file: str = Form(...)):
    """Process uploaded CSV and redirect to preview"""
    # In a real app, you'd handle file upload here
    # For now, we'll assume the CSV is already in the directory
    return RedirectResponse(url="/preview", status_code=303)

@app.get("/preview", response_class=HTMLResponse)
async def preview_emails(request: Request):
    """Preview the first 5 emails with enhanced personalization"""
    try:
        prospects = load_prospects_from_csv("prospects.csv")
        email_previews = []
        
        # Get scheduling link from environment or use default
        scheduling_link = os.getenv("SCHEDULING_LINK", "https://timerex.net/s/jake_aff6/ee8be5cd/")
        
        for prospect in prospects[:5]:  # First 5 only
            # Ensure company has name and website
            if not prospect.company or not prospect.website:
                continue
                
            # Build detailed context for the new email template
            context = {
                'first_name': prospect.name.split()[0] if prospect.name else "Team",
                'company': prospect.company,
                'company_work': get_company_work_description(prospect),
                'company_impression': get_company_impression(prospect),
                'market_opportunity': get_market_opportunity(prospect),
                'industry_type': get_industry_type(prospect),
                'relevant_connections': get_relevant_connections(prospect),
                'connection_1': get_connection_1(prospect),
                'connection_2': get_connection_2(prospect),
                'connection_3': get_connection_3(prospect),
                'connection_4': get_connection_4(prospect),
                'scheduling_link': scheduling_link
            }
            
            # Generate email using the emails module
            email_content = emails.compose_email(context)
            
            email_previews.append(EmailPreview(
                prospect=prospect,
                subject=email_content['subject'],
                body=email_content['body'],
                cc=email_content['cc']
            ))
        
        return templates.TemplateResponse("preview.html", {
            "request": request,
            "email_previews": email_previews,
            "total_prospects": len(prospects)
        })
    
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="prospects.csv not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading prospects: {str(e)}")

@app.post("/generate-icp")
async def generate_icp(icp_prompt: str = Form(...), max_companies: int = Form(10)):
    """Generate real companies from ICP description using ChatGPT and redirect to companies table"""
    try:
        # Use ChatGPT to generate real companies
        generator = RealCompanyGenerator()
        real_companies = generator.generate_real_companies(icp_prompt, max_companies or 10)
        
        # Check if we got valid companies
        if not real_companies or len(real_companies) == 0:
            print("No companies generated, using fallback...")
            raise Exception("No companies generated")
        
        print(f"Generated {len(real_companies)} companies")
        for i, company in enumerate(real_companies):
            print(f"Company {i+1}: {company.name} - {company.contact_name} - {company.contact_email}")
        
        # Check if companies have valid data
        valid_companies = [c for c in real_companies if c.name and c.contact_name and c.contact_email]
        print(f"Valid companies: {len(valid_companies)} out of {len(real_companies)}")
        
        if len(valid_companies) == 0:
            print("No valid companies generated, using fallback...")
            print("Invalid companies details:")
            for i, company in enumerate(real_companies):
                print(f"  {i+1}. Name: '{company.name}', Contact: '{company.contact_name}', Email: '{company.contact_email}'")
            raise Exception("No valid companies generated")
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save real companies to CSV
        generator.save_companies_csv(valid_companies, path="data/real_companies.csv")
        
        # Also save in the old format for compatibility
        with open("prospects.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "title", "company", "website", "email", "country"])
            for company in valid_companies:
                writer.writerow([
                    company.contact_name,
                    company.contact_title,
                    company.name,
                    company.website,
                    company.contact_email,
                    company.country
                ])
        
        # Redirect to companies table view
        return RedirectResponse(url="/companies", status_code=303)
    
    except Exception as e:
        # If ChatGPT fails, use fallback companies
        print(f"ChatGPT generation failed: {e}")
        print("Using fallback companies...")
        
        # Create fallback companies
        fallback_companies = [
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
        
        # Save fallback companies to CSV
        with open("data/real_companies.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "title", "company", "website", "email", "country", "industry", "description"])
            for company in fallback_companies:
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
        
        # Also save in the old format for compatibility
        with open("prospects.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "title", "company", "website", "email", "country"])
            for company in fallback_companies:
                writer.writerow([
                    company['name'],
                    company['title'],
                    company['company'],
                    company['website'],
                    company['email'],
                    company['country']
                ])
        
        # Redirect to companies table view
        return RedirectResponse(url="/companies", status_code=303)

@app.get("/companies", response_class=HTMLResponse)
async def view_companies(request: Request):
    """Display generated companies in a table format"""
    try:
        # Load companies from the generated CSV
        companies = []
        csv_file = "data/real_companies.csv" if os.path.exists("data/real_companies.csv") else "data/companies.csv"
        
        if os.path.exists(csv_file):
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row.get('company'):  # Skip empty rows
                        companies.append({
                            'name': row.get('name', ''),
                            'title': row.get('title', ''),
                            'company': row.get('company', ''),
                            'website': row.get('website', ''),
                            'email': row.get('email', ''),
                            'country': row.get('country', ''),
                            'industry': row.get('industry', ''),
                            'description': row.get('description', '')
                        })
        
        return templates.TemplateResponse("companies.html", {
            "request": request,
            "companies": companies,
            "total_companies": len(companies)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading companies: {str(e)}")

@app.post("/send-campaign")
async def send_campaign(request: Request):
    """Send the email campaign using Mailgun"""
    try:
        # Check if Mailgun is configured
        mailgun_api_key = os.getenv("MAILGUN_API_KEY")
        mailgun_domain = os.getenv("MAILGUN_DOMAIN")
        from_email = os.getenv("FROM_EMAIL")
        
        if not mailgun_api_key or not mailgun_domain or not from_email:
            return {
                "message": "Email sending not configured. Please set MAILGUN_API_KEY, MAILGUN_DOMAIN, and FROM_EMAIL in your .env file.",
                "emails_sent": 0,
                "error": "Missing Mailgun configuration"
            }
        
        # Load prospects from CSV
        prospects = load_prospects_from_csv("prospects.csv")
        
        if not prospects:
            return {
                "message": "No prospects found to send emails to",
                "emails_sent": 0,
                "error": "No prospects available"
            }
        
        successful_sends = 0
        failed_sends = 0
        errors = []
        
        # Get scheduling link from environment or use default
        scheduling_link = os.getenv("SCHEDULING_LINK", "https://timerex.net/s/jake_aff6/ee8be5cd/")
        
        for prospect in prospects:
            try:
                # Build context for email generation
                context = {
                    'first_name': prospect.name.split()[0] if prospect.name else "Team",
                    'company': prospect.company,
                    'company_work': get_company_work_description(prospect),
                    'company_impression': get_company_impression(prospect),
                    'market_opportunity': get_market_opportunity(prospect),
                    'industry_type': get_industry_type(prospect),
                    'relevant_connections': get_relevant_connections(prospect),
                    'connection_1': get_connection_1(prospect),
                    'connection_2': get_connection_2(prospect),
                    'connection_3': get_connection_3(prospect),
                    'connection_4': get_connection_4(prospect),
                    'scheduling_link': scheduling_link
                }
                
                # Generate email content using the emails module
                email_content = emails.compose_email(context)
                
                # Prepare Mailgun API request
                import requests
                
                mailgun_url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"
                
                # Prepare email data
                email_data = {
                    "from": f"Denpota Jacob Furugaki <{from_email}>",
                    "to": prospect.email,
                    "subject": email_content['subject'],
                    "html": email_content['body']
                }
                
                # Add CC if specified
                if email_content.get('cc'):
                    email_data["cc"] = email_content['cc']
                
                # Send email via Mailgun API
                response = requests.post(
                    mailgun_url,
                    auth=("api", mailgun_api_key),
                    data=email_data
                )
                
                if response.status_code == 200:
                    successful_sends += 1
                    print(f"✅ Email sent successfully to {prospect.name} ({prospect.email}) at {prospect.company}")
                else:
                    failed_sends += 1
                    error_msg = f"Failed to send to {prospect.email}: Status {response.status_code} - {response.text}"
                    errors.append(error_msg)
                    print(f"❌ {error_msg}")
                
                # Rate limiting - wait 3 seconds between emails
                import time
                time.sleep(3)
                
            except Exception as e:
                failed_sends += 1
                error_msg = f"Error sending to {prospect.email}: {str(e)}"
                errors.append(error_msg)
                print(f"❌ {error_msg}")
        
        return {
            "message": f"Campaign completed. {successful_sends} emails sent successfully, {failed_sends} failed.",
            "emails_sent": successful_sends,
            "emails_failed": failed_sends,
            "total_prospects": len(prospects),
            "errors": errors[:5] if errors else []  # Return first 5 errors
        }
        
    except Exception as e:
        return {
            "message": f"Campaign failed: {str(e)}",
            "emails_sent": 0,
            "error": str(e)
        }

def load_prospects_from_csv(csv_file: str) -> List[Prospect]:
    """Load prospects from CSV file"""
    prospects = []
    
    with open(csv_file, 'r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        required_headers = ['name', 'title', 'company', 'website', 'email', 'country']
        
        # Validate headers
        if not all(header in reader.fieldnames for header in required_headers):
            missing_headers = [h for h in required_headers if h not in reader.fieldnames]
            raise ValueError(f"Missing required headers: {missing_headers}")
        
        for row in reader:
            # Skip empty rows
            if not any(row.values()):
                continue
            
            # Validate required fields
            if not row.get('email') or not row.get('name') or not row.get('company'):
                continue
            
            prospects.append(Prospect(**row))
    
    return prospects

def get_company_work_description(prospect: Prospect) -> str:
    """Get description of what the company does"""
    # This would ideally use AI to analyze the company, but for now use industry-based defaults
    industry = getattr(prospect, 'industry', '').lower()
    if 'tech' in industry or 'software' in industry:
        return "innovative technology solutions"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "gaming and entertainment experiences"
    elif 'vr' in industry or 'ar' in industry or 'xr' in industry:
        return "immersive VR/AR experiences"
    else:
        return "innovative solutions"

def get_company_impression(prospect: Prospect) -> str:
    """Get what impressed about the company"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'tech' in industry:
        return "how you're making technology accessible and user-friendly"
    elif 'gaming' in industry:
        return "your creative approach to gaming experiences"
    elif 'vr' in industry or 'ar' in industry:
        return "your innovative approach to immersive technology"
    else:
        return "your innovative approach and market positioning"

def get_market_opportunity(prospect: Prospect) -> str:
    """Get market opportunity description"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'health' in industry or 'wellness' in industry or 'fitness' in industry:
        return "corporate wellness and retail expansion"
    elif 'tech' in industry or 'software' in industry:
        return "enterprise partnerships and market expansion"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "gaming partnerships and content localization"
    elif 'vr' in industry or 'ar' in industry:
        return "immersive technology adoption and partnerships"
    elif 'retail' in industry or 'ecommerce' in industry:
        return "retail partnerships and distribution expansion"
    else:
        return "market expansion and strategic partnerships"

def get_relevant_connections(prospect: Prospect) -> str:
    """Get relevant connections description"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'health' in industry or 'wellness' in industry or 'fitness' in industry:
        return "corporate wellness programs, retail distributors, and healthcare providers"
    elif 'tech' in industry or 'software' in industry:
        return "enterprise partners, technology integrators, and business development teams"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "gaming publishers, esports teams, and entertainment venues"
    elif 'vr' in industry or 'ar' in industry:
        return "entertainment venues, theme parks, and enterprise training programs"
    elif 'retail' in industry or 'ecommerce' in industry:
        return "retail chains, e-commerce platforms, and distribution networks"
    else:
        return "corporate partners, retail distributors, and key stakeholders"

def get_industry_type(prospect: Prospect) -> str:
    """Get industry type for the template"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'tech' in industry:
        return "technology"
    elif 'gaming' in industry:
        return "gaming"
    elif 'vr' in industry or 'ar' in industry:
        return "immersive technology"
    else:
        return "technology"

def get_connection_1(prospect: Prospect) -> str:
    """Get first relevant connection"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'health' in industry or 'wellness' in industry or 'fitness' in industry:
        return "Rakuten – E-commerce and wellness collaborations"
    elif 'tech' in industry or 'software' in industry:
        return "Rakuten – E-commerce and technology collaborations"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "Bandai Namco – Gaming and entertainment partnerships"
    elif 'vr' in industry or 'ar' in industry:
        return "Sony – VR/AR technology and entertainment collaborations"
    elif 'retail' in industry or 'ecommerce' in industry:
        return "Rakuten – E-commerce platform and retail partnerships"
    else:
        return "Rakuten – E-commerce and technology collaborations"

def get_connection_2(prospect: Prospect) -> str:
    """Get second relevant connection"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'health' in industry or 'wellness' in industry or 'fitness' in industry:
        return "ANA – Corporate wellness and travel health programs"
    elif 'tech' in industry or 'software' in industry:
        return "ANA – Corporate partnerships and business development"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "ANA – Entertainment and travel partnerships"
    elif 'vr' in industry or 'ar' in industry:
        return "ANA – Corporate training and immersive experiences"
    elif 'retail' in industry or 'ecommerce' in industry:
        return "ANA – Corporate partnerships and business development"
    else:
        return "ANA – Corporate partnerships and business development"

def get_connection_3(prospect: Prospect) -> str:
    """Get third relevant connection"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'health' in industry or 'wellness' in industry or 'fitness' in industry:
        return "Aeon Retail – Nationwide retail distribution network"
    elif 'tech' in industry or 'software' in industry:
        return "Aeon Retail – Nationwide retail distribution network"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "Aeon Retail – Gaming retail and entertainment venues"
    elif 'vr' in industry or 'ar' in industry:
        return "Aeon Retail – VR/AR retail experiences and distribution"
    elif 'retail' in industry or 'ecommerce' in industry:
        return "Aeon Retail – Nationwide retail distribution network"
    else:
        return "Aeon Retail – Nationwide retail distribution network"

def get_connection_4(prospect: Prospect) -> str:
    """Get fourth relevant connection"""
    industry = getattr(prospect, 'industry', '').lower()
    if 'health' in industry or 'wellness' in industry or 'fitness' in industry:
        return "Shiseido – Wellness and lifestyle partnerships"
    elif 'tech' in industry or 'software' in industry:
        return "Shiseido – Lifestyle and consumer partnerships"
    elif 'gaming' in industry or 'entertainment' in industry:
        return "Shiseido – Lifestyle and entertainment collaborations"
    elif 'vr' in industry or 'ar' in industry:
        return "Shiseido – Lifestyle and immersive experience partnerships"
    elif 'retail' in industry or 'ecommerce' in industry:
        return "Shiseido – Lifestyle and consumer partnerships"
    else:
        return "Shiseido – Lifestyle and consumer partnerships"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

