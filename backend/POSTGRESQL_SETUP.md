# PostgreSQL Setup Guide for AgriSense

This guide will help you switch from SQLite to PostgreSQL and set up Adminer for database management.

---

## 📋 Table of Contents

1. [Why PostgreSQL?](#why-postgresql)
2. [Prerequisites](#prerequisites)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Using Adminer](#using-adminer)
5. [Troubleshooting](#troubleshooting)

---

## 🐘 Why PostgreSQL?

**SQLite is great for:**
- ✅ Learning and development
- ✅ Single-user applications
- ✅ Quick prototyping

**PostgreSQL is better for:**
- ✅ Production deployments
- ✅ Multiple concurrent users
- ✅ Better performance with large datasets
- ✅ Advanced features (JSON, full-text search, etc.)
- ✅ Industry standard for web applications

---

## 📦 Prerequisites

1. **Docker and Docker Compose installed**
   - Check: `docker --version` and `docker-compose --version`
   - If not installed: https://docs.docker.com/get-docker/

2. **Existing SQLite database with data**
   - File: `backend/agrisense.db`
   - If you don't have data, run: `python scripts/seed_data.py`

3. **Backend dependencies installed**
   - Run: `pip install -r requirements.txt`

---

## 🚀 Step-by-Step Setup

### Step 1: Start PostgreSQL and Adminer

```bash
# From the project root directory
docker-compose up -d postgres adminer
```

**What this does:**
- Starts PostgreSQL database on port 5432
- Starts Adminer (database management tool) on port 8080
- Creates a persistent volume for database data

**Verify it's running:**
```bash
docker-compose ps
```

You should see:
```
NAME                    STATUS
agrisense-postgres      Up (healthy)
agrisense-adminer       Up
```

---

### Step 2: Create .env file with PostgreSQL credentials

```bash
# Copy the example file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

**Update these lines in .env:**

```bash
# Database Configuration
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense

# PostgreSQL credentials (must match docker-compose.yml)
POSTGRES_USER=agrisense_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=agrisense
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

**⚠️ IMPORTANT:** Change `changeme` to a secure password in production!

---

### Step 3: Run database migrations

```bash
# From the backend directory
cd backend

# Run Alembic migrations to create tables in PostgreSQL
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade -> abc123, Initial migration
INFO  [alembic.runtime.migration] Running upgrade abc123 -> def456, Add users table
...
```

**Verify tables were created:**
```bash
# Connect to PostgreSQL
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense

# List tables
\dt

# You should see:
#  users
#  sensor_readings
#  pest_detections
#  alerts
#  alembic_version

# Exit psql
\q
```

---

### Step 4: Migrate data from SQLite to PostgreSQL

```bash
# From the backend directory
python scripts/migrate_sqlite_to_postgres.py
```

**What this script does:**
1. ✅ Reads all data from `agrisense.db` (SQLite)
2. ✅ Connects to PostgreSQL
3. ✅ Clears existing data in PostgreSQL (if any)
4. ✅ Transfers all users, sensor readings, pest detections, and alerts
5. ✅ Preserves all IDs and relationships
6. ✅ Verifies migration was successful

**Expected output:**
```
================================================================================
🚀 AgriSense: SQLite to PostgreSQL Migration
================================================================================

📂 Found SQLite database: /path/to/backend/agrisense.db
🐘 Connecting to PostgreSQL at localhost:5432/agrisense
✅ PostgreSQL connection successful

📊 Records in SQLite database:
   Users: 3
   Sensor Readings: 504
   Pest Detections: 9
   Alerts: 12

🗑️  Clearing existing data in PostgreSQL...
✅ PostgreSQL tables cleared

👤 Migrating users...
✅ Migrated 3 users

📊 Migrating sensor readings...
✅ Migrated 504 sensor readings

🐛 Migrating pest detections...
✅ Migrated 9 pest detections

🔔 Migrating alerts...
✅ Migrated 12 alerts

✅ Verifying migration...

📊 Records in PostgreSQL database:
   Users: 3 (expected: 3)
   Sensor Readings: 504 (expected: 504)
   Pest Detections: 9 (expected: 9)
   Alerts: 12 (expected: 12)

🎉 Migration completed successfully!
   All data has been transferred from SQLite to PostgreSQL

================================================================================
✅ MIGRATION COMPLETE
================================================================================
```

---

### Step 5: Test the backend with PostgreSQL

```bash
# Start the backend server
python run.py
```

**Test endpoints:**

1. **Health check:**
   ```bash
   curl http://localhost:5000/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "timestamp": "2025-01-04T10:30:00Z",
     "database": "connected",
     "database_type": "postgresql"
   }
   ```

2. **Login with test user:**
   ```bash
   curl -X POST http://localhost:5000/api/v1/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'
   ```

3. **Open Swagger UI:**
   - Go to: http://localhost:5000/docs
   - Test all endpoints

---

## 🔧 Using Adminer

Adminer is a lightweight database management tool (like phpMyAdmin but better).

### Access Adminer

1. **Open in browser:** http://localhost:8080

2. **Login credentials:**
   - **System:** PostgreSQL
   - **Server:** postgres
   - **Username:** agrisense_user
   - **Password:** changeme
   - **Database:** agrisense

3. **Click "Login"**

### What you can do in Adminer:

#### 1. Browse Tables
- Click on any table name (users, sensor_readings, etc.)
- View all records
- Sort and filter data

#### 2. Run SQL Queries
- Click "SQL command" in the left menu
- Write custom queries:
  ```sql
  -- Get all users
  SELECT * FROM users;
  
  -- Get sensor readings from last 24 hours
  SELECT * FROM sensor_readings 
  WHERE timestamp > NOW() - INTERVAL '24 hours'
  ORDER BY timestamp DESC;
  
  -- Get pest detections with high confidence
  SELECT * FROM pest_detections 
  WHERE confidence > 0.8
  ORDER BY detected_at DESC;
  
  -- Get unread alerts
  SELECT * FROM alerts 
  WHERE is_read = false
  ORDER BY created_at DESC;
  ```

#### 3. Edit Data
- Click on any table
- Click "edit" next to a record
- Modify values
- Click "Save"

#### 4. Add New Records
- Click on any table
- Click "New item"
- Fill in values
- Click "Save"

#### 5. Delete Records
- Click on any table
- Check the checkbox next to records
- Click "Delete" at the bottom

#### 6. Export Data
- Click "Export" in the left menu
- Choose format (SQL, CSV, etc.)
- Click "Export"

#### 7. Import Data
- Click "Import" in the left menu
- Choose file
- Click "Execute"

#### 8. View Table Structure
- Click on any table
- Click "Show structure"
- See columns, types, indexes, foreign keys

---

## 🐛 Troubleshooting

### Issue 1: "Connection refused" when connecting to PostgreSQL

**Solution:**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# If not running, start it
docker-compose up -d postgres

# Check logs
docker-compose logs postgres
```

---

### Issue 2: "Password authentication failed"

**Solution:**
```bash
# Make sure credentials in .env match docker-compose.yml
# Default credentials:
POSTGRES_USER=agrisense_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=agrisense
```

---

### Issue 3: "Database does not exist"

**Solution:**
```bash
# PostgreSQL creates the database automatically
# But if it doesn't exist, create it manually:
docker exec -it agrisense-postgres psql -U agrisense_user -c "CREATE DATABASE agrisense;"
```

---

### Issue 4: "Alembic migration failed"

**Solution:**
```bash
# Check current migration version
alembic current

# If stuck, reset to base
alembic downgrade base

# Then upgrade again
alembic upgrade head
```

---

### Issue 5: "Migration script can't find SQLite database"

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Check if agrisense.db exists
ls -la agrisense.db

# If not, seed data first
python scripts/seed_data.py

# Then run migration
python scripts/migrate_sqlite_to_postgres.py
```

---

### Issue 6: "Adminer shows empty database"

**Solution:**
```bash
# Make sure you ran migrations
alembic upgrade head

# Make sure you ran data migration
python scripts/migrate_sqlite_to_postgres.py

# Check if data exists in PostgreSQL
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense -c "SELECT COUNT(*) FROM users;"
```

---

## 🔄 Switching Back to SQLite (if needed)

If you want to switch back to SQLite for development:

1. **Update .env:**
   ```bash
   DATABASE_URL=sqlite:///./agrisense.db
   ```

2. **Restart backend:**
   ```bash
   python run.py
   ```

That's it! The backend will automatically use SQLite.

---

## 📊 Database Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Setup** | ✅ Zero config | ⚠️ Requires server |
| **Performance** | ✅ Fast for small data | ✅ Fast for large data |
| **Concurrent Users** | ❌ Limited | ✅ Excellent |
| **Data Size** | ⚠️ Up to ~1GB | ✅ Unlimited |
| **Production Ready** | ❌ Not recommended | ✅ Industry standard |
| **Backup** | ✅ Copy file | ⚠️ Requires pg_dump |
| **Management Tools** | ⚠️ Limited | ✅ Many options |

---

## 🎯 Next Steps

After setting up PostgreSQL:

1. ✅ **Update your .env file** to use PostgreSQL URL
2. ✅ **Run migrations** with Alembic
3. ✅ **Migrate your data** from SQLite
4. ✅ **Test all endpoints** in Swagger UI
5. ✅ **Explore data** in Adminer
6. ✅ **Update documentation** with PostgreSQL setup
7. ✅ **Deploy to production** with Docker Compose

---

## 📚 Additional Resources

- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **Adminer Documentation:** https://www.adminer.org/
- **SQLAlchemy PostgreSQL:** https://docs.sqlalchemy.org/en/20/dialects/postgresql.html
- **Docker PostgreSQL:** https://hub.docker.com/_/postgres

---

## 🆘 Need Help?

If you encounter issues:

1. Check the logs: `docker-compose logs postgres`
2. Check backend logs: `python run.py` (look for errors)
3. Check Adminer connection settings
4. Verify .env file has correct credentials
5. Make sure PostgreSQL is running: `docker-compose ps`

---

**Last Updated:** January 2025  
**Status:** Ready for use! 🚀
