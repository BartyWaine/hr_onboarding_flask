@echo off
echo 🚀 HR Onboarding Dashboard - Heroku Deployment
echo.

echo Step 1: Checking Heroku CLI...
heroku --version
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI not found! Please install it first.
    echo Download from: https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

echo.
echo Step 2: Logging into Heroku...
heroku login
if %errorlevel% neq 0 (
    echo ❌ Heroku login failed!
    pause
    exit /b 1
)

echo.
echo Step 3: Creating Heroku app...
heroku create hr-onboarding-dashboard-%random%
if %errorlevel% neq 0 (
    echo ❌ Failed to create Heroku app!
    pause
    exit /b 1
)

echo.
echo Step 4: Setting environment variables...
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=hr-dashboard-secret-key-%random%

echo.
echo Step 5: Deploying to Heroku...
git push heroku master
if %errorlevel% neq 0 (
    echo ❌ Deployment failed!
    pause
    exit /b 1
)

echo.
echo ✅ Deployment successful!
echo.
echo 🌐 Your HR Onboarding Dashboard is now live!
echo 📱 Login with: admin / admin123
echo.
echo 📊 Features available:
echo   ✅ 16 Active Employees
echo   ✅ 3,400 HR Dataset Records  
echo   ✅ 104 Tasks, 45 Policies, 45 Training Programs
echo   ✅ Complete Analytics Dashboard
echo.
heroku open
pause