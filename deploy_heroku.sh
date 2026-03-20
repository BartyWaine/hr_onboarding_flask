#!/bin/bash
# HR Onboarding Dashboard - Heroku Deployment Script

echo "🚀 HR Onboarding Dashboard - Heroku Deployment"
echo "================================================"

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit - HR Onboarding Dashboard"
fi

# Login to Heroku
echo "🔐 Logging into Heroku..."
heroku login

# Create Heroku app
echo "📱 Creating Heroku app..."
read -p "Enter your app name (e.g., my-hr-dashboard): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name cannot be empty"
    exit 1
fi

heroku create $APP_NAME

# Set environment variables
echo "⚙️  Setting environment variables..."
heroku config:set FLASK_ENV=production --app $APP_NAME
heroku config:set SECRET_KEY=$(openssl rand -base64 32) --app $APP_NAME
heroku config:set DEBUG=False --app $APP_NAME

# Deploy to Heroku
echo "🚀 Deploying to Heroku..."
git add .
git commit -m "Deploy HR Dashboard to Heroku"
git push heroku main

# Open the app
echo "✅ Deployment complete!"
echo "🌐 Opening your HR Dashboard..."
heroku open --app $APP_NAME

echo ""
echo "🎉 Your HR Onboarding Dashboard is now live!"
echo "📊 Features available:"
echo "   - Complete HR Dashboard"
echo "   - Employee Management (16 active employees)"
echo "   - Task Tracking (104 tasks)"
echo "   - Policy Management (45 policies)"
echo "   - Training Programs (45 training assignments)"
echo "   - HR Dataset Analytics (3,400 records)"
echo "   - KPI Monitoring"
echo ""
echo "🔐 Default login: admin / admin123"
echo "⚠️  Remember to change the admin password in production!"
echo ""
echo "📱 Your app URL: https://$APP_NAME.herokuapp.com"