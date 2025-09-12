"""
Email composition module for outreach campaigns.
Provides compose_email function that generates subject and body using Jinja2 templates.
"""

from jinja2 import Environment, FileSystemLoader
from typing import Dict, Any
import os
from pathlib import Path


def compose_email(context: Dict[str, Any]) -> Dict[str, str]:
    """
    Compose email using Jinja2 template with provided context.
    
    Args:
        context: Dictionary containing email template variables
        
    Returns:
        Dictionary with 'subject', 'body', and 'cc' keys
        
    Required context keys:
        - first_name: Recipient's first name
        - company: Company name
        - company_work: Description of company's work
        - company_impression: What impressed about the company
        - relevant_industry: Industry context
        - market_trend: Current market trend
        - industry_type: Type of industry
        - idea_1, idea_2, idea_3: Three idea bullets
        - scheduling_link: Link for scheduling meeting
    """
    
    # Validate required keys
    required_keys = [
        'first_name', 'company', 'company_work', 'company_impression', 'market_opportunity',
        'industry_type', 'relevant_connections', 'connection_1', 'connection_2', 'connection_3', 'connection_4', 'scheduling_link'
    ]
    
    # Set defaults for missing keys
    defaults = {
        'first_name': 'Team',
        'company': 'your company',
        'company_work': 'innovative solutions',
        'company_impression': 'your innovative approach and market positioning',
        'market_opportunity': 'market expansion and partnerships',
        'industry_type': 'technology',
        'relevant_connections': 'corporate partners, retail distributors, and key stakeholders',
        'connection_1': 'Rakuten – E-commerce and technology collaborations',
        'connection_2': 'ANA – Corporate partnerships and business development',
        'connection_3': 'Aeon Retail – Nationwide retail distribution network',
        'connection_4': 'Shiseido – Lifestyle and consumer partnerships',
        'scheduling_link': 'https://timerex.net/s/jake_aff6/ee8be5cd/'
    }
    
    # Apply defaults for missing keys
    for key in required_keys:
        if key not in context or not context[key]:
            context[key] = defaults[key]
    
    # Setup Jinja2 environment
    template_dir = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(template_dir))
    
    try:
        # Load the email template
        template = env.get_template("email.jinja2")
        
        # Render the template
        rendered_content = template.render(**context)
        
        # Split into subject and body
        lines = rendered_content.strip().split('\n')
        subject = lines[0] if lines else f"Quick intro: Omnilinks × {context['company']}"
        body = '\n'.join(lines[1:]) if len(lines) > 1 else rendered_content
        
        return {
            'subject': subject,
            'body': body,
            'cc': 'joseph@omnilinks-group.com'
        }
        
    except Exception as e:
        # Fallback if template rendering fails
        fallback_subject = f"Quick intro: Omnilinks × {context['company']}"
        fallback_body = f"""Hi {context['first_name']},

I noted {context['company']}'s {context['company_work']} and was impressed by {context['company_impression']}—great foundation for deeper {context['market_opportunity']} here.

I help {context['industry_type']} companies enter Japan, connecting them with {context['relevant_connections']}.

Relevant Connections in Japan:
{context['connection_1']}
{context['connection_2']}
{context['connection_3']}
{context['connection_4']}

Monthly Rate Plans

Base Fee – 1,000 USD (Market Connection Support)
- Introductions to potential partners
- Initial outreach and communication
- Arranging discovery meetings

POC & Implementation – 3,000 USD (Proof of Concept / Implementation Facilitation)
- Base Fee services, plus:
- POC and implementation facilitation
- Translation of documents
- Meeting support with stakeholders

Post-Implementation – 6,000 USD~ (Customer Success & Aftercare)
- All previous services, plus:
- Acting as a local contact point
- Managing feedback, issue resolution
- Proposing upsell and retention

Commissions will be added to the contract when a deal is signed. Minimum contract term for all plans is 3 months. Prices exclude tax.

Would you be open to a 20-minute call next week (JST) to discuss partnership opportunities?

You can book a time directly via my scheduling link:

{context['scheduling_link']}

Best regards,


Denpota Jacob Furugaki / 古垣伝法太<br>
E-mail: jake@omnilinks-group.com<br>
HP: https://www.omnilinks-group.com/home-jp"""
        
        return {
            'subject': fallback_subject,
            'body': fallback_body,
            'cc': 'joseph@omnilinks-group.com'
        }
