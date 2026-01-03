#!/bin/bash

# GitHub Repository Configuration Script
# This script is specifically designed for AI assistant to run
# It automatically handles line endings and overwrites untracked files

# Fix line endings for this script (convert CRLF to LF if needed)
if command -v dos2unix &> /dev/null; then
    dos2unix "$0" 2>/dev/null || true
fi

set -e  # Exit on error

# ============================================================================
# 🔧 CONFIGURATION SECTION - Just paste your GitHub repository URL!
# ============================================================================

# Paste your GitHub repository URL here (from browser or clone button)
# Examples:
#   https://github.com/username/repository
#   https://github.com/username/repository.git
#   git@github.com:username/repository.git (SSH format)
REPO_URL="https://github.com/bryanlzj/AgriSense"   # e.g., "https://github.com/yourusername/agrisense"

# The branch to checkout after setup
DEFAULT_BRANCH="main"    # e.g., "main" or "master"

# Optional: Git User Configuration (leave empty to skip)
GIT_USER_NAME=""                          # e.g., "John Doe" or leave empty
GIT_USER_EMAIL=""                         # e.g., "john@example.com" or leave empty

# Optional: Credential Cache Duration (in seconds)
CREDENTIAL_CACHE_TIMEOUT=3600             # Default: 1 hour (3600 seconds)

# ============================================================================
# END CONFIGURATION - Do not modify below this line unless you know what you're doing
# ============================================================================

# Colors for better output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo ""
echo -e "${BLUE}=========================================="
echo "GitHub Repository Configuration Setup"
echo -e "==========================================${NC}"
echo ""

# Parse the repository URL to extract components
echo -e "${BLUE}🔍 Parsing repository URL...${NC}"

# Remove any existing credentials from URL
CLEAN_URL=$(echo "$REPO_URL" | sed -E 's|https://[^@]*@|https://|')

# Remove .git suffix if present
CLEAN_URL=$(echo "$CLEAN_URL" | sed 's/\.git$//')

# Detect if SSH or HTTPS
if [[ $CLEAN_URL =~ ^git@github\.com:(.+)/(.+)$ ]]; then
    # SSH format: git@github.com:username/repo
    REPO_OWNER="${BASH_REMATCH[1]}"
    REPO_NAME="${BASH_REMATCH[2]}"
    USE_SSH=true
    
    echo -e "${GREEN}✅ Successfully parsed SSH URL${NC}"
    echo ""
    echo -e "${YELLOW}Repository Details:${NC}"
    echo "  Owner: ${REPO_OWNER}"
    echo "  Repository: ${REPO_NAME}"
    echo "  Protocol: SSH"
    echo ""
    
