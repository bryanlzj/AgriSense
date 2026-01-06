#!/bin/bash

# ===================================
# AgriSense Backend - Database Backup Script
# ===================================
# This script creates a backup of the PostgreSQL database
# Usage: ./scripts/backup.sh

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# ===================================
# Configuration
# ===================================
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
BACKUP_DIR="$PROJECT_ROOT/backups"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="$BACKUP_DIR/agrisense_backup_$TIMESTAMP.sql"

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   AgriSense Database Backup            ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# ===================================
# Create Backup Directory
# ===================================
mkdir -p "$BACKUP_DIR"

# ===================================
# Create Database Backup
# ===================================
echo -e "${YELLOW}Creating database backup...${NC}"

cd "$PROJECT_ROOT"
docker-compose exec -T postgres pg_dump -U agrisense_user agrisense > "$BACKUP_FILE"

# ===================================
# Compress Backup
# ===================================
echo -e "${YELLOW}Compressing backup...${NC}"
gzip "$BACKUP_FILE"
BACKUP_FILE="$BACKUP_FILE.gz"

# ===================================
# Show Backup Info
# ===================================
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)

echo ""
echo -e "${GREEN}✓ Backup completed successfully${NC}"
echo ""
echo "Backup file: $BACKUP_FILE"
echo "Backup size: $BACKUP_SIZE"
echo ""

# ===================================
# Cleanup Old Backups (keep last 7 days)
# ===================================
echo -e "${YELLOW}Cleaning up old backups (keeping last 7 days)...${NC}"
find "$BACKUP_DIR" -name "agrisense_backup_*.sql.gz" -mtime +7 -delete
echo -e "${GREEN}✓ Cleanup completed${NC}"
echo ""

# ===================================
# List All Backups
# ===================================
echo "Available backups:"
ls -lh "$BACKUP_DIR"
