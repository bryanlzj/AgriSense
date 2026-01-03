#!/bin/bash

# Setup script for dual remote (Azure + GitHub)
# This keeps Azure as 'origin' for Evo Builder and adds GitHub as 'github'

# ============================================================================
# CONFIGURATION - Update these values for your repository
# ============================================================================
GITHUB_URL="https://github.com/bryanlzj/AgriSense.git"
GITHUB_BRANCH="main"
# ============================================================================

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}=========================================="
echo "Dual Remote Setup (Azure + GitHub)"
echo -e "==========================================${NC}"
echo ""

echo -e "${YELLOW}Current Git Remote Configuration:${NC}"
git remote -v
echo ""

# Store the current Azure remote URL
AZURE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$AZURE_URL" ]; then
    echo -e "${YELLOW}⚠️  Warning: No 'origin' remote found${NC}"
else
    echo -e "${GREEN}✅ Azure remote (origin) preserved:${NC}"
    echo "   $AZURE_URL"
    echo ""
fi

# Check if github remote already exists
if git remote | grep -q "^github$"; then
    echo -e "${BLUE}🔄 GitHub remote already exists. Updating URL...${NC}"
    git remote set-url github "$GITHUB_URL"
    echo -e "${GREEN}✅ Updated GitHub remote URL${NC}"
else
    echo -e "${BLUE}➕ Adding new GitHub remote...${NC}"
    git remote add github "$GITHUB_URL"
    echo -e "${GREEN}✅ Added GitHub remote${NC}"
fi

echo ""
echo -e "${YELLOW}Updated Git Remote Configuration:${NC}"
git remote -v
echo ""

# Fetch from GitHub to get branch info
echo -e "${BLUE}📥 Fetching from GitHub...${NC}"
if git fetch github 2>/dev/null; then
    echo -e "${GREEN}✅ Successfully fetched from GitHub${NC}"
    echo ""
    echo -e "${YELLOW}Available GitHub branches:${NC}"
    git branch -r | grep "github/" | sed 's/^/  /'
else
    echo -e "${YELLOW}⚠️  Could not fetch from GitHub (authentication may be required)${NC}"
fi

echo ""
echo -e "${GREEN}=========================================="
echo "✅ Setup Complete!"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}Configuration Summary:${NC}"
echo "  • Azure Remote:  origin → $AZURE_URL"
echo "  • GitHub Remote: github → $GITHUB_URL"
echo "  • GitHub Branch: $GITHUB_BRANCH"
echo ""
echo -e "${YELLOW}Common Commands:${NC}"
echo ""
echo -e "${BLUE}Push to Azure (Evo Builder):${NC}"
echo "  git push origin agrisense"
echo ""
echo -e "${BLUE}Push to GitHub:${NC}"
echo "  git push github $GITHUB_BRANCH"
echo ""
echo -e "${BLUE}Pull from GitHub:${NC}"
echo "  git pull github $GITHUB_BRANCH"
echo ""
echo -e "${BLUE}View all remotes:${NC}"
echo "  git remote -v"
echo ""
echo -e "${BLUE}See current branch:${NC}"
echo "  git branch --show-current"
echo ""
