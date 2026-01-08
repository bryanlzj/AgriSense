# 📜 Backend Scripts

## ⚠️ Important Notice

**Most scripts in this folder are no longer needed!**

The backend now automatically handles database initialization on startup. Simply run:

```bash
python run.py
```

The system will automatically:
- ✅ Check database connection
- ✅ Create missing tables
- ✅ Seed test data (if `SEED_DATABASE=True`)

---

## 🗑️ Legacy Scripts (Not Needed)

These scripts were used in the old setup but are **no longer required**:

### ❌ Initialization Scripts
- `init_postgres.py` - Replaced by automatic initialization in `db_init.py`
- `setup_postgres_direct.sh` - No longer needed
- `setup_postgres_direct.bat` - No longer needed
- `quick_postgres_setup.sh` - No longer needed
- `setup_postgres.bat` - No longer needed
- `setup_postgres.ps1` - No longer needed
- `START_HERE.bat` - No longer needed

### ❌ Migration Scripts
- `migrate_sqlite_to_postgres.py` - System uses PostgreSQL directly now

### ❌ Seeding Scripts
- `seed_data.py` - Seeding happens automatically via `SEED_DATABASE` flag

---

## ✅ Useful Scripts (Keep These)

### **Database Management**

#### `start-database.bat` (Windows)
Start PostgreSQL and Adminer containers:
```bash
scripts\start-database.bat
```

#### `stop-database.bat` (Windows)
Stop database containers:
```bash
scripts\stop-database.bat
```

#### `reset_postgres.bat` (Windows)
Reset the database (drops all tables):
```bash
scripts\reset_postgres.bat
```

After reset, restart the backend to recreate tables:
```bash
python run.py
```

---

### **Backup & Restore** (Linux/Mac)

#### `backup.sh`
Create a database backup:
```bash
bash scripts/backup.sh
```

Creates timestamped backup in `backups/` directory.

#### `restore.sh`
Restore from a backup:
```bash
bash scripts/restore.sh backups/agrisense_backup_YYYYMMDD_HHMMSS.sql.gz
```

#### `rollback.sh`
Rollback Alembic migrations:
```bash
bash scripts/rollback.sh 1  # Rollback 1 migration
```

---

### **Deployment**

#### `deploy.sh` (Linux/Mac)
Production deployment script:
```bash
bash scripts/deploy.sh
```

This script:
- Pulls latest code
- Rebuilds containers
- Runs migrations
- Restarts services

---

## 🎯 Common Tasks

### First-Time Setup

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Configure environment
cp .env.example .env

# 3. Start backend (automatic initialization)
python run.py
```

### Reset Database

```bash
# Windows
scripts\reset_postgres.bat
python run.py

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python run.py
```

### Backup Database

```bash
# Linux/Mac
bash scripts/backup.sh

# Windows (manual)
docker exec agrisense-postgres pg_dump -U agrisense_user agrisense > backup.sql
```

### View Database

Open Adminer: http://localhost:8080
- System: `PostgreSQL`
- Server: `postgres`
- Username: `agrisense_user`
- Password: `changeme`
- Database: `agrisense`

---

## 🔄 Migration from Old Setup

If you were using the old scripts:

### Old Way:
```bash
bash scripts/setup_postgres_direct.sh
python scripts/init_postgres.py
python scripts/seed_data.py
```

### New Way:
```bash
# Just set SEED_DATABASE=True in .env
python run.py
```

That's it! Everything happens automatically.

---

## 📝 Script Cleanup Recommendations

You can safely delete these legacy scripts:

```bash
cd backend/scripts
rm -f init_postgres.py
rm -f setup_postgres_direct.sh
rm -f setup_postgres_direct.bat
rm -f quick_postgres_setup.sh
rm -f setup_postgres.bat
rm -f setup_postgres.ps1
rm -f START_HERE.bat
rm -f migrate_sqlite_to_postgres.py
rm -f seed_data.py
```

**Keep these:**
- `start-database.bat` / `stop-database.bat` (Windows)
- `reset_postgres.bat` (Windows)
- `backup.sh` / `restore.sh` / `rollback.sh` (Linux/Mac)
- `deploy.sh` (Linux/Mac)
- `README.md` (this file)
- `FIX_MIGRATION.md` (reference)

---

## 🎓 Understanding the New System

### Automatic Initialization

The backend uses a `lifespan` event handler in `main.py`:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Runs on startup
    from db_init import initialize_database
    initialize_database()
    
    yield
    
    # Runs on shutdown
    # Cleanup code here
```

### Database Initialization Flow

1. **Check Connection** - Verify PostgreSQL is accessible
2. **Compare Schema** - Check existing tables vs. models
3. **Create Missing Tables** - Add any missing tables
4. **Seed Data** (optional) - If `SEED_DATABASE=True` and database is empty

### Benefits

- ✅ No manual scripts to run
- ✅ Automatic schema updates
- ✅ Consistent across environments
- ✅ Simpler deployment
- ✅ Less room for error

---

## 🔧 Troubleshooting

### "Database already has data"

This is normal! The system detects existing data and skips seeding.

To force re-seed:
1. Reset database: `scripts\reset_postgres.bat`
2. Restart backend: `python run.py`

### "Cannot connect to database"

Check if PostgreSQL is running:
```bash
docker ps
```

Start it:
```bash
docker-compose up -d postgres
```

### "Tables already exist"

This is expected behavior. The system only creates missing tables.

---

## 📚 Documentation

- **Main README:** `/backend/README.md`
- **API Docs:** http://localhost:5000/docs
- **Database Schema:** See `/backend/models/`

---

**Last Updated:** January 2025

**Note:** This folder contains legacy scripts for reference. Most functionality is now built into the backend startup process.
