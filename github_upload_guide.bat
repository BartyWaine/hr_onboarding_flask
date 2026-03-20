@echo off
echo 🚀 TechCorp HR Portal - GitHub Upload & Deployment
echo.
echo This will help you upload to GitHub and deploy your website!
echo.
echo 📋 What we'll do:
echo 1. Open GitHub to create repository
echo 2. Open your project folder for easy upload
echo 3. Open Render for deployment
echo 4. Guide you through each step
echo.
pause

echo 🌐 Opening GitHub...
start https://github.com/new

echo 📁 Opening your project folder...
start explorer "d:\hr_onboarding_flask"

echo ⏳ Waiting 5 seconds for GitHub to load...
timeout /t 5 /nobreak >nul

echo 🚀 Opening Render...
start https://render.com

echo.
echo 📋 STEP-BY-STEP INSTRUCTIONS:
echo.
echo ═══════════════════════════════════════════════════════════════
echo 📁 STEP 1: CREATE GITHUB REPOSITORY
echo ═══════════════════════════════════════════════════════════════
echo.
echo In the GitHub tab that just opened:
echo 1. Repository name: hr-onboarding-dashboard
echo 2. Description: TechCorp HR Onboarding Portal
echo 3. Make it Public
echo 4. Click "Create repository"
echo.
echo ═══════════════════════════════════════════════════════════════
echo 📤 STEP 2: UPLOAD YOUR FILES
echo ═══════════════════════════════════════════════════════════════
echo.
echo After creating the repository:
echo 1. Click "uploading an existing file"
echo 2. Drag ALL files from the folder that opened
echo 3. Or click "choose your files" and select all
echo 4. Commit message: "Initial commit - TechCorp HR Portal"
echo 5. Click "Commit changes"
echo.
echo ═══════════════════════════════════════════════════════════════
echo 🚀 STEP 3: DEPLOY ON RENDER
echo ═══════════════════════════════════════════════════════════════
echo.
echo In the Render tab:
echo 1. Sign up with your GitHub account
echo 2. Click "New +" then "Web Service"
echo 3. Connect your "hr-onboarding-dashboard" repository
echo 4. Name: hr-onboarding-dashboard
echo 5. Click "Create Web Service"
echo.
echo ═══════════════════════════════════════════════════════════════
echo ✅ STEP 4: YOUR WEBSITE WILL BE LIVE!
echo ═══════════════════════════════════════════════════════════════
echo.
echo Your website URL will be:
echo https://hr-onboarding-dashboard-[random].onrender.com
echo.
echo Login credentials:
echo Username: admin
echo Password: admin123
echo.
echo Features included:
echo ✅ 16 Active Employees across 5 departments
echo ✅ 3,400 HR Dataset Records with analytics
echo ✅ 104 Tasks, 45 Policies, 45 Training Programs
echo ✅ Modern TechCorp theme with blue gradient
echo ✅ Mobile-responsive dashboard
echo.
echo 🕐 Deployment time: 5-8 minutes total
echo.
pause

echo.
echo 🎯 Need help with any step? Here are the key files being uploaded:
echo.
dir /b
echo.
echo All files are ready for deployment! 🚀
echo.
pause