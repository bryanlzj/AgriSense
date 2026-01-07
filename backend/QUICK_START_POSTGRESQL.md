# 🚀 Quick Start: Switch to PostgreSQL + Adminer

**Time Required:** 5 minutes  
**Difficulty:** Easy (automated script)

---

## Option 1: Automated Setup (Recommended)

Run this single command from the **backend directory**:

```bash
cd backend
bash scripts/quick_postgres_setup.sh
```

**What it does:**
1. ✅ Starts PostgreSQL and Adminer with Docker
2. ✅ Creates/updates .env file with PostgreSQL URL
3. ✅ Runs database migrations
4. ✅ Migrates all your data from SQLite to PostgreSQL
5. ✅ Verifies everything works

**Expected output:**
```
================================================================================
🚀 AgriSense: Quick PostgreSQL Setup
================================================================================

📋 Checking prerequisites...
✅ Docker is installed
✅ Docker Compose is installed
✅ In backend directory
✅ SQLite database exists

🐘 Starting PostgreSQL and Adminer...
⏳ Waiting for PostgreSQL to be ready...
✅ PostgreSQL is ready

📝 Creating .env file...
✅ .env file created and updated

🔄 Running database migrations...
✅ Migrations complete

📦 Migrating data from SQLite to PostgreSQL...
✅ Migrated 3 users
✅ Migrated 504 sensor readings
✅ Migrated 9 pest detections
✅ Migrated 12 alerts

🎉 PostgreSQL Setup Complete!
================================================================================

📊 Your database is ready:
   - PostgreSQL running on: localhost:5432
   - Adminer running on: http://localhost:8080

🔐 Adminer login credentials:
   System: PostgreSQL
   Server: postgres
   Username: agrisense_user
   Password: changeme
   Database: agrisense
```

---

## Option 2: Manual Setup

If you prefer to do it step-by-step:

### Step 1: Start PostgreSQL and Adminer
```bash
docker-compose up -d postgres adminer
```

### Step 2: Update .env file
```bash
# Edit backend/.env
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
```

### Step 3: Run migrations
```bash
cd backend
alembic upgrade head
```

### Step 4: Migrate data
```bash
python scripts/migrate_sqlite_to_postgres.py
```

---

## 🌐 Access Adminer (Database Manager)

1. **Open browser:** http://localhost:8080

2. **Login with:**
   - System: **PostgreSQL**
   - Server: **postgres**
   - Username: **agrisense_user**
   - Password: **changeme**
   - Database: **agrisense**

3. **Click "Login"**

### What you can do in Adminer:

- 📊 **Browse all tables** (users, sensor_readings, pest_detections, alerts)
- ✏️ **Edit records** directly in the UI
- ➕ **Add new records** with a form
- 🗑️ **Delete records** with one click
- 🔍 **Run SQL queries** with syntax highlighting
- 📥 **Export data** to SQL, CSV, or JSON
- 📤 **Import data** from files
- 📈 **View table structure** and relationships

---

## 🧪 Test Your Setup

### 1. Test Backend Connection
```bash
cd backend
python run.py
```

Open: http://localhost:5000/health

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "database_type": "postgresql"
}
```

### 2. Test API Endpoints
Open: http://localhost:5000/docs

Try these:
- POST /api/v1/auth/login (username: admin, password: admin123)
- GET /api/v1/sensor/ (requires auth token)
- GET /api/v1/pest/ (requires auth token)

### 3. Check Data in Adminer
1. Go to http://localhost:8080
2. Login with credentials above
3. Click "users" table → You should see 3 users
4. Click "sensor_readings" → You should see 504 readings
5. Click "pest_detections" → You should see 9 detections
6. Click "alerts" → You should see 12 alerts

---

## 🔄 Useful Commands

### View PostgreSQL logs
```bash
docker-compose logs -f postgres
```

### Stop PostgreSQL and Adminer
```bash
docker-compose down
```

### Restart PostgreSQL
```bash
docker-compose restart postgres
```

### Connect to PostgreSQL CLI
```bash
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense
```

### Backup PostgreSQL database
```bash
docker exec -t agrisense-postgres pg_dump -U agrisense_user agrisense > backup.sql
```

### Restore PostgreSQL database
```bash
cat backup.sql | docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense
```

---

## 🐛 Troubleshooting

### "Connection refused"
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# If not running, start it
docker-compose up -d postgres

# Wait 10 seconds for it to be ready
sleep 10
```

### "Password authentication failed"
Make sure your .env file has:
```bash
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
```

### "Database does not exist"
```bash
# Create database manually
docker exec -it agrisense-postgres psql -U agrisense_user -c "CREATE DATABASE agrisense;"
```

### "Adminer shows empty database"
```bash
# Make sure you ran migrations and data migration
cd backend
alembic upgrade head
python scripts/migrate_sqlite_to_postgres.py
```

---

## 🔙 Switch Back to SQLite

If you want to go back to SQLite:

1. Edit `backend/.env`:
   ```bash
   DATABASE_URL=sqlite:///./agrisense.db
   ```

2. Restart backend:
   ```bash
   python run.py
   ```

That's it! No need to stop PostgreSQL.

---

## 📚 Full Documentation

For detailed explanations, see: **POSTGRESQL_SETUP.md**

---

## ✅ Checklist

After setup, verify:

- [ ] PostgreSQL running: `docker-compose ps postgres`
- [ ] Adminer accessible: http://localhost:8080
- [ ] Can login to Adminer with credentials
- [ ] See all 4 tables in Adminer (users, sensor_readings, pest_detections, alerts)
- [ ] Backend connects: http://localhost:5000/health shows "postgresql"
- [ ] API works: http://localhost:5000/docs
- [ ] Can login with admin/admin123

---

**Setup Time:** ~5 minutes  
**Status:** Ready to use! 🎉
