#!/bin/bash

# ============================================================================
# DUAL REMOTE RESTORATION SCRIPT
# ============================================================================
# This script restores the complete git configuration for working with both
# Azure DevOps (Evo Builder) and GitHub repositories.
#
# Run this script if Evo Builder environment resets or git config is lost.
# ============================================================================

# ============================================================================
# CONFIGURATION - Your repository details
# ============================================================================
GITHUB_URL="https://github.com/bryanlzj/AgriSense.git"
GITHUB_BRANCH="bryan"
AZURE_BRANCH="fast-star-62628"
LOCAL_WORKING_BRANCH="agrisense"
# ============================================================================

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}=========================================="
echo "🔧 Dual Remote Restoration Script"
echo -e "==========================================${NC}"
echo ""

# ============================================================================
# STEP 1: Verify Azure Remote (origin)
# ============================================================================
echo -e "${BLUE}[1/5] Verifying Azure remote (origin)...${NC}"
AZURE_URL=$(git remote get-url origin 2>/dev/null)

if [ -z "$AZURE_URL" ]; then
    echo -e "${RED}❌ Error: No 'origin' remote found${NC}"
    echo "   This script expects Azure DevOps to be set as 'origin'"
    exit 1
else
    echo -e "${GREEN}✅ Azure remote (origin) found:${NC}"
    echo "   $AZURE_URL"
fi
echo ""

# ============================================================================
# STEP 2: Setup GitHub Remote
# ============================================================================
echo -e "${BLUE}[2/5] Setting up GitHub remote...${NC}"

if git remote | grep -q "^github$"; then
    echo -e "${YELLOW}   GitHub remote exists. Updating URL...${NC}"
    git remote set-url github "$GITHUB_URL"
    echo -e "${GREEN}✅ Updated GitHub remote URL${NC}"
else
    echo -e "${YELLOW}   Adding new GitHub remote...${NC}"
    git remote add github "$GITHUB_URL"
    echo -e "${GREEN}✅ Added GitHub remote${NC}"
fi
echo ""

# ============================================================================
# STEP 3: Fetch from Both Remotes
# ============================================================================
echo -e "${BLUE}[3/5] Fetching from remotes...${NC}"

echo -e "${YELLOW}   Fetching from Azure...${NC}"
if git fetch origin 2>/dev/null; then
    echo -e "${GREEN}✅ Fetched from Azure${NC}"
else
    echo -e "${RED}⚠️  Could not fetch from Azure${NC}"
fi

echo -e "${YELLOW}   Fetching from GitHub...${NC}"
if git fetch github 2>/dev/null; then
    echo -e "${GREEN}✅ Fetched from GitHub${NC}"
else
    echo -e "${YELLOW}⚠️  Could not fetch from GitHub (may require authentication)${NC}"
fi
echo ""

# ============================================================================
# STEP 4: Setup Working Branch
# ============================================================================
echo -e "${BLUE}[4/5] Setting up working branch...${NC}"

CURRENT_BRANCH=$(git branch --show-current)

if [ "$CURRENT_BRANCH" != "$LOCAL_WORKING_BRANCH" ]; then
    echo -e "${YELLOW}   Current branch: $CURRENT_BRANCH${NC}"
    echo -e "${YELLOW}   Switching to: $LOCAL_WORKING_BRANCH${NC}"
    
    # Check if branch exists locally
    if git show-ref --verify --quiet refs/heads/$LOCAL_WORKING_BRANCH; then
        git checkout $LOCAL_WORKING_BRANCH
    else
        # Create branch from remote if it exists
        if git show-ref --verify --quiet refs/remotes/origin/$AZURE_BRANCH; then
            git checkout -b $LOCAL_WORKING_BRANCH origin/$AZURE_BRANCH
        else
            echo -e "${RED}❌ Error: Cannot find branch $AZURE_BRANCH on origin${NC}"
            exit 1
        fi
    fi
    echo -e "${GREEN}✅ Switched to $LOCAL_WORKING_BRANCH${NC}"
else
    echo -e "${GREEN}✅ Already on $LOCAL_WORKING_BRANCH${NC}"
fi

# Set upstream tracking to Azure
echo -e "${YELLOW}   Setting upstream tracking...${NC}"
git branch --set-upstream-to=origin/$AZURE_BRANCH $LOCAL_WORKING_BRANCH 2>/dev/null
echo -e "${GREEN}✅ Upstream set to origin/$AZURE_BRANCH${NC}"
echo ""

# ============================================================================
# STEP 5: Verify Configuration
# ============================================================================
echo -e "${BLUE}[5/5] Verifying configuration...${NC}"
echo ""

echo -e "${YELLOW}Git Remotes:${NC}"
git remote -v | sed 's/^/  /'
echo ""

echo -e "${YELLOW}Current Branch:${NC}"
echo "  $(git branch --show-current)"
echo ""

echo -e "${YELLOW}Branch Tracking:${NC}"
git branch -vv | grep "^\*" | sed 's/^/  /'
echo ""

echo -e "${YELLOW}Available Remote Branches:${NC}"
echo -e "${BLUE}  Azure (origin):${NC}"
git branch -r | grep "origin/" | sed 's/^/    /'
echo -e "${BLUE}  GitHub (github):${NC}"
git branch -r | grep "github/" | sed 's/^/    /'
echo ""

# ============================================================================
# COMPLETION
# ============================================================================
echo -e "${GREEN}=========================================="
echo "✅ Setup Complete!"
echo -e "==========================================${NC}"
echo ""
echo -e "${YELLOW}📋 Configuration Summary:${NC}"
echo ""
echo "  🔹 Working Branch:  $LOCAL_WORKING_BRANCH"
echo "  🔹 Tracks Azure:    origin/$AZURE_BRANCH"
echo "  🔹 Azure Remote:    $AZURE_URL"
echo "  🔹 GitHub Remote:   $GITHUB_URL"
echo "  🔹 GitHub Branch:   $GITHUB_BRANCH"
echo ""
echo -e "${YELLOW}📚 Common Workflows:${NC}"
echo ""
echo -e "${BLUE}Work in Evo Builder (use $LOCAL_WORKING_BRANCH):${NC}"
echo "  git checkout $LOCAL_WORKING_BRANCH"
echo "  # Make your changes"
echo "  git add ."
echo "  git commit -m \"Your message\""
echo "  git push origin $LOCAL_WORKING_BRANCH:$AZURE_BRANCH"
echo ""
echo -e "${BLUE}Sync to GitHub:${NC}"
echo "  git push github $GITHUB_BRANCH"
echo ""
echo -e "${BLUE}Pull from GitHub:${NC}"
echo "  git pull github $GITHUB_BRANCH"
echo ""
echo -e "${BLUE}Check status:${NC}"
echo "  git status"
echo "  git remote -v"
echo "  git branch -vv"
echo ""
echo -e "${GREEN}🎉 You're all set! Happy coding!${NC}"
echo ""
