#!/bin/bash

# ===================================
# AgriSense Backend - Database Restore Script
# ===================================
# This script restores a PostgreSQL database backup
# Usage: ./scripts/restore.sh <backup_file>
# Example: ./scripts/restore.sh backups/agrisense_backup_20250104_120000.sql.gz

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ===================================
# Configuration
# ===================================
BACKUP_FILE=$1
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

echo -e "${YELLOW}╔════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║   AgriSense Database Restore           ║${NC}"
echo -e "${YELLOW}╚════════════════════════════════════════╝${NC}"
echo ""

# ===================================
# Validate Input
# ===================================
if [ -z "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: No backup file specified${NC}"
    echo "Usage: ./scripts/restore.sh <backup_file>"
    echo ""
    echo "Available backups:"
    ls -lh "$PROJECT_ROOT/backups" 2>/dev/null || echo "No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

# ===================================
# Confirmation
# ===================================
echo -e "${RED}WARNING: This will replace the current database!${NC}"
echo -e "${RED}All current data will be lost.${NC}"
echo ""
echo "Backup file: $BACKUP_FILE"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# ===================================
# Decompress if Needed
# ===================================
if [[ "$BACKUP_FILE" == *.gz ]]; then
    echo -e "${YELLOW}Decompressing backup...${NC}"
    TEMP_FILE="${BACKUP_FILE%.gz}"
    gunzip -c "$BACKUP_FILE" > "$TEMP_FILE"
    BACKUP_FILE="$TEMP_FILE"
fi

# ===================================
# Drop and Recreate Database
# ===================================
echo -e "${YELLOW}Dropping existing database...${NC}"
cd "$PROJECT_ROOT"
docker-compose exec -T postgres psql -U agrisense_user -c "DROP DATABASE IF EXISTS agrisense;"
docker-compose exec -T postgres psql -U agrisense_user -c "CREATE DATABASE agrisense;"

# ===================================
# Restore Database
# ===================================
echo -e "${YELLOW}Restoring database...${NC}"
cat "$BACKUP_FILE" | docker-compose exec -T postgres psql -U agrisense_user agrisense

# ===================================
# Cleanup Temp File
# ===================================
if [ -n "$TEMP_FILE" ]; then
    rm -f "$TEMP_FILE"
fi

# ===================================
# Verify Restore
# ===================================
echo ""
echo -e "${YELLOW}Verifying restore...${NC}"
docker-compose exec -T postgres psql -U agrisense_user agrisense -c "\dt"

echo ""
echo -e "${GREEN}✓ Database restored successfully${NC}"
