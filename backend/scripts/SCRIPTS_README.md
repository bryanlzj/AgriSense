# 📚 AgriSense Backend Scripts Documentation

This directory contains utility scripts for database management, setup, and maintenance.

## 🚀 Quick Start

### **For New Setup (PostgreSQL Direct)**

**Windows:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup script
cd backend
scripts\setup_postgres_direct.bat
```

**Linux/Mac:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup script
cd backend
bash scripts/setup_postgres_direct.sh
```

This will:
- ✅ Create all database tables from SQLAlchemy models
- ✅ Seed test data (users, sensor readings, pest detections, alerts)
- ✅ Configure .env file for PostgreSQL
- ✅ No SQLite migration needed!

---

## 📁 Script Categories

### 🔧 **Setup Scripts (Use These!)**

#### `init_postgres.py` ⭐ **RECOMMENDED**
**Purpose:** Initialize PostgreSQL database directly from SQLAlchemy models

**What it does:**
- Creates all tables using ORM (no migrations needed)
- Seeds test data (3 users, 7 days of sensor data, pest detections, alerts)
- Verifies setup

**Usage:**
```bash
python scripts/init_postgres.py
```

**Prerequisites:**
- PostgreSQL running (docker-compose up postgres)
- .env configured with PostgreSQL credentials

---

#### `setup_postgres_direct.sh` / `setup_postgres_direct.bat` ⭐ **RECOMMENDED**
**Purpose:** Complete automated setup for PostgreSQL

**What it does:**
- Starts PostgreSQL + Adminer containers
- Configures .env file
- Installs dependencies
- Runs init_postgres.py
- Shows access credentials

**Usage:**
```bash
# Linux/Mac
bash scripts/setup_postgres_direct.sh

# Windows
scripts\setup_postgres_direct.bat
```

---

#### `seed_data.py`
**Purpose:** Populate database with test data

**What it does:**
- Creates 3 test users (admin, farmer1, farmer2)
- Generates 7 days of hourly sensor readings
- Creates sample pest detections
- Creates sample alerts

**Usage:**
```bash
python scripts/seed_data.py
```

**Note:** Works with both SQLite and PostgreSQL

---

### 🗄️ **Database Management Scripts**

#### `start-database.bat` (Windows)
**Purpose:** Start PostgreSQL and Adminer containers

**Usage:**
```bash
scripts\start-database.bat
```

---

#### `stop-database.bat` (Windows)
**Purpose:** Stop PostgreSQL and Adminer containers

**Usage:**
```bash
scripts\stop-database.bat
```

---

#### `reset_postgres.bat` (Windows)
**Purpose:** Reset PostgreSQL database (drop and recreate schema)

**Usage:**
```bash
scripts\reset_postgres.bat
```

**⚠️ WARNING:** This deletes ALL data!

---

### 📦 **Legacy Migration Scripts (Not Needed)**

These scripts were used to migrate from SQLite to PostgreSQL. Since we now use PostgreSQL directly, these are **NOT NEEDED** for new setups:

- ❌ `migrate_sqlite_to_postgres.py` - Migrates data from SQLite to PostgreSQL
- ❌ `quick_postgres_setup.sh` - Old setup script with migration
- ❌ `setup_postgres.bat` - Old Windows setup with migration
- ❌ `setup_postgres.ps1` - Old PowerShell setup with migration
- ❌ `START_HERE.bat` - Old Windows quick start with migration

**Why not needed?**
- We create PostgreSQL tables directly from SQLAlchemy models
- No SQLite database to migrate from
- Simpler and faster setup

---

### 💾 **Backup & Restore Scripts**

#### `backup.sh` (Linux/Mac)
**Purpose:** Create timestamped database backup

**What it does:**
- Creates compressed backup (.sql.gz)
- Stores in /backups directory
- Cleans up old backups (keeps last 7 days)

**Usage:**
```bash
bash scripts/backup.sh
```

