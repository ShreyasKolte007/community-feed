#!/bin/bash
# Git Setup and Push Script

echo "=========================================="
echo "GIT SETUP & PUSH TO GITHUB"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git branch -M main
fi

# Add all files
echo "Adding files..."
git add .

# Commit
echo "Committing..."
git commit -m "Playto Community Feed - Complete Submission

Features:
- Community feed with posts and comments
- Threaded comment system (nested)
- Karma system (5 for posts, 1 for comments)
- 24-hour leaderboard
- N+1 query optimization
- Race condition prevention
- Comprehensive tests
- Full documentation"

# Ask for GitHub repo URL
echo ""
echo "Enter your GitHub repository URL:"
echo "Example: https://github.com/yourusername/playto-community-feed.git"
read -p "URL: " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "No URL provided. Please run:"
    echo "git remote add origin YOUR_REPO_URL"
    echo "git push -u origin main"
else
    # Add remote
    git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
    
    # Push
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
    
    echo ""
    echo "=========================================="
    echo "SUCCESS! Code pushed to GitHub"
    echo "=========================================="
    echo ""
    echo "Repository: $REPO_URL"
    echo ""
    echo "Next steps:"
    echo "1. Make repository public (if private)"
    echo "2. Deploy using deploy_railway.sh"
    echo "3. Submit to Playto"
fi
