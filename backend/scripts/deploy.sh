#!/bin/bash

# ===================================
# AgriSense Backend - Deployment Script
# ===================================
# This script automates the deployment process
# Usage: ./scripts/deploy.sh [environment]
# Example: ./scripts/deploy.sh production

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ===================================
# Configuration
# ===================================
ENVIRONMENT=${1:-production}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   AgriSense Backend Deployment        ║${NC}"
echo -e "${GREEN}║   Environment: $ENVIRONMENT           ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# ===================================
# Step 1: Check Prerequisites
# ===================================
echo -e "${YELLOW}[1/7] Checking prerequisites...${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

# Check if .env file exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${RED}Error: .env file not found${NC}"
    echo "Copy .env.production.example to .env and configure it:"
    echo "  cp .env.production.example .env"
    echo "  nano .env"
    exit 1
fi

echo -e "${GREEN}✓ All prerequisites met${NC}"
echo ""

# ===================================
# Step 2: Pull Latest Code (if Git repo)
# ===================================
echo -e "${YELLOW}[2/7] Checking for updates...${NC}"

if [ -d "$PROJECT_ROOT/.git" ]; then
    cd "$PROJECT_ROOT"
    echo "Pulling latest changes from Git..."
    git pull origin main || echo "Warning: Could not pull from Git (continuing anyway)"
else
    echo "Not a Git repository, skipping..."
fi

echo -e "${GREEN}✓ Code up to date${NC}"
echo ""

# ===================================
# Step 3: Stop Running Containers
# ===================================
echo -e "${YELLOW}[3/7] Stopping running containers...${NC}"

cd "$PROJECT_ROOT"
docker-compose down || echo "No containers to stop"

echo -e "${GREEN}✓ Containers stopped${NC}"
echo ""

# ===================================
# Step 4: Build Docker Images
# ===================================
echo -e "${YELLOW}[4/7] Building Docker images...${NC}"

cd "$PROJECT_ROOT"
docker-compose build --no-cache

echo -e "${GREEN}✓ Images built successfully${NC}"
echo ""

# ===================================
# Step 5: Start Services
# ===================================
echo -e "${YELLOW}[5/7] Starting services...${NC}"

cd "$PROJECT_ROOT"
docker-compose up -d

echo -e "${GREEN}✓ Services started${NC}"
echo ""

# ===================================
# Step 6: Wait for Database
# ===================================
echo -e "${YELLOW}[6/7] Waiting for database to be ready...${NC}"

# Wait for PostgreSQL to be ready
for i in {1..30}; do
    if docker-compose exec -T postgres pg_isready -U agrisense_user &> /dev/null; then
        echo -e "${GREEN}✓ Database is ready${NC}"
        break
    fi
    echo "Waiting for database... ($i/30)"
    sleep 2
done

echo ""

# ===================================
# Step 7: Run Database Migrations
# ===================================
echo -e "${YELLOW}[7/7] Running database migrations...${NC}"

# Run Alembic migrations inside the backend container
docker-compose exec -T backend alembic upgrade head

echo -e "${GREEN}✓ Migrations completed${NC}"
echo ""

# ===================================
# Deployment Complete
# ===================================
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Deployment Successful! 🎉            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""
echo "Backend API: http://localhost:5000"
echo "API Docs: http://localhost:5000/docs"
echo "Health Check: http://localhost:5000/health"
echo ""
echo "View logs: docker-compose logs -f backend"
echo "Stop services: docker-compose down"
echo ""