---

#### `restore.sh` (Linux/Mac)
**Purpose:** Restore database from backup

**Usage:**
```bash
bash scripts/restore.sh backups/agrisense_backup_20250104_120000.sql.gz
```

**⚠️ WARNING:** This replaces current database!

---

#### `rollback.sh` (Linux/Mac)
**Purpose:** Rollback database migrations

**Usage:**
```bash
# Rollback 1 migration
bash scripts/rollback.sh 1

# Rollback 3 migrations
bash scripts/rollback.sh 3
```

---

### 🚀 **Deployment Scripts**

#### `deploy.sh` (Linux/Mac)
**Purpose:** Automated production deployment

**What it does:**
- Pulls latest code from Git
- Stops running containers
- Builds Docker images
- Starts services
- Runs database migrations
- Verifies deployment

**Usage:**
```bash
bash scripts/deploy.sh
```

---

## 🎯 Common Tasks

### **First-Time Setup**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup script
cd backend
bash scripts/setup_postgres_direct.sh  # Linux/Mac
# OR
scripts\setup_postgres_direct.bat      # Windows
```

---

### **Reset Database (Fresh Start)**
```bash
# Windows
scripts\reset_postgres.bat
python scripts/init_postgres.py

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python scripts/init_postgres.py
```

---

### **Add More Test Data**
```bash
python scripts/seed_data.py
```

---

### **Backup Database**
```bash
bash scripts/backup.sh
```

---

### **Restore Database**
```bash
bash scripts/restore.sh backups/agrisense_backup_YYYYMMDD_HHMMSS.sql.gz
```

---

## 🔐 Default Credentials

### **PostgreSQL Database**
- Host: `localhost`
- Port: `5432`
- Database: `agrisense`
- Username: `agrisense_user`
- Password: `changeme`

### **Adminer (Database UI)**
- URL: http://localhost:8080
- System: `PostgreSQL`
- Server: `postgres`
- Username: `agrisense_user`
- Password: `changeme`
- Database: `agrisense`

### **Test Users**
- Admin: `admin` / `admin123`
- Farmer 1: `farmer1` / `password123`
- Farmer 2: `farmer2` / `password123`

---

## 📊 Database Schema

The database has 4 main tables:

1. **users** - User accounts
2. **sensor_readings** - Environmental sensor data (temperature, humidity, soil moisture, light)
3. **pest_detections** - ML-based pest detection results
4. **alerts** - Weather warnings and pest risk alerts

All tables are created from SQLAlchemy models in `/backend/models/`

---

## 🛠️ Troubleshooting

### **"Cannot connect to PostgreSQL"**
```bash
# Check if PostgreSQL is running
docker ps

# Start PostgreSQL
docker-compose up -d postgres

# Check logs
docker logs agrisense-postgres
```

---

### **"Tables already exist"**
This is normal! The scripts handle existing tables gracefully.

To reset:
```bash
# Windows
scripts\reset_postgres.bat

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

---

### **"Module not found" errors**
```bash
# Install dependencies
pip install -r requirements.txt
```

---

### **"Permission denied" (Linux/Mac)**
```bash
# Make scripts executable
chmod +x scripts/*.sh
```

---

## 📝 Notes

- **PostgreSQL is the primary database** - No SQLite needed
- **Models define schema** - Tables created from SQLAlchemy models
- **Alembic for migrations** - Use for schema changes in production
- **Seed data for testing** - Run seed_data.py anytime for fresh test data

---

## 🔗 Related Documentation

- [PostgreSQL Setup Guide](../docs/POSTGRESQL_SETUP.md)
- [Database Models](../models/)
- [API Documentation](http://localhost:5000/docs)

---

## 📞 Support

If you encounter issues:
1. Check PostgreSQL is running: `docker ps`
2. Check .env configuration
3. Review logs: `docker logs agrisense-postgres`
4. Reset database and try again

---

**Last Updated:** January 2025
