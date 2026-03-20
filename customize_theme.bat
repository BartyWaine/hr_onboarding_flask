@echo off
echo 🎨 TechCorp HR Portal - Theme Customization
echo.
echo Current company name: TechCorp HR Portal
echo.
set /p company_name="Enter your company name (or press Enter to keep TechCorp): "

if "%company_name%"=="" set company_name=TechCorp

echo.
echo Choose a color theme:
echo 1. Blue (Current) - Professional
echo 2. Green - Nature/Growth
echo 3. Purple - Creative
echo 4. Orange - Energetic
echo 5. Red - Bold
echo.
set /p theme_choice="Enter theme number (1-5): "

echo.
echo Applying customizations...

REM Update company name in templates
powershell -Command "(Get-Content 'templates\base.html') -replace 'TechCorp HR Portal', '%company_name% HR Portal' | Set-Content 'templates\base.html'"
powershell -Command "(Get-Content 'templates\dashboard.html') -replace 'TechCorp Dashboard', '%company_name% Dashboard' | Set-Content 'templates\dashboard.html'"

REM Apply color theme
if "%theme_choice%"=="2" (
    powershell -Command "(Get-Content 'templates\base.html') -replace '--primary-color: #2563eb;', '--primary-color: #059669;' | Set-Content 'templates\base.html'"
    powershell -Command "(Get-Content 'templates\base.html') -replace '--secondary-color: #1e40af;', '--secondary-color: #047857;' | Set-Content 'templates\base.html'"
    echo ✅ Applied Green theme
)
if "%theme_choice%"=="3" (
    powershell -Command "(Get-Content 'templates\base.html') -replace '--primary-color: #2563eb;', '--primary-color: #7c3aed;' | Set-Content 'templates\base.html'"
    powershell -Command "(Get-Content 'templates\base.html') -replace '--secondary-color: #1e40af;', '--secondary-color: #6d28d9;' | Set-Content 'templates\base.html'"
    echo ✅ Applied Purple theme
)
if "%theme_choice%"=="4" (
    powershell -Command "(Get-Content 'templates\base.html') -replace '--primary-color: #2563eb;', '--primary-color: #ea580c;' | Set-Content 'templates\base.html'"
    powershell -Command "(Get-Content 'templates\base.html') -replace '--secondary-color: #1e40af;', '--secondary-color: #dc2626;' | Set-Content 'templates\base.html'"
    echo ✅ Applied Orange theme
)
if "%theme_choice%"=="5" (
    powershell -Command "(Get-Content 'templates\base.html') -replace '--primary-color: #2563eb;', '--primary-color: #dc2626;' | Set-Content 'templates\base.html'"
    powershell -Command "(Get-Content 'templates\base.html') -replace '--secondary-color: #1e40af;', '--secondary-color: #b91c1c;' | Set-Content 'templates\base.html'"
    echo ✅ Applied Red theme
)

echo.
echo ✅ Customization complete!
echo.
echo 🏢 Company Name: %company_name% HR Portal
echo 🎨 Theme: Applied successfully
echo.
echo Your website is now customized and ready for deployment!
echo.
pause