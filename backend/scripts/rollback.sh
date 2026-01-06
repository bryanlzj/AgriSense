#!/bin/bash

# ===================================
# AgriSense Backend - Rollback Script
# ===================================
# This script rolls back the last database migration
# Usage: ./scripts/rollback.sh [steps]
# Example: ./scripts/rollback.sh 1  (rollback 1 migration)

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ===================================
# Configuration
# ===================================
STEPS=${1:-1}
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo -e "${YELLOW}╔════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║   AgriSense Database Rollback          ║${NC}"
echo -e "${YELLOW}║   Rolling back $STEPS migration(s)     ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════╝${NC}"
echo ""

# ===================================
# Confirmation
# ===================================
echo -e "${RED}WARNING: This will rollback database migrations!${NC}"
echo -e "${RED}This may result in data loss.${NC}"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Rollback cancelled."
    exit 0
fi

# ===================================
# Show Current Migration
# ===================================
echo -e "${YELLOW}Current database version:${NC}"
cd "$PROJECT_ROOT"
docker-compose exec -T backend alembic current
echo ""

# ===================================
# Rollback Migration
# ===================================
echo -e "${YELLOW}Rolling back $STEPS migration(s)...${NC}"

for i in $(seq 1 $STEPS); do
    docker-compose exec -T backend alembic downgrade -1
    echo "Rolled back migration $i/$STEPS"
done

echo ""

# ===================================
# Show New Migration
# ===================================
echo -e "${GREEN}New database version:${NC}"
docker-compose exec -T backend alembic current
echo ""

echo -e "${GREEN}✓ Rollback completed successfully${NC}"
