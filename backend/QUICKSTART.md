# 🚀 AgriSense Backend - Quick Start

## 3-Step Setup

### 1️⃣ Start PostgreSQL

```bash
docker-compose up -d postgres adminer
```

### 2️⃣ Configure Environment

```bash
cp .env.example .env
```

**Optional:** Edit `.env` to customize settings:
- Set `SEED_DATABASE=True` for test data (development)
- Set `SEED_DATABASE=False` for empty database (production)

### 3️⃣ Start Backend

```bash
pip install -r requirements.txt
python run.py
```

**Done!** 🎉

---

## ✅ What Happens Automatically

When you start the backend, it automatically:

1. ✅ Connects to PostgreSQL
2. ✅ Checks database schema
3. ✅ Creates missing tables from models
4. ✅ Seeds test data (if `SEED_DATABASE=True`)

**No manual scripts needed!**

---

## 🌐 Access Your API

- **API Docs:** http://localhost:5000/docs
- **Database UI:** http://localhost:8080

---

## 🔐 Test Credentials

### Login to API
```
Username: admin
Password: admin123
```

### Access Database (Adminer)
```
System:   PostgreSQL
Server:   postgres
Username: agrisense_user
Password: changeme
Database: agrisense
```

---

## 🎯 Common Tasks

### View Logs
```bash
# Backend logs (in terminal where you ran python run.py)

# Database logs
docker logs agrisense-postgres
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

### Stop Everything
```bash
# Stop backend: Ctrl+C in terminal

# Stop database
docker-compose down
```

---

## 🆘 Troubleshooting

### "Cannot connect to database"

**Check if PostgreSQL is running:**
```bash
docker ps
```

**Start PostgreSQL:**
```bash
docker-compose up -d postgres
```

### "Port already in use"

**Change port in `.env`:**
```bash
PORT=5001  # Change from 5000 to 5001
```

### "Module not found"

**Install dependencies:**
```bash
pip install -r requirements.txt
```

---

## 📚 Learn More

- **Full Documentation:** [README.md](README.md)
- **API Documentation:** http://localhost:5000/docs
- **Scripts Guide:** [scripts/README.md](scripts/README.md)

---

## 🎓 Key Concepts

### Automatic Database Initialization

The backend automatically manages your database:

- **First run:** Creates all tables and seeds test data
- **Subsequent runs:** Checks for missing tables and adds them
- **Existing data:** Never overwritten or deleted

### Configuration via Environment

Control behavior with `.env` file:

```bash
# Development (with test data)
SEED_DATABASE=True

# Production (empty database)
SEED_DATABASE=False
```

### No Manual Scripts

Unlike traditional setups, you don't need to run:
- ❌ `init_postgres.py`
- ❌ `seed_data.py`
- ❌ `migrate_sqlite_to_postgres.py`

Just run `python run.py` and everything happens automatically! ✨

---

**Questions?** Check the [full README](README.md) or API docs at http://localhost:5000/docs
