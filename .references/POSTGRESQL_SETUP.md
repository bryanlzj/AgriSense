# PostgreSQL + Adminer Setup

## 🚀 Quick Setup (Automated)

### Step 1: Start PostgreSQL + Adminer

```bash
# From project root
docker compose -f docker-compose.db.yml up -d
```

This starts:
- **PostgreSQL** on port 5432
- **Adminer** on port 8080 (database manager)

### Step 2: Run Setup Script

**Windows (PowerShell - Recommended):**
```powershell
cd backend
powershell -ExecutionPolicy Bypass -File scripts/setup_postgres.ps1
```

**Windows (Batch):**
```cmd
cd backend
scripts\setup_postgres.bat
```

**Linux/Mac:**
```bash
cd backend
bash scripts/quick_postgres_setup.sh
```

**The script will:**
1. ✅ Update your `.env` file to use PostgreSQL
2. ✅ Run Alembic migrations (create tables)
3. ✅ Migrate all your data from SQLite
4. ✅ Verify everything works

**Time:** 2-3 minutes  
**Your data:** Safely preserved (SQLite file stays as backup)

---

## 🌐 Access Adminer (Database Manager)

**URL:** http://localhost:8080

**Login:**
- System: **PostgreSQL**
- Server: **postgres**
- Username: **agrisense_user**
- Password: **changeme**
- Database: **agrisense**

**What you can do in Adminer:**
- 📊 Browse all tables (users, sensor_readings, pest_detections, alerts)
- ✏️ Edit records with visual forms
- ➕ Add new records easily
- 🗑️ Delete records with one click
- 🔍 Run SQL queries with syntax highlighting
- 📥 Export data (CSV, SQL, JSON)
- 📤 Import data from files

---

## 🔧 Manual Setup (If Script Fails)

### 1. Start Services
```bash
# From project root
docker compose -f docker-compose.db.yml up -d
```

### 2. Update .env File
```bash
cd backend
```

Edit `.env` and change:
```
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
```

### 3. Run Migrations
```bash
alembic upgrade head
```

### 4. Migrate Data
```bash
python scripts/migrate_sqlite_to_postgres.py
```

---

## 📋 Useful Commands

### Docker Management
```bash
# Start services (database only)
docker compose -f docker-compose.db.yml up -d

# Stop services
docker compose -f docker-compose.db.yml down

# View logs
docker compose -f docker-compose.db.yml logs -f postgres

# Restart services
docker compose -f docker-compose.db.yml restart
```

### Database Backup & Restore
```bash
# Backup database
docker exec -t agrisense-postgres pg_dump -U agrisense_user agrisense > backup.sql

# Restore database
cat backup.sql | docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense
```

### Alembic Migrations
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# View current version
alembic current
```

### Database Connection Test
```bash
# Test PostgreSQL connection
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense

# Inside psql:
\dt              # List tables
\d users         # Describe users table
SELECT COUNT(*) FROM users;  # Count users
\q               # Quit
```

---

## 🐛 Troubleshooting

### Issue: "relation does not exist"
**Solution:** Run migrations first
```bash
cd backend
alembic upgrade head
```

### Issue: "No module named 'psycopg2'"
**Solution:** Install PostgreSQL driver
```bash
pip install psycopg2-binary
```

### Issue: Can't connect to PostgreSQL
**Solution:** Check if Docker is running
```bash
docker compose -f docker-compose.db.yml ps
```

### Issue: Port 5432 already in use
**Solution:** Stop other PostgreSQL instances
```bash
# Windows
net stop postgresql-x64-14

# Mac
brew services stop postgresql

# Linux
sudo systemctl stop postgresql
```

### Issue: Adminer shows "Unable to connect"
**Solution:** Make sure you're using "postgres" as the server name (not "localhost")

---

## 🔄 Switching Back to SQLite

If you need to switch back to SQLite:

1. Edit `backend/.env`:
   ```
   DATABASE_URL=sqlite:///./agrisense.db
   ```

2. Restart your backend server

Your SQLite file (`agrisense.db`) is still there with all your original data!

---

## 📊 Database Schema

After migration, you'll have these tables:

- **users** - User accounts (5 records)
- **sensor_readings** - Environmental data (506 records)
- **pest_detections** - ML detection results (9 records)
- **alerts** - System alerts (12 records)

**Total:** 532 records migrated from SQLite to PostgreSQL

---

## 🎯 Next Steps

1. ✅ Run the setup script
2. ✅ Open Adminer and explore your data
3. ✅ Update your backend to use PostgreSQL
4. ✅ Test your API endpoints
5. ✅ Celebrate! 🎉

---

**Need help?** Check the error messages in the script output or Docker logs.
