# 🚀 GitHub Actions Newsletter Setup Guide

**Complete setup in ~8 minutes!** This guide will get your AI newsletter running automatically in the cloud for **FREE**.

## 📋 What You'll Get

- ✅ **Completely free** newsletter automation
- ✅ **Runs every weekday at 7 AM Eastern**
- ✅ **No hardware needed** - runs in GitHub's cloud
- ✅ **Reliable delivery** - GitHub's servers are super stable
- ✅ **Easy to manage** - view logs, manually trigger, modify schedule

---

## 🎯 Step-by-Step Setup

### Step 1: Create GitHub Account (2 minutes)

1. Go to [github.com](https://github.com)
2. Click "Sign up" 
3. Choose a username and create account
4. **No payment required** - we're using the free tier

### Step 2: Create Repository (1 minute)

1. Click the **"+"** in top right → **"New repository"**
2. **Repository name**: `ai-newsletter` (or whatever you prefer)
3. **Make sure it's PUBLIC** (this keeps it free)
4. ✅ Check **"Add a README file"**
5. Click **"Create repository"**

### Step 3: Upload Newsletter Files (3 minutes)

**Option A: Drag & Drop (Easiest)**
1. In your new repository, click **"uploading an existing file"**
2. **Drag and drop ALL these files** from your AI Newsletter folder:
   ```
   📁 .github/workflows/newsletter.yml
   📄 newsletter_scheduler_github.py
   📄 enhanced_newsletter_generator.py
   📄 config.py
   📄 requirements.txt
   📁 utils/ (entire folder)
   ```
3. Scroll down, add commit message: "Add newsletter files"
4. Click **"Commit changes"**

**Option B: GitHub Desktop (If you prefer)**
1. Download GitHub Desktop
2. Clone your repository
3. Copy all the files above into the folder
4. Commit and push

### Step 4: Add Email Secrets (3 minutes)

This is where you securely store your email credentials.

1. In your repository, click **"Settings"** tab
2. In left sidebar, click **"Secrets and variables"** → **"Actions"**
3. Click **"New repository secret"** and add each of these:

**Required Secrets:**
```
Name: EMAIL_FROM
Value: your-email@gmail.com

Name: EMAIL_TO  
Value: recipient@gmail.com

Name: EMAIL_USER
Value: your-email@gmail.com

Name: EMAIL_PASSWORD
Value: your-gmail-app-password (see below)

Name: SMTP_SERVER
Value: smtp.gmail.com

Name: SMTP_PORT
Value: 465
```

**Optional Secrets (for better AI summaries):**
```
Name: OPENAI_API_KEY
Value: your-openai-key (if you have one)

Name: USE_EXTERNAL_LLM
Value: true (if you added OpenAI key)

Name: PREFERRED_LLM
Value: openai (if you added OpenAI key)
```

### Step 5: Get Gmail App Password (2 minutes)

**You need an "App Password" for Gmail (not your regular password):**

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **"Security"** in left sidebar
3. Under "Signing in to Google", click **"2-Step Verification"**
4. **Enable 2-Step Verification** if not already enabled
5. Go back to Security, click **"App passwords"**
6. Select **"Mail"** and **"Other"**, name it "AI Newsletter"
7. **Copy the 16-character password** (like: `abcd efgh ijkl mnop`)
8. **Use this as your EMAIL_PASSWORD secret** (not your regular Gmail password)

### Step 6: Enable the Workflow (30 seconds)

1. In your repository, click **"Actions"** tab
2. You should see "AI Newsletter Daily Scheduler"
3. Click **"Enable workflow"** if prompted
4. Click **"Run workflow"** → **"Run workflow"** to test it

---

## 🎉 You're Done!

Your newsletter will now automatically:
- ✅ **Run every weekday at 7 AM Eastern**
- ✅ **Skip weekends and holidays**
- ✅ **Send you email notifications**
- ✅ **Retry if something fails**

---

## 🛠️ Managing Your Newsletter

### View Logs
1. Go to **"Actions"** tab in your repository
2. Click on any run to see detailed logs
3. Download artifacts to see generated newsletter files

### Manual Run
1. Go to **"Actions"** tab
2. Click **"AI Newsletter Daily Scheduler"**
3. Click **"Run workflow"**
4. Choose options:
   - **Force run**: Ignore schedule/holidays
   - **Dry run**: Generate but don't send email

### Modify Schedule
Edit `.github/workflows/newsletter.yml`:
```yaml
# Change these cron expressions for different times
- cron: '0 11 * * 1-5'  # 11 AM UTC = 7 AM EDT
- cron: '0 12 * * 1-5'  # 12 PM UTC = 7 AM EST
```

### Stop Newsletter
1. Go to **"Actions"** tab
2. Click **"AI Newsletter Daily Scheduler"**
3. Click **"..."** → **"Disable workflow"**

---

## 🔧 Troubleshooting

### Newsletter Not Sending?
1. Check **"Actions"** tab for error messages
2. Verify your Gmail App Password is correct
3. Make sure 2-Step Verification is enabled on Gmail
4. Check that all required secrets are added

### Want to Test First?
1. Go to **"Actions"** → **"Run workflow"**
2. Check **"Dry run"** option
3. This generates newsletter without sending email

### Need Help?
- Check the **"Actions"** logs for detailed error messages
- Verify all secrets are spelled correctly
- Make sure your Gmail App Password is the 16-character one

---

## 💰 Cost Breakdown

- **GitHub Actions**: FREE (2,000 minutes/month included)
- **Your usage**: ~5 minutes per newsletter × 22 weekdays = 110 minutes/month
- **You're using**: ~5% of free allowance
- **Total cost**: $0.00 forever! 🎉

---

## 🎯 Next Steps

Once it's working:
1. **Customize the newsletter** by editing `enhanced_newsletter_generator.py`
2. **Adjust the schedule** if needed
3. **Add more email recipients** in the EMAIL_TO secret (comma-separated)
4. **Monitor the first few runs** to make sure everything works perfectly

**Your newsletter is now running in the cloud! 🌟**

---

## 📞 Quick Reference

**Repository Settings**: `Settings` → `Secrets and variables` → `Actions`
**View Runs**: `Actions` tab
**Manual Run**: `Actions` → `AI Newsletter Daily Scheduler` → `Run workflow`
**Logs**: Click any run in the Actions tab
**Disable**: `Actions` → `AI Newsletter Daily Scheduler` → `...` → `Disable workflow`

**You did it! Your AI newsletter is now fully automated! 🚀📧**
