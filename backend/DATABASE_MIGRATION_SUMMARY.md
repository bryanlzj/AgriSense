# 📊 Database Migration Summary

## What We've Set Up

### 🎯 Goal
Switch from SQLite (single-file database) to PostgreSQL (production-grade database) + add Adminer (database management tool)

---

## 📦 What's Been Added

### 1. **Adminer** (Database Management Tool)
- **Added to:** `docker-compose.yml`
- **Access:** http://localhost:8080
- **Purpose:** Visual interface to manage your database (like phpMyAdmin)
- **Features:**
  - Browse tables
  - Edit/add/delete records
  - Run SQL queries
  - Export/import data
  - View table structure

### 2. **Migration Script** 
- **File:** `backend/scripts/migrate_sqlite_to_postgres.py`
- **Purpose:** Automatically transfer all data from SQLite to PostgreSQL
- **What it migrates:**
  - ✅ All users (3 users)
  - ✅ All sensor readings (504 readings)
  - ✅ All pest detections (9 detections)
  - ✅ All alerts (12 alerts)
- **Safety:** Preserves all IDs and relationships

### 3. **Quick Setup Script**
- **File:** `backend/scripts/quick_postgres_setup.sh`
- **Purpose:** One-command setup for everything
- **What it does:**
  1. Starts PostgreSQL + Adminer
  2. Updates .env file
  3. Runs migrations
  4. Migrates data
  5. Verifies setup

### 4. **Documentation**
- **QUICK_START_POSTGRESQL.md** - 5-minute quick start guide
- **POSTGRESQL_SETUP.md** - Detailed step-by-step guide (486 lines)
- **DATABASE_MIGRATION_SUMMARY.md** - This file

---

## 🚀 How to Use (3 Options)

### Option 1: Automated (Easiest) ⭐
```bash
cd backend
bash scripts/quick_postgres_setup.sh
```
**Time:** 2-3 minutes  
**Difficulty:** Easy (fully automated)

---

### Option 2: Manual (Step-by-step)
```bash
# 1. Start PostgreSQL and Adminer
docker-compose up -d postgres adminer

# 2. Update .env file
# Edit backend/.env and change:
# DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense

# 3. Run migrations
cd backend
alembic upgrade head

# 4. Migrate data
python scripts/migrate_sqlite_to_postgres.py
```
**Time:** 5 minutes  
**Difficulty:** Medium (requires manual steps)

---

### Option 3: Keep SQLite (No Changes)
If you want to keep using SQLite:
- Do nothing! Your current setup still works
- SQLite is great for development
- Switch to PostgreSQL when you're ready for production

---

## 🌐 Access Points After Setup

| Service | URL | Credentials |
|---------|-----|-------------|
| **Backend API** | http://localhost:5000 | - |
| **Swagger Docs** | http://localhost:5000/docs | - |
| **Adminer** | http://localhost:8080 | See below ⬇️ |
| **PostgreSQL** | localhost:5432 | See below ⬇️ |

### Adminer Login:
- **System:** PostgreSQL
- **Server:** postgres
- **Username:** agrisense_user
- **Password:** changeme
- **Database:** agrisense

### PostgreSQL Direct Connection:
```bash
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense
```

---

## 📊 Database Comparison

| Feature | SQLite (Current) | PostgreSQL (New) |
|---------|------------------|------------------|
| **File** | `agrisense.db` (single file) | Docker container |
| **Setup** | ✅ Zero config | ⚠️ Requires Docker |
| **Performance** | ✅ Fast for small data | ✅ Faster for large data |
| **Concurrent Users** | ❌ Limited (1-2) | ✅ Excellent (100+) |
| **Production Ready** | ❌ Not recommended | ✅ Industry standard |
| **Management Tool** | ⚠️ DB Browser (external) | ✅ Adminer (built-in) |
| **Backup** | ✅ Copy file | ⚠️ Requires pg_dump |
| **Your Data** | ✅ 528 records | ✅ Same 528 records |

---

## 🎯 What Happens to Your SQLite Data?

### Before Migration:
```
backend/
├── agrisense.db          ← Your current SQLite database
│   ├── 3 users
│   ├── 504 sensor readings
│   ├── 9 pest detections
│   └── 12 alerts
```

### After Migration:
```
backend/
├── agrisense.db          ← Still here! (backup)
│   └── All data preserved
│
PostgreSQL (Docker):
├── users                 ← Copied from SQLite
├── sensor_readings       ← Copied from SQLite
├── pest_detections       ← Copied from SQLite
└── alerts                ← Copied from SQLite
```

**Important:** Your SQLite file is NOT deleted! It stays as a backup.

---

## 🔍 Verify Migration Success

### 1. Check Record Counts in Adminer
1. Go to http://localhost:8080
2. Login with credentials
3. Click each table and verify counts:
   - **users:** 3 records
   - **sensor_readings:** 504 records
   - **pest_detections:** 9 records
   - **alerts:** 12 records

