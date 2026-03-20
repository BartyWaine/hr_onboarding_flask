@echo off
echo 🚀 HR Onboarding Dashboard - Heroku Deployment
echo ================================================

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI not found. Please install it first:
    echo    https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

REM Check if git is initialized
if not exist ".git" (
    echo 📁 Initializing Git repository...
    git init
    git add .
    git commit -m "Initial commit - HR Onboarding Dashboard"
)

REM Login to Heroku
echo 🔐 Logging into Heroku...
heroku login

REM Create Heroku app
echo 📱 Creating Heroku app...
set /p APP_NAME="Enter your app name (e.g., my-hr-dashboard): "

if "%APP_NAME%"=="" (
    echo ❌ App name cannot be empty
    pause
    exit /b 1
)

heroku create %APP_NAME%

REM Set environment variables
echo ⚙️  Setting environment variables...
heroku config:set FLASK_ENV=production --app %APP_NAME%
heroku config:set SECRET_KEY=your-secret-key-change-this --app %APP_NAME%
heroku config:set DEBUG=False --app %APP_NAME%

REM Deploy to Heroku
echo 🚀 Deploying to Heroku...
git add .
git commit -m "Deploy HR Dashboard to Heroku"
git push heroku main

REM Open the app
echo ✅ Deployment complete!
echo 🌐 Opening your HR Dashboard...
heroku open --app %APP_NAME%

echo.
echo 🎉 Your HR Onboarding Dashboard is now live!
echo 📊 Features available:
echo    - Complete HR Dashboard
echo    - Employee Management (16 active employees)
echo    - Task Tracking (104 tasks)
echo    - Policy Management (45 policies)
echo    - Training Programs (45 training assignments)
echo    - HR Dataset Analytics (3,400 records)
echo    - KPI Monitoring
echo.
echo 🔐 Default login: admin / admin123
echo ⚠️  Remember to change the admin password in production!
echo.
echo 📱 Your app URL: https://%APP_NAME%.herokuapp.com
pause