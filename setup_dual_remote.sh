#!/bin/bash

# Setup script for dual remote (Azure + GitHub)
# This keeps Azure as 'origin' for Evo Builder and adds GitHub as 'github'

echo "=== Current Git Remote Configuration ==="
git remote -v
echo ""

# Check if github remote already exists
if git remote | grep -q "^github$"; then
    echo "GitHub remote already exists. Updating URL..."
    read -p "Enter your GitHub repo URL (e.g., https://github.com/username/repo.git): " GITHUB_URL
    git remote set-url github "$GITHUB_URL"
else
    echo "Adding new GitHub remote..."
    read -p "Enter your GitHub repo URL (e.g., https://github.com/username/repo.git): " GITHUB_URL
    git remote add github "$GITHUB_URL"
fi

echo ""
echo "=== Updated Git Remote Configuration ==="
git remote -v
echo ""

echo "=== Setup Complete! ==="
echo ""
echo "Usage:"
echo "  - Push to Azure (Evo Builder):  git push origin <branch>"
echo "  - Push to GitHub:               git push github <branch>"
echo "  - Pull from Azure:              git pull origin <branch>"
echo "  - Pull from GitHub:             git pull github <branch>"
echo ""
echo "To push current branch to GitHub:"
echo "  git push github $(git branch --show-current)"
echo ""
echo "To set GitHub as default push for current branch:"
echo "  git branch --set-upstream-to=github/$(git branch --show-current)"