### 2. Check Backend Connection
```bash
curl http://localhost:5000/health
```
Should show:
```json
{
  "status": "healthy",
  "database": "connected",
  "database_type": "postgresql"
}
```

### 3. Test Login
```bash
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
Should return a JWT token.

---

## 🎨 Adminer Features Demo

### Browse Tables
1. Click "users" → See all 3 users
2. Click "sensor_readings" → See 504 readings with pagination
3. Click "pest_detections" → See 9 detections with images
4. Click "alerts" → See 12 alerts

### Run SQL Queries
Click "SQL command" and try:

```sql
-- Get all users
SELECT * FROM users;

-- Get sensor readings from last 24 hours
SELECT * FROM sensor_readings 
WHERE timestamp > NOW() - INTERVAL '24 hours'
ORDER BY timestamp DESC;

-- Get high-confidence pest detections
SELECT * FROM pest_detections 
WHERE confidence > 0.8
ORDER BY detected_at DESC;

-- Get unread alerts
SELECT * FROM alerts 
WHERE is_read = false
ORDER BY created_at DESC;

-- Get user with most sensor readings
SELECT u.username, COUNT(s.id) as reading_count
FROM users u
LEFT JOIN sensor_readings s ON u.id = s.user_id
GROUP BY u.username
ORDER BY reading_count DESC;
```

### Edit Data
1. Click any table
2. Click "edit" next to a record
3. Change values
4. Click "Save"

### Add New Records
1. Click any table
2. Click "New item"
3. Fill in form
4. Click "Save"

### Export Data
1. Click "Export" in left menu
2. Choose format (SQL, CSV, JSON)
3. Click "Export"
4. Download file

---

## 🔄 Common Tasks

### Start Services
```bash
docker-compose up -d postgres adminer
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f postgres
```

### Backup Database
```bash
docker exec -t agrisense-postgres pg_dump -U agrisense_user agrisense > backup.sql
```

### Restore Database
```bash
cat backup.sql | docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense
```

### Connect to PostgreSQL CLI
```bash
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense
```

### Switch Back to SQLite
Edit `backend/.env`:
```bash
DATABASE_URL=sqlite:///./agrisense.db
```
Restart backend. Done!

---

## 🐛 Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| "Connection refused" | `docker-compose up -d postgres` |
| "Password authentication failed" | Check .env has correct credentials |
| "Database does not exist" | `docker exec -it agrisense-postgres psql -U agrisense_user -c "CREATE DATABASE agrisense;"` |
| Adminer shows empty database | Run migrations: `alembic upgrade head` |
| Migration script fails | Make sure you're in backend directory |
| Can't access Adminer | Check port 8080 is not in use |

---

## 📚 Documentation Files

1. **QUICK_START_POSTGRESQL.md** (270 lines)
   - 5-minute quick start
   - Automated setup instructions
   - Adminer usage guide

2. **POSTGRESQL_SETUP.md** (486 lines)
   - Detailed step-by-step guide
   - Troubleshooting section
   - Database comparison
   - Advanced usage

3. **DATABASE_MIGRATION_SUMMARY.md** (this file)
   - Overview of changes
   - Quick reference
   - Visual guides

---

## ✅ Next Steps

After successful migration:

1. ✅ **Test all API endpoints** in Swagger UI
2. ✅ **Explore data in Adminer** (http://localhost:8080)
3. ✅ **Update your .env file** for production
4. ✅ **Change default password** from "changeme" to something secure
5. ✅ **Create database backups** regularly
6. ✅ **Update documentation** with PostgreSQL setup
7. ✅ **Deploy to production** with Docker Compose

---

## 🎉 Benefits of This Setup

### For Development:
- ✅ **Visual database management** with Adminer
- ✅ **Easy data inspection** without SQL knowledge
- ✅ **Quick data editing** for testing
- ✅ **SQL query playground** for learning
- ✅ **Production-like environment** locally

### For Production:
- ✅ **Industry-standard database** (PostgreSQL)
- ✅ **Better performance** with large datasets
- ✅ **Concurrent user support** (100+ users)
- ✅ **Advanced features** (JSON, full-text search)
- ✅ **Easy deployment** with Docker Compose

### For Learning:
- ✅ **Understand database migrations**
- ✅ **Learn PostgreSQL** (most popular DB)
- ✅ **Practice SQL queries** in Adminer
- ✅ **See data relationships** visually
- ✅ **Professional development workflow**

---

## 🔗 Quick Links

- **Adminer:** http://localhost:8080
- **Backend API:** http://localhost:5000
- **Swagger Docs:** http://localhost:5000/docs
- **Health Check:** http://localhost:5000/health

---

**Created:** January 2025  
**Status:** Ready to use! 🚀  
**Estimated Setup Time:** 5 minutes  
**Difficulty:** Easy (automated script available)
