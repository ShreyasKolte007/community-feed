@echo off
REM Git Setup and Push Script for Windows

echo ==========================================
echo GIT SETUP ^& PUSH TO GITHUB
echo ==========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing Git repository...
    git init
    git branch -M main
)

REM Add all files
echo Adding files...
git add .

REM Commit
echo Committing...
git commit -m "Playto Community Feed - Complete Submission" -m "Features:" -m "- Community feed with posts and comments" -m "- Threaded comment system (nested)" -m "- Karma system (5 for posts, 1 for comments)" -m "- 24-hour leaderboard" -m "- N+1 query optimization" -m "- Race condition prevention" -m "- Comprehensive tests" -m "- Full documentation"

REM Ask for GitHub repo URL
echo.
echo Enter your GitHub repository URL:
echo Example: https://github.com/yourusername/playto-community-feed.git
set /p REPO_URL="URL: "

if "%REPO_URL%"=="" (
    echo No URL provided. Please run:
    echo git remote add origin YOUR_REPO_URL
    echo git push -u origin main
) else (
    REM Add remote
    git remote add origin "%REPO_URL%" 2>nul
    if errorlevel 1 git remote set-url origin "%REPO_URL%"
    
    REM Push
    echo.
    echo Pushing to GitHub...
    git push -u origin main
    
    echo.
    echo ==========================================
    echo SUCCESS! Code pushed to GitHub
    echo ==========================================
    echo.
    echo Repository: %REPO_URL%
    echo.
    echo Next steps:
    echo 1. Make repository public (if private)
    echo 2. Deploy using Railway
    echo 3. Submit to Playto
)

pause
