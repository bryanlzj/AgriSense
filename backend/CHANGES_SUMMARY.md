# 📝 AgriSense Backend - PostgreSQL Direct Setup Changes

## 🎯 Executive Summary

The AgriSense backend has been **completely transitioned to PostgreSQL** as the primary database. SQLite is no longer used, and all database tables are created directly from SQLAlchemy models using the ORM.

---

## ✅ What Was Done

### **1. Fixed Model Issues**

#### **Alert Model - Fixed Reserved Keyword Conflict**
- **Issue:** `metadata` is a reserved name in SQLAlchemy
- **Fix:** Renamed column to `alert_metadata`
- **File:** `backend/models/alert.py`
- **Impact:** API responses now work correctly

---

### **2. Created New Setup Scripts**

#### **Main Setup Script: `init_postgres.py`**
**Purpose:** Initialize PostgreSQL database directly from SQLAlchemy models

**What it does:**
1. ✅ Connects to PostgreSQL
2. ✅ Creates all tables using `Base.metadata.create_all()`
3. ✅ Seeds test data (3 users, 7 days of sensor readings, pest detections, alerts)
4. ✅ Verifies setup

**Usage:**
```bash
python scripts/init_postgres.py
```

---

#### **Automated Setup Scripts**

**Linux/Mac: `setup_postgres_direct.sh`**
```bash
bash scripts/setup_postgres_direct.sh
```

**Windows: `setup_postgres_direct.bat`**
```bash
scripts\setup_postgres_direct.bat
```

**What they do:**
1. ✅ Check prerequisites (Docker, Docker Compose)
2. ✅ Start PostgreSQL + Adminer containers
3. ✅ Configure .env file for PostgreSQL
4. ✅ Install Python dependencies
5. ✅ Run `init_postgres.py`
6. ✅ Display access credentials

---

### **3. Updated Configuration**

#### **.env.example**
**Before:**
```env
# SQLite by default
DATABASE_URL=sqlite:///./agrisense.db
```

**After:**
```env
# PostgreSQL by default
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
POSTGRES_USER=agrisense_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=agrisense
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

### **4. Enhanced seed_data.py**

**Added:**
```python
# Ensures tables exist before seeding
Base.metadata.create_all(bind=engine)
```

**Benefit:** Works with both SQLite and PostgreSQL, creates tables if missing.

---

### **5. Created Comprehensive Documentation**

#### **New Documentation Files:**

1. **`POSTGRESQL_DIRECT_SETUP.md`** (396 lines)
   - Complete setup guide
   - Prerequisites and configuration
   - Troubleshooting
   - Security notes

2. **`scripts/SCRIPTS_README.md`** (374 lines)
   - Detailed script documentation
   - Common tasks
   - Script categories
   - Usage examples

3. **`MIGRATION_TO_POSTGRESQL_DIRECT.md`** (385 lines)
   - Summary of changes
   - Benefits
   - Migration path
   - Key concepts

4. **`CHANGES_SUMMARY.md`** (This file)
   - Quick reference
   - What changed
   - How to use

---

## 🗂️ File Structure

### **New Files:**
```
backend/
├── scripts/
│   ├── init_postgres.py                 ⭐ NEW - Main setup script
│   ├── setup_postgres_direct.sh         ⭐ NEW - Linux/Mac automated setup
│   ├── setup_postgres_direct.bat        ⭐ NEW - Windows automated setup
│   └── SCRIPTS_README.md                ⭐ NEW - Script documentation
├── POSTGRESQL_DIRECT_SETUP.md           ⭐ NEW - Setup guide
├── MIGRATION_TO_POSTGRESQL_DIRECT.md    ⭐ NEW - Migration guide
└── CHANGES_SUMMARY.md                   ⭐ NEW - This file
```

### **Modified Files:**
```
backend/
├── models/
│   └── alert.py                         ✏️ FIXED - Renamed metadata column
├── scripts/
│   └── seed_data.py                     ✏️ ENHANCED - Added table creation
└── .env.example                         ✏️ UPDATED - PostgreSQL by default
```

### **Legacy Files (Not Needed for New Setups):**
```
backend/scripts/
├── migrate_sqlite_to_postgres.py        ⚠️ LEGACY - SQLite migration
├── quick_postgres_setup.sh              ⚠️ LEGACY - Old setup with migration
├── setup_postgres.bat                   ⚠️ LEGACY - Old Windows setup
├── setup_postgres.ps1                   ⚠️ LEGACY - Old PowerShell setup
└── START_HERE.bat                       ⚠️ LEGACY - Old quick start
```

**Note:** Legacy scripts are kept for reference but not needed for new setups.

---

## 🚀 How to Use (Quick Reference)

### **For New Setup:**

**Windows:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup
cd backend
scripts\setup_postgres_direct.bat
```

**Linux/Mac:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup
cd backend
bash scripts/setup_postgres_direct.sh
```

---

### **Manual Setup:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Configure environment
cd backend
cp .env.example .env

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python scripts/init_postgres.py
```

---

### **Reset Database:**
```bash
# Windows
scripts\reset_postgres.bat
python scripts/init_postgres.py

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python scripts/init_postgres.py
```

---

### **Add More Test Data:**
```bash
python scripts/seed_data.py
```

---

## 📊 Database Schema

### **Tables Created from Models:**

