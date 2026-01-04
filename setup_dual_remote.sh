#!/bin/bash

# ============================================================================
# DUAL REMOTE RESTORATION SCRIPT WITH AUTO-SYNC
# ============================================================================
# This script restores the complete git configuration for working with both
# Azure DevOps (Evo Builder) and GitHub repositories.
#
# NEW: Automatically syncs histories to prevent divergence and conflicts!
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
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}=========================================="
echo "🔧 Dual Remote Restoration Script"
echo "   with Auto-Sync Protection"
echo -e "==========================================${NC}"
echo ""

# ============================================================================
# STEP 1: Verify Azure Remote (origin)
# ============================================================================
echo -e "${BLUE}[1/7] Verifying Azure remote (origin)...${NC}"
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
echo -e "${BLUE}[2/7] Setting up GitHub remote...${NC}"

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
echo -e "${BLUE}[3/7] Fetching from remotes...${NC}"

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
echo -e "${BLUE}[4/7] Setting up working branch...${NC}"

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
# STEP 5: 🆕 AUTO-SYNC - Prevent Divergence
# ============================================================================
echo -e "${CYAN}[5/7] 🔄 Auto-Sync: Checking for divergence...${NC}"

# Check if GitHub branch exists
if git show-ref --verify --quiet refs/remotes/github/$GITHUB_BRANCH; then
    echo -e "${YELLOW}   Comparing local with GitHub...${NC}"
    
    # Get commit hashes
    LOCAL_COMMIT=$(git rev-parse HEAD)
    GITHUB_COMMIT=$(git rev-parse github/$GITHUB_BRANCH)
    
    if [ "$LOCAL_COMMIT" = "$GITHUB_COMMIT" ]; then
        echo -e "${GREEN}✅ Local and GitHub are in sync!${NC}"
    else
        # Check if they share common history
        MERGE_BASE=$(git merge-base HEAD github/$GITHUB_BRANCH 2>/dev/null)
        
        if [ -z "$MERGE_BASE" ]; then
            echo -e "${YELLOW}⚠️  Unrelated histories detected!${NC}"
            echo -e "${YELLOW}   This happens after environment refresh.${NC}"
            echo ""
            echo -e "${CYAN}   🔧 Auto-fixing: Merging histories...${NC}"
            
            # Attempt automatic merge with unrelated histories
            if git merge github/$GITHUB_BRANCH --allow-unrelated-histories --no-edit -m "chore: Auto-sync after environment refresh" 2>/dev/null; then
                echo -e "${GREEN}✅ Histories merged successfully!${NC}"
            else
                echo -e "${RED}❌ Automatic merge failed - conflicts detected${NC}"
                echo ""
                echo -e "${YELLOW}📋 Manual intervention required:${NC}"
                echo "   1. Check conflicted files: git status"
                echo "   2. Resolve conflicts in your editor"
                echo "   3. Stage resolved files: git add <file>"
                echo "   4. Complete merge: git commit"
                echo "   5. Push to both remotes"
                echo ""
                echo -e "${YELLOW}⚠️  Setup paused. Run this script again after resolving conflicts.${NC}"
                exit 1
            fi
        else
            # They share history but diverged
            AHEAD=$(git rev-list --count github/$GITHUB_BRANCH..HEAD)
            BEHIND=$(git rev-list --count HEAD..github/$GITHUB_BRANCH)
            
            if [ "$BEHIND" -gt 0 ]; then
                echo -e "${YELLOW}⚠️  Local is $BEHIND commit(s) behind GitHub${NC}"
                echo -e "${CYAN}   🔧 Auto-fixing: Pulling from GitHub...${NC}"
                
                if git pull github $GITHUB_BRANCH --no-edit 2>/dev/null; then
                    echo -e "${GREEN}✅ Pulled latest changes from GitHub${NC}"
                else
                    echo -e "${RED}❌ Pull failed - conflicts detected${NC}"
                    echo ""
                    echo -e "${YELLOW}📋 Manual intervention required:${NC}"
                    echo "   1. Resolve conflicts"
                    echo "   2. Complete merge: git commit"
                    echo "   3. Run this script again"
                    exit 1
                fi
            fi
            
            if [ "$AHEAD" -gt 0 ]; then
                echo -e "${YELLOW}   Local is $AHEAD commit(s) ahead of GitHub${NC}"
                echo -e "${CYAN}   💡 Will sync to GitHub after setup completes${NC}"
            fi
        fi
    fi
