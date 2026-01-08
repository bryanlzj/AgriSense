#!/bin/bash

# ===================================
# PostgreSQL Direct Setup Script
# ===================================
# This script sets up PostgreSQL database directly using SQLAlchemy models
# NO SQLite migration - PostgreSQL only!

set -e  # Exit on error

echo "================================================================================"
echo "🚀 AgriSense: PostgreSQL Direct Setup"
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
    echo "   cd backend && bash scripts/setup_postgres_direct.sh"
    exit 1
fi
echo "✅ In backend directory"

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
max_attempts=6
attempt=0
while [ $attempt -lt $max_attempts ]; do
    if docker-compose ps postgres | grep -q "healthy\|Up"; then
        echo "✅ PostgreSQL is ready"
        break
    else
        attempt=$((attempt + 1))
        if [ $attempt -eq $max_attempts ]; then
            echo "❌ PostgreSQL failed to start"
            exit 1
        fi
        echo "⏳ Still waiting... (attempt $attempt/$max_attempts)"
        sleep 5
    fi
done

echo ""

# ===================================
# Step 3: Create/Update .env file
# ===================================

if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
else
    echo "📝 Backing up existing .env to .env.backup..."
    cp .env .env.backup
fi

# Update DATABASE_URL in .env to use PostgreSQL
echo "📝 Updating DATABASE_URL to PostgreSQL..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    sed -i '' 's|^DATABASE_URL=.*|DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense|g' .env
    sed -i '' 's|^# POSTGRES_USER=|POSTGRES_USER=|g' .env
    sed -i '' 's|^# POSTGRES_PASSWORD=|POSTGRES_PASSWORD=|g' .env
    sed -i '' 's|^# POSTGRES_DB=|POSTGRES_DB=|g' .env
    sed -i '' 's|^# POSTGRES_HOST=|POSTGRES_HOST=|g' .env
    sed -i '' 's|^# POSTGRES_PORT=|POSTGRES_PORT=|g' .env
else
    # Linux
    sed -i 's|^DATABASE_URL=.*|DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense|g' .env
    sed -i 's|^# POSTGRES_USER=|POSTGRES_USER=|g' .env
    sed -i 's|^# POSTGRES_PASSWORD=|POSTGRES_PASSWORD=|g' .env
    sed -i 's|^# POSTGRES_DB=|POSTGRES_DB=|g' .env
    sed -i 's|^# POSTGRES_HOST=|POSTGRES_HOST=|g' .env
    sed -i 's|^# POSTGRES_PORT=|POSTGRES_PORT=|g' .env
fi

echo "✅ .env file configured for PostgreSQL"
echo ""

# ===================================
# Step 4: Install dependencies
# ===================================

echo "📦 Installing/Upgrading dependencies..."
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
echo "✅ Dependencies installed"
echo ""

# ===================================
# Step 5: Initialize PostgreSQL database
# ===================================

echo "🗄️  Initializing PostgreSQL database..."
echo "   - Creating tables from SQLAlchemy models"
echo "   - Seeding test data"
echo ""

python scripts/init_postgres.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Database initialization failed!"
    exit 1
fi

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
echo "📝 Test user credentials:"
echo "   Admin:   username='admin',   password='admin123'"
echo "   Farmer1: username='farmer1', password='password123'"
echo "   Farmer2: username='farmer2', password='password123'"
echo ""
echo "🚀 Next steps:"
echo "   1. Start backend: python run.py"
echo "   2. Test API: http://localhost:5000/docs"
echo "   3. View data in Adminer: http://localhost:8080"
echo ""
