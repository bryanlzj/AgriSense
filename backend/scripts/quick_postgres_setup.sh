#!/bin/bash

# ===================================
# Quick PostgreSQL Setup Script
# ===================================
# This script automates the entire PostgreSQL setup process

set -e  # Exit on error

echo "================================================================================"
echo "🚀 AgriSense: Quick PostgreSQL Setup"
echo "================================================================================"
echo ""

# ===================================
# Step 1: Check prerequisites
# ===================================

echo "📋 Checking prerequisites..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed"
    echo "   Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✅ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed"
    echo "   Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi
echo "✅ Docker Compose is installed"

# Check if we're in the backend directory
if [ ! -f "alembic.ini" ]; then
    echo "❌ Not in backend directory"
    echo "   Please run this script from the backend directory:"
    echo "   cd backend && bash scripts/quick_postgres_setup.sh"
    exit 1
fi
echo "✅ In backend directory"

# Check if SQLite database exists
if [ ! -f "agrisense.db" ]; then
    echo "⚠️  SQLite database not found"
    echo "   Creating seed data first..."
    python scripts/seed_data.py
fi
echo "✅ SQLite database exists"

echo ""

# ===================================
# Step 2: Start PostgreSQL and Adminer
# ===================================

echo "🐘 Starting PostgreSQL and Adminer..."
cd ..  # Go to project root
docker-compose up -d postgres adminer
cd backend

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

# Check if PostgreSQL is healthy
if docker-compose ps postgres | grep -q "healthy"; then
    echo "✅ PostgreSQL is ready"
else
    echo "⚠️  PostgreSQL is starting... waiting a bit more..."
    sleep 10
fi

echo ""

# ===================================
# Step 3: Create .env file if it doesn't exist
# ===================================

if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    
    # Update DATABASE_URL in .env
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' 's|DATABASE_URL=sqlite:///./agrisense.db|DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense|g' .env
    else
        # Linux
        sed -i 's|DATABASE_URL=sqlite:///./agrisense.db|DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense|g' .env
    fi
    
    echo "✅ .env file created and updated"
else
    echo "✅ .env file already exists"
fi

echo ""

# ===================================
# Step 4: Run database migrations
# ===================================

echo "🔄 Running database migrations..."
alembic upgrade head
echo "✅ Migrations complete"

echo ""

# ===================================
# Step 5: Migrate data from SQLite to PostgreSQL
# ===================================

echo "📦 Migrating data from SQLite to PostgreSQL..."
python scripts/migrate_sqlite_to_postgres.py

echo ""

# ===================================
# Step 6: Verify setup
# ===================================

echo "✅ Verifying setup..."

# Check if backend can connect to PostgreSQL
echo "🔍 Testing database connection..."
python -c "
from database import check_db_connection
if check_db_connection():
    print('✅ Backend can connect to PostgreSQL')
else:
    print('❌ Backend cannot connect to PostgreSQL')
    exit(1)
"

echo ""

# ===================================
# Done!
# ===================================

echo "================================================================================"
echo "🎉 PostgreSQL Setup Complete!"
echo "================================================================================"
echo ""
echo "📊 Your database is ready:"
echo "   - PostgreSQL running on: localhost:5432"
echo "   - Adminer running on: http://localhost:8080"
echo ""
echo "🔐 Adminer login credentials:"
echo "   System: PostgreSQL"
echo "   Server: postgres"
echo "   Username: agrisense_user"
echo "   Password: changeme"
echo "   Database: agrisense"
echo ""
echo "🚀 Next steps:"
echo "   1. Open Adminer: http://localhost:8080"
echo "   2. Start backend: python run.py"
echo "   3. Test API: http://localhost:5000/docs"
echo ""
echo "📚 For more details, see: POSTGRESQL_SETUP.md"
echo ""
