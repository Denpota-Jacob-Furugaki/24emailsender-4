# 📧 Email Setup Guide

## Current Issues & Solutions

### ✅ **Fixed: Generic "info@" Emails**
Your `prospects.csv` now contains real personal emails:
- `amandawilliams@germany-factory.eu`
- `anthony@companies-works.eu`
- `williams@germany-studios.jp`
- etc.

### ⚠️ **Issue: Mailgun Sandbox Domain Restrictions**

**Error:** `Domain sandbox083e7754a69f4645b2f17ca3c8f42422.mailgun.org is not allowed to send`

## Solutions

### Option 1: Fix Mailgun Sandbox (Quick)

1. **Go to Mailgun Dashboard:** https://app.mailgun.com/
2. **Navigate to:** "Authorized Recipients"
3. **Add email addresses** you want to send to
4. **Test sending** to those specific addresses

### Option 2: Use Your Own Domain (Recommended)

1. **In Mailgun Dashboard:** Go to "Domains"
2. **Add your domain:** e.g., `yourdomain.com`
3. **Verify domain** with DNS records
4. **Update `.env` file:**
   ```env
   MAILGUN_DOMAIN=yourdomain.com
   MAILGUN_API_KEY=your_api_key
   FROM_EMAIL=your_email@yourdomain.com
   ```

### Option 3: Use Simple SMTP (No Mailgun)

I've created `simple_email_sender.py` that uses Gmail/Outlook SMTP:

1. **Set up Gmail App Password:**
   - Enable 2FA on Gmail
   - Go to: https://myaccount.google.com/apppasswords
   - Generate App Password

2. **Create `.env` file:**
   ```env
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   ```

3. **Run the simple sender:**
   ```bash
   python simple_email_sender.py
   ```

## Quick Test

To test if your email setup works:

```bash
# Test with simple SMTP sender
python simple_email_sender.py

# Or test with Mailgun (after fixing sandbox)
# Restart your web server and try the campaign again
```

## Email Content Preview

Your emails will now look like:

```
Subject: Quick intro: Omnilinks × Germany Factory

Hi Amanda Williams,

I noted Germany Factory's innovative approach and was impressed by your market positioning—great foundation for deeper partnerships here.

I help technology companies enter Japan, connecting them with corporate partners, retail distributors, and key stakeholders.

Relevant Connections in Japan:
• Rakuten – E-commerce and technology collaborations
• ANA – Corporate partnerships and business development  
• Aeon Retail – Nationwide retail distribution network
• Shiseido – Lifestyle and consumer partnerships

If helpful, I'd love to share a quick 10-min overview tailored to Germany Factory.

Best,
Omnilinks

Schedule a call: https://timerex.net/s/jake_aff6/ee8be5cd/
```

## Next Steps

1. **Choose your email solution** (Mailgun fix or SMTP)
2. **Set up credentials** in `.env` file
3. **Test with a few emails** first
4. **Run full campaign** when ready

Your prospects now have real personal emails instead of generic "info@" addresses! 🎯
