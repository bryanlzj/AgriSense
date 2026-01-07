# AgriSense Scripts

All utility scripts for AgriSense backend.

## 🚀 Quick Start (Windows)

**Double-click:** `START_HERE.bat`

This will automatically:
1. Start PostgreSQL + Adminer
2. Create database tables
3. Migrate your data from SQLite

Then run:
```bash
cd backend
python run.py
```

---

## 📁 Available Scripts

### Setup Scripts
- **`START_HERE.bat`** - Complete automated setup (Windows)
- **`setup_postgres.ps1`** - PowerShell setup script
- **`setup_postgres.bat`** - Batch setup script
- **`start-database.bat`** - Start PostgreSQL + Adminer only
- **`stop-database.bat`** - Stop database services

### Database Scripts
- **`migrate_sqlite_to_postgres.py`** - Migrate data from SQLite to PostgreSQL
- **`seed_data.py`** - Seed database with test data
- **`backup.sh`** - Backup database (Linux/Mac)
- **`restore.sh`** - Restore database (Linux/Mac)
- **`rollback.sh`** - Rollback migrations (Linux/Mac)

### Deployment Scripts
- **`deploy.sh`** - Deploy to production (Linux/Mac)
- **`quick_postgres_setup.sh`** - Quick PostgreSQL setup (Linux/Mac)

---

## 🎯 Common Tasks

### First Time Setup
```bash
# Windows
START_HERE.bat

# Linux/Mac
bash quick_postgres_setup.sh
```

### Start Database Only
```bash
# Windows
start-database.bat

# Linux/Mac
docker compose up postgres adminer -d
```

### Migrate Data from SQLite
```bash
python migrate_sqlite_to_postgres.py
```

### Seed Test Data
```bash
python seed_data.py
```

---

## 🌐 Access Points

| Service | URL | Credentials |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | - |
| API Docs | http://localhost:8000/docs | - |
| Adminer | http://localhost:8080 | postgres / agrisense_user / changeme / agrisense |

---

## 📝 Notes

- All scripts assume you're running from the `backend/scripts/` directory
- Make sure Docker Desktop is running before executing setup scripts
- Your SQLite database (`agrisense.db`) is kept as a backup after migration
