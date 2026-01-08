# 🚀 AgriSense Backend - Quick Reference

## ⚡ Quick Start (3 Steps)

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Edit .env (optional)
# Change SEED_DATABASE=True or False

# 3. Start backend
cd backend
python run.py
```

---

## 🎛️ Control Seed Data

### **Edit `.env` file:**

```bash
# Development (with test data)
SEED_DATABASE=True

# Production (empty database)
SEED_DATABASE=False
```

**That's it!** Just change `True` to `False`.

---

## 📊 What Gets Seeded (when True)

- **3 users:** admin, farmer1, farmer2
- **504 sensor readings:** 7 days × 24 hours × 3 users
- **9 pest detections:** Various pest types
- **12 alerts:** Temperature, humidity, pest alerts

**Note:** Only seeds if database is empty.

---

## 🔐 Default Credentials

### **PostgreSQL:**
```
Host:     localhost:5432
Database: agrisense
Username: agrisense_user
Password: changeme
```

### **Adminer (UI):**
```
URL:    http://localhost:8080
System: PostgreSQL
Server: postgres
User:   agrisense_user
Pass:   changeme
```

### **Test Users:**
```
admin    / admin123
farmer1  / password123
farmer2  / password123
```

---

## 🌐 URLs

- **API Docs:** http://localhost:5000/docs
- **Adminer:** http://localhost:8080
- **Health:** http://localhost:5000/health

---

## 🔧 Common Commands

```bash
# Start database
docker-compose up -d postgres adminer

# Stop database
docker-compose down

# View logs
docker-compose logs postgres

# Start backend
cd backend
python run.py

# Reset database (drops all data)
docker-compose down -v
docker-compose up -d postgres adminer
# Then restart backend - tables recreated
```

---

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env` | Main configuration (root level) |
| `backend/.env` | Backend configuration |
| `backend/db_init.py` | Auto database initialization |
| `backend/main.py` | API server with startup hook |
| `backend/config.py` | Settings management |

---

## ✅ What Happens on Startup

1. ✅ Connects to PostgreSQL
2. ✅ Checks existing tables
3. ✅ Creates missing tables
4. ✅ Seeds data if `SEED_DATABASE=True` and DB is empty
5. ✅ Starts API server

**All automatic - no manual scripts needed!**

---

## 🗄️ Database Tables

1. **users** - User accounts
2. **sensor_readings** - Sensor data
3. **pest_detections** - Pest information
4. **alerts** - System alerts

---

## 🆘 Troubleshooting

### **Can't connect to database:**
```bash
docker-compose up -d postgres
docker-compose logs postgres
```

### **Tables not created:**
Check backend logs for errors.

### **Seed data not appearing:**
- Check `SEED_DATABASE=True` in `.env`
- Database might already have data (seeding skipped)

### **Reset everything:**
```bash
docker-compose down -v
docker-compose up -d postgres adminer
cd backend && python run.py
```

---

## 📚 Full Documentation

- **`SETUP_COMPLETE.md`** - Complete setup guide
- **`README.md`** - Main documentation
- **`QUICKSTART.md`** - Quick start guide

---

## 🎯 Key Points

✅ **PostgreSQL only** (no SQLite)  
✅ **Automatic initialization** on startup  
✅ **Easy seed control** with one flag  
✅ **Safe** - never overwrites existing data  
✅ **Simple** - just change True/False  

---

**That's all you need to know!** 🎉
