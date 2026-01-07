# 🐘 PostgreSQL Setup for AgriSense

## ⚡ Quick Start (3 Steps)

### 1️⃣ Start Database Services

```bash
docker compose -f docker-compose.db.yml up -d
```

### 2️⃣ Run Setup Script

**Windows:**
```powershell
cd backend
powershell -ExecutionPolicy Bypass -File scripts/setup_postgres.ps1
```

**Linux/Mac:**
```bash
cd backend
bash scripts/quick_postgres_setup.sh
```

### 3️⃣ Access Adminer

Open: **http://localhost:8080**

Login:
- System: **PostgreSQL**
- Server: **postgres**
- Username: **agrisense_user**
- Password: **changeme**
- Database: **agrisense**

---

## ✅ What This Does

1. Updates `.env` to use PostgreSQL
2. Creates database tables (via Alembic)
3. Migrates all data from SQLite (5 users, 506 readings, 9 detections, 12 alerts)
4. Keeps SQLite as backup

---

## 📚 Full Documentation

See: `backend/POSTGRESQL_SETUP.md`

---

## 🎯 Current Issue

You tried to run the migration script but got:
```
relation "alerts" does not exist
```

**Why?** The PostgreSQL database doesn't have tables yet.

**Solution:** Run the setup script above. It will:
1. Create the tables first (via Alembic)
2. Then migrate the data

---

**Ready?** Run the setup script now! 🚀