elif [[ $CLEAN_URL =~ https://github\.com/([^/]+)/([^/]+) ]]; then
    # HTTPS format: https://github.com/username/repo
    REPO_OWNER="${BASH_REMATCH[1]}"
    REPO_NAME="${BASH_REMATCH[2]}"
    USE_SSH=false
    
    echo -e "${GREEN}✅ Successfully parsed HTTPS URL${NC}"
    echo ""
    echo -e "${YELLOW}Repository Details:${NC}"
    echo "  Owner: ${REPO_OWNER}"
    echo "  Repository: ${REPO_NAME}"
    echo "  Protocol: HTTPS"
    echo ""
    
else
    echo -e "${RED}❌ Error: Invalid GitHub URL format${NC}"
    echo ""
    echo "Expected formats:"
    echo "  HTTPS: https://github.com/USERNAME/REPOSITORY"
    echo "  SSH:   git@github.com:USERNAME/REPOSITORY.git"
    echo ""
    echo "Your URL:"
    echo "  ${REPO_URL}"
    echo ""
    exit 1
fi

# Check if git is initialized, if not initialize it
if [ ! -d .git ]; then
    echo -e "${YELLOW}📦 Git repository not initialized. Initializing now...${NC}"
    git init
    echo -e "${GREEN}✅ Git repository initialized${NC}"
    echo ""
else
    echo -e "${GREEN}✅ Git repository already initialized${NC}"
    echo ""
fi

# Handle authentication based on protocol
if [ "$USE_SSH" = true ]; then
    # SSH authentication
    echo -e "${BLUE}🔐 Using SSH authentication${NC}"
    echo ""
    echo -e "${YELLOW}Make sure you have:${NC}"
    echo "  1. SSH key generated (ssh-keygen)"
    echo "  2. SSH key added to GitHub (Settings → SSH and GPG keys)"
    echo "  3. SSH agent running with your key loaded"
    echo ""
    
    # Test SSH connection
    echo -e "${BLUE}🔍 Testing SSH connection to GitHub...${NC}"
    if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
        echo -e "${GREEN}✅ SSH authentication successful!${NC}"
    else
        echo -e "${YELLOW}⚠️  SSH test inconclusive, but continuing...${NC}"
        echo -e "${YELLOW}   If connection fails, check your SSH keys${NC}"
    fi
    echo ""
    
    REPO_URL_WITH_AUTH="git@github.com:${REPO_OWNER}/${REPO_NAME}.git"
    
else
    # HTTPS authentication - need Personal Access Token (PAT)
    echo -e "${YELLOW}📝 Personal Access Token (PAT) Required${NC}"
    echo ""
    echo "To create a GitHub PAT:"
    echo "  1. Go to: https://github.com/settings/tokens"
    echo "  2. Click 'Generate new token (classic)'"
    echo "  3. Set scopes: 'repo' (Full control of private repositories)"
    echo "  4. Click 'Generate token'"
    echo "  5. Copy the token (starts with 'ghp_')"
    echo ""
    echo -e "${GREEN}Please enter your GitHub PAT:${NC}"
    echo -e "${YELLOW}(Your input will be hidden for security)${NC}"
    echo -e "${YELLOW}(Press Enter to skip if repository is public and you only need read access)${NC}"
    read -s PAT
    echo ""
    
    # Build URL with or without PAT
    if [ -z "$PAT" ]; then
        echo -e "${YELLOW}⚠️  No PAT provided. Using public access (read-only).${NC}"
        REPO_URL_WITH_AUTH="https://github.com/${REPO_OWNER}/${REPO_NAME}.git"
    else
        # Validate PAT format (GitHub PATs start with ghp_, gho_, ghu_, ghs_, or ghr_)
        if [[ ! $PAT =~ ^gh[pousr]_ ]]; then
            echo -e "${YELLOW}⚠️  Warning: PAT doesn't match expected GitHub format (should start with 'ghp_', 'gho_', etc.)${NC}"
            echo -n "Continue anyway? (y/N): "
            read -r CONTINUE
            if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
                echo "Setup cancelled."
                exit 1
            fi
        fi
        
        REPO_URL_WITH_AUTH="https://${PAT}@github.com/${REPO_OWNER}/${REPO_NAME}.git"
    fi
fi

echo ""
echo -e "${BLUE}🔧 Configuring git remote URL...${NC}"

# Check if origin remote exists
if git remote get-url origin &> /dev/null; then
    # Update existing remote
    git remote set-url origin "$REPO_URL_WITH_AUTH"
    echo -e "${GREEN}✅ Updated existing 'origin' remote${NC}"
else
    # Add new remote
    git remote add origin "$REPO_URL_WITH_AUTH"
    echo -e "${GREEN}✅ Added new 'origin' remote${NC}"
fi

# Configure git user if specified
if [ -n "$GIT_USER_NAME" ] || [ -n "$GIT_USER_EMAIL" ]; then
    echo ""
    echo -e "${BLUE}🔧 Configuring git user...${NC}"
    if [ -n "$GIT_USER_NAME" ]; then
        git config --global user.name "$GIT_USER_NAME"
        echo -e "${GREEN}✅ Set git user.name: ${GIT_USER_NAME}${NC}"
    fi
    if [ -n "$GIT_USER_EMAIL" ]; then
        git config --global user.email "$GIT_USER_EMAIL"
        echo -e "${GREEN}✅ Set git user.email: ${GIT_USER_EMAIL}${NC}"
    fi
fi

# Configure git to cache credentials (only for HTTPS)
if [ "$USE_SSH" = false ] && [ -n "$PAT" ]; then
    echo ""
    echo -e "${BLUE}🔧 Configuring git credential helper...${NC}"
    git config --global credential.helper "cache --timeout=${CREDENTIAL_CACHE_TIMEOUT}"
    CACHE_HOURS=$((CREDENTIAL_CACHE_TIMEOUT / 3600))
    CACHE_MINUTES=$(((CREDENTIAL_CACHE_TIMEOUT % 3600) / 60))
    if [ $CACHE_HOURS -gt 0 ]; then
        echo -e "${GREEN}✅ Credentials will be cached for ${CACHE_HOURS} hour(s)${NC}"
    else
        echo -e "${GREEN}✅ Credentials will be cached for ${CACHE_MINUTES} minute(s)${NC}"
    fi
fi

# Test the connection
echo ""
echo -e "${BLUE}🔍 Testing connection to GitHub...${NC}"
echo ""

if git ls-remote origin &> /dev/null; then
    echo -e "${GREEN}✅ SUCCESS! Connection to GitHub is working!${NC}"
    echo ""
    
    # Fetch branches
    echo -e "${BLUE}📥 Fetching branches...${NC}"
    git fetch origin
    
    echo ""
    echo -e "${YELLOW}Available remote branches:${NC}"
    git branch -r | sed 's/^/  /'
    
    echo ""
    echo -e "${YELLOW}Current local branch:${NC}"
    CURRENT_BRANCH=$(git branch --show-current)
    if [ -z "$CURRENT_BRANCH" ]; then
        echo -e "  ${RED}(No branch checked out)${NC}"
    else
        echo "  ${CURRENT_BRANCH}"
    fi
    
    # Auto-checkout default branch if not already on it
    echo ""
    if [ "$CURRENT_BRANCH" != "$DEFAULT_BRANCH" ]; then
        echo -e "${BLUE}🔄 Switching to default branch: ${DEFAULT_BRANCH}${NC}"
        
        # Remove any untracked files that might conflict (they're not important)
        echo -e "${YELLOW}🗑️  Cleaning untracked files...${NC}"
        git clean -fd
        
        # Check if branch exists locally
        if git show-ref --verify --quiet refs/heads/$DEFAULT_BRANCH; then
            # Branch exists locally, just checkout (force to overwrite any local changes)
            git checkout -f $DEFAULT_BRANCH
            echo -e "${GREEN}✅ Switched to existing local branch: ${DEFAULT_BRANCH}${NC}"
        else
            # Branch doesn't exist locally, create and track remote
            if git show-ref --verify --quiet refs/remotes/origin/$DEFAULT_BRANCH; then
                git checkout -b $DEFAULT_BRANCH origin/$DEFAULT_BRANCH
                echo -e "${GREEN}✅ Created and switched to branch: ${DEFAULT_BRANCH} (tracking origin/${DEFAULT_BRANCH})${NC}"
            else
                echo -e "${YELLOW}⚠️  Warning: Branch ${DEFAULT_BRANCH} not found on remote${NC}"
                echo -e "${YELLOW}   Staying on current branch: ${CURRENT_BRANCH}${NC}"
            fi
        fi
        
        # Pull latest changes
        echo ""
        echo -e "${BLUE}📥 Pulling latest changes...${NC}"
        if git pull origin $DEFAULT_BRANCH; then
            echo -e "${GREEN}✅ Successfully pulled latest changes${NC}"
        else
            echo -e "${YELLOW}⚠️  Could not pull changes (this is normal for new branches)${NC}"
        fi
    else
        echo -e "${GREEN}✅ Already on default branch: ${DEFAULT_BRANCH}${NC}"
        
        # Pull latest changes
        echo ""
        echo -e "${BLUE}📥 Pulling latest changes...${NC}"
        if git pull origin $DEFAULT_BRANCH; then
            echo -e "${GREEN}✅ Successfully pulled latest changes${NC}"
        else
            echo -e "${YELLOW}⚠️  Could not pull changes${NC}"
        fi
    fi
    
    echo ""
    echo -e "${GREEN}=========================================="
    echo "✅ Setup Complete!"
    echo -e "==========================================${NC}"
    echo ""
    echo -e "${YELLOW}Configuration Summary:${NC}"
    echo "  • Repository: ${REPO_NAME}"
    echo "  • Owner: ${REPO_OWNER}"
    echo "  • Branch: ${DEFAULT_BRANCH}"
    echo "  • Remote: origin"
    if [ "$USE_SSH" = true ]; then
        echo "  • Protocol: SSH"
    else
        echo "  • Protocol: HTTPS"
    fi
    echo ""
    echo -e "${YELLOW}Quick Commands:${NC}"
    echo "  • Pull latest: ${BLUE}git pull${NC}"
    echo "  • Push changes: ${BLUE}git push${NC}"
    echo "  • Check status: ${BLUE}git status${NC}"
    echo "  • View remote: ${BLUE}git remote -v${NC}"
    echo ""
    echo -e "${YELLOW}GitHub Repository URL:${NC}"
    echo "  https://github.com/${REPO_OWNER}/${REPO_NAME}"
    echo ""
    
else
    echo ""
    echo -e "${RED}❌ Error: Failed to connect to GitHub${NC}"
    echo ""
    echo "Possible issues:"
    if [ "$USE_SSH" = true ]; then
        echo "  • SSH key not added to GitHub"
        echo "  • SSH key not loaded in ssh-agent"
        echo "  • Repository doesn't exist or you don't have access"
    else
        echo "  • PAT is invalid or expired"
        echo "  • PAT doesn't have 'repo' permissions"
        echo "  • Repository doesn't exist or is private (need PAT for private repos)"
    fi
    echo "  • Repository URL is incorrect"
    echo "  • Network connectivity issues"
    echo ""
    echo "Please check your credentials and try again."
    echo ""
    exit 1
fi