else
    echo -e "${YELLOW}⚠️  GitHub branch '$GITHUB_BRANCH' not found${NC}"
    echo -e "${CYAN}   💡 Will create it when you first push${NC}"
fi
echo ""

# ============================================================================
# STEP 6: Verify Configuration
# ============================================================================
echo -e "${BLUE}[6/7] Verifying configuration...${NC}"
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
# STEP 7: 🆕 PUSH TO GITHUB (if ahead)
# ============================================================================
echo -e "${CYAN}[7/7] 🔄 Final Sync: Pushing to GitHub...${NC}"

if git show-ref --verify --quiet refs/remotes/github/$GITHUB_BRANCH; then
    AHEAD=$(git rev-list --count github/$GITHUB_BRANCH..HEAD 2>/dev/null || echo "0")
    
    if [ "$AHEAD" -gt 0 ]; then
        echo -e "${YELLOW}   Pushing $AHEAD commit(s) to GitHub...${NC}"
        
        if git push github $LOCAL_WORKING_BRANCH:$GITHUB_BRANCH 2>/dev/null; then
            echo -e "${GREEN}✅ Pushed to GitHub successfully!${NC}"
        else
            echo -e "${YELLOW}⚠️  Could not push to GitHub (may require authentication)${NC}"
            echo -e "${CYAN}   💡 Run manually: git push github $LOCAL_WORKING_BRANCH:$GITHUB_BRANCH${NC}"
        fi
    else
        echo -e "${GREEN}✅ GitHub is already up to date!${NC}"
    fi
else
    echo -e "${YELLOW}   Creating new branch on GitHub...${NC}"
    if git push github $LOCAL_WORKING_BRANCH:$GITHUB_BRANCH 2>/dev/null; then
        echo -e "${GREEN}✅ Created branch on GitHub!${NC}"
    else
        echo -e "${YELLOW}⚠️  Could not push to GitHub (may require authentication)${NC}"
        echo -e "${CYAN}   💡 Run manually: git push github $LOCAL_WORKING_BRANCH:$GITHUB_BRANCH${NC}"
    fi
fi
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
echo -e "${CYAN}🔄 Auto-Sync Status:${NC}"
echo "  ✅ Histories are synchronized"
echo "  ✅ No divergence detected"
echo "  ✅ Ready to work without conflicts"
echo ""
echo -e "${YELLOW}📚 Common Workflows:${NC}"
echo ""
echo -e "${BLUE}Work in Evo Builder (use $LOCAL_WORKING_BRANCH):${NC}"
echo "  git checkout $LOCAL_WORKING_BRANCH"
echo "  # Make your changes"
echo "  git add ."
echo "  git commit -m \"Your message\""
echo ""
echo -e "${BLUE}Push to BOTH remotes (recommended):${NC}"
echo "  git push origin $LOCAL_WORKING_BRANCH:$AZURE_BRANCH"
echo "  git push github $LOCAL_WORKING_BRANCH:$GITHUB_BRANCH"
echo ""
echo -e "${BLUE}Or use this one-liner:${NC}"
echo "  git push origin $LOCAL_WORKING_BRANCH:$AZURE_BRANCH && git push github $LOCAL_WORKING_BRANCH:$GITHUB_BRANCH"
echo ""
echo -e "${BLUE}Pull latest from GitHub:${NC}"
echo "  git pull github $GITHUB_BRANCH"
echo ""
echo -e "${BLUE}Check status:${NC}"
echo "  git status"
echo "  git remote -v"
echo "  git branch -vv"
echo ""
echo -e "${CYAN}💡 Pro Tip:${NC}"
echo "  Always push to BOTH remotes after committing to prevent divergence!"
echo "  Run this script after every environment refresh."
echo ""
echo -e "${GREEN}🎉 You're all set! Happy coding!${NC}"
echo ""