1. **users** (from `models/user.py`)
   - User accounts and authentication
   - Fields: id, username, hashed_password, is_active, created_at, updated_at

2. **sensor_readings** (from `models/sensor_reading.py`)
   - Environmental sensor data
   - Fields: id, user_id, temperature, humidity, soil_moisture, light_intensity, timestamp

3. **pest_detections** (from `models/pest_detection.py`)
   - ML-based pest detection results
   - Fields: id, user_id, image_url, pest_type, confidence_score, severity_level, recommendations, detected_at

4. **alerts** (from `models/alert.py`)
   - Weather warnings and pest risk notifications
   - Fields: id, user_id, alert_type, severity, title, message, recommendations, is_read, alert_metadata, created_at

---

## 🔧 PostgreSQL Compliance

### **All Models Are PostgreSQL-Compliant:**

✅ **Column Types:**
- String → VARCHAR
- Integer → INTEGER
- Float → DOUBLE PRECISION
- Boolean → BOOLEAN
- DateTime(timezone=True) → TIMESTAMP WITH TIME ZONE
- Text → TEXT
- JSON → JSONB
- Enum → PostgreSQL ENUM

✅ **Constraints:**
- Primary keys
- Foreign keys with CASCADE
- Unique constraints
- NOT NULL constraints
- Default values

✅ **Indexes:**
- Single-column indexes
- Composite indexes
- Unique indexes

✅ **Relationships:**
- One-to-many
- Cascade deletes
- Back-populates

---

## 🎯 Benefits

### **1. Simpler Setup**
- ❌ No SQLite database needed
- ❌ No migration step
- ✅ One-step setup process

### **2. PostgreSQL-First**
- ✅ Production-ready from day one
- ✅ Consistent dev/prod environments
- ✅ No database switching

### **3. Model-Driven**
- ✅ Tables created from SQLAlchemy models
- ✅ Single source of truth
- ✅ Easier to maintain

### **4. Better Documentation**
- ✅ Clear setup instructions
- ✅ Comprehensive script docs
- ✅ Troubleshooting guides

---

## 🔐 Default Credentials

### **PostgreSQL:**
- Host: `localhost`
- Port: `5432`
- Database: `agrisense`
- Username: `agrisense_user`
- Password: `changeme`

### **Adminer (Database UI):**
- URL: http://localhost:8080
- System: `PostgreSQL`
- Server: `postgres`
- Username: `agrisense_user`
- Password: `changeme`
- Database: `agrisense`

### **Test Users:**
- Admin: `admin` / `admin123`
- Farmer 1: `farmer1` / `password123`
- Farmer 2: `farmer2` / `password123`

---

## 📚 Documentation Reference

| Document | Purpose |
|----------|---------|
| **POSTGRESQL_DIRECT_SETUP.md** | Complete setup guide with troubleshooting |
| **scripts/SCRIPTS_README.md** | Detailed script documentation |
| **MIGRATION_TO_POSTGRESQL_DIRECT.md** | Migration guide and key concepts |
| **CHANGES_SUMMARY.md** | This file - quick reference |

---

## 🛠️ Troubleshooting

### **"Cannot connect to PostgreSQL"**
```bash
docker ps                              # Check if running
docker-compose up -d postgres          # Start PostgreSQL
docker logs agrisense-postgres         # Check logs
```

### **"Tables already exist"**
```bash
# Reset database
scripts\reset_postgres.bat             # Windows
# OR
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"  # Linux/Mac

# Re-initialize
python scripts/init_postgres.py
```

### **"Module not found"**
```bash
pip install -r requirements.txt
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] PostgreSQL container is running (`docker ps`)
- [ ] Adminer is accessible (http://localhost:8080)
- [ ] Can login to Adminer with credentials
- [ ] 4 tables exist (users, sensor_readings, pest_detections, alerts)
- [ ] Tables have data (3 users, sensor readings, etc.)
- [ ] Backend starts successfully (`python run.py`)
- [ ] API docs accessible (http://localhost:5000/docs)
- [ ] Can login with test credentials

---

## 🚀 Next Steps

1. **Verify Setup:**
   - Check PostgreSQL is running
   - Access Adminer
   - View tables and data

2. **Start Backend:**
   ```bash
   python run.py
   ```

3. **Test API:**
   - http://localhost:5000/docs
   - Try `/auth/login` with test credentials

4. **Develop:**
   - Add new models in `/backend/models/`
   - Create API routes in `/backend/routers/`
   - Use Alembic for schema changes

---

## 📞 Support

If you encounter issues:

1. Check [POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md)
2. Check [scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md)
3. Review PostgreSQL logs: `docker logs agrisense-postgres`
4. Reset database and try again

---

## 📝 Summary

**What Changed:**
- ✅ PostgreSQL is now the primary database
- ✅ No SQLite needed
- ✅ Tables created directly from models
- ✅ Simplified setup process
- ✅ Comprehensive documentation

**How to Use:**
```bash
# One command setup
bash scripts/setup_postgres_direct.sh
```

**Result:**
- 🐘 PostgreSQL database ready
- 📊 4 tables created
- 👥 3 test users
- 📈 7 days of sensor data
- 🐛 Sample pest detections
- 🔔 Sample alerts

---

**Last Updated:** January 2025

**System:** AgriSense - Agricultural Monitoring System
