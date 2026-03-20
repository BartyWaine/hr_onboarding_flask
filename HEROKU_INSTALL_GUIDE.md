# 🚀 Heroku Installation & Deployment Guide

## Step 1: Install Heroku CLI

### Option A: Direct Download (Recommended)
1. Go to: https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli
2. Click "Download and install" for Windows
3. Run the installer (.exe file)
4. Restart your command prompt

### Option B: Using Chocolatey
```cmd
choco install heroku-cli
```

### Option C: Using Scoop
```cmd
scoop install heroku
```

## Step 2: Verify Installation
```cmd
heroku --version
```

## Step 3: Login to Heroku
```cmd
heroku login
```
(This will open your browser for authentication)

## Step 4: Deploy Your HR Dashboard
```cmd
cd d:\hr_onboarding_flask
git init
git add .
git commit -m "Initial commit"
heroku create your-hr-dashboard
git push heroku main
```

## Step 5: Set Environment Variables
```cmd
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key-here
```

## Your Website Will Be Live At:
https://your-hr-dashboard.herokuapp.com

## Login Credentials:
- Username: admin
- Password: admin123

## Features Available:
✅ 16 Active Employees
✅ 3,400 HR Dataset Records
✅ 104 Tasks, 45 Policies, 45 Training Programs
✅ Complete Analytics Dashboard
✅ Mobile-responsive design

## Troubleshooting:
- If git is not installed, download from: https://git-scm.com/download/win
- If deployment fails, check logs: `heroku logs --tail`
- For help: `heroku help`

🎉 Your HR Onboarding Dashboard will be live and accessible worldwide!