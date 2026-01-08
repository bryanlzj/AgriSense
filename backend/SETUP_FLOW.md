# 🔄 AgriSense PostgreSQL Setup Flow

## 📊 Visual Setup Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGRISENSE POSTGRESQL SETUP                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: Start PostgreSQL                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  $ docker-compose up -d postgres adminer                        │
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                     │
│  │  PostgreSQL  │         │   Adminer    │                     │
│  │  Port: 5432  │         │  Port: 8080  │                     │
│  └──────────────┘         └──────────────┘                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Run Setup Script                                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Windows:  scripts\setup_postgres_direct.bat                    │
│  Linux:    bash scripts/setup_postgres_direct.sh                │
│                                                                  │
│  This script does:                                              │
│  ✓ Configure .env file                                          │
│  ✓ Install dependencies                                         │
│  ✓ Run init_postgres.py                                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: init_postgres.py Execution                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 1. Connect to PostgreSQL                               │    │
│  │    postgresql://agrisense_user:***@localhost:5432      │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↓                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 2. Create Tables from Models                           │    │
│  │    Base.metadata.create_all(bind=engine)               │    │
│  │                                                         │    │
│  │    models/user.py           → users table              │    │
│  │    models/sensor_reading.py → sensor_readings table    │    │
│  │    models/pest_detection.py → pest_detections table    │    │
│  │    models/alert.py          → alerts table             │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↓                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 3. Seed Test Data                                      │    │
│  │                                                         │    │
│  │    Users:            3 users (admin, farmer1, farmer2) │    │
│  │    Sensor Readings:  168 readings per user (7 days)   │    │
│  │    Pest Detections:  3 detections per user            │    │
│  │    Alerts:           4 alerts per user                 │    │
│  └────────────────────────────────────────────────────────┘    │
│                            ↓                                     │
│  ┌────────────────────────────────────────────────────────┐    │
│  │ 4. Verify Setup                                        │    │
│  │    ✓ Count records in each table                      │    │
│  │    ✓ Display summary                                   │    │
│  └────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────────┐
│ RESULT: Database Ready!                                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PostgreSQL Database: agrisense                                 │
│  ├── users (3 records)                                          │
│  ├── sensor_readings (504 records)                              │
│  ├── pest_detections (9 records)                                │
│  └── alerts (12 records)                                        │
│                                                                  │
│  Access Points:                                                 │
│  • Adminer:  http://localhost:8080                              │
│  • Backend:  http://localhost:5000                              │
│  • API Docs: http://localhost:5000/docs                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow: Models → PostgreSQL

```
┌─────────────────────────────────────────────────────────────────┐
│                    SQLAlchemy Models (Python)                    │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   models/        │  │   models/        │  │   models/        │
│   user.py        │  │   sensor_        │  │   pest_          │
│                  │  │   reading.py     │  │   detection.py   │
│  class User:     │  │                  │  │                  │
│    id            │  │  class Sensor    │  │  class Pest      │
│    username      │  │  Reading:        │  │  Detection:      │
│    password      │  │    temperature   │  │    pest_type     │
│    ...           │  │    humidity      │  │    confidence    │
└──────────────────┘  └──────────────────┘  └──────────────────┘
         │                     │                      │
         │                     │                      │
         └─────────────────────┼──────────────────────┘
                               │
                               ↓
                    ┌──────────────────────┐
                    │  Base.metadata       │
                    │  .create_all()       │
                    └──────────────────────┘
                               │
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                           │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│  users           │  │  sensor_readings │  │  pest_detections │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│  id SERIAL PK    │  │  id SERIAL PK    │  │  id SERIAL PK    │
│  username VARCHAR│  │  user_id INT FK  │  │  user_id INT FK  │
│  hashed_password │  │  temperature     │  │  pest_type       │
│  is_active BOOL  │  │  humidity        │  │  confidence      │
│  created_at      │  │  soil_moisture   │  │  severity_level  │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

---

## 🔀 Old vs New Setup Comparison

### **OLD WAY (SQLite → PostgreSQL Migration)**

```
┌─────────────────────────────────────────────────────────────────┐
│ OLD SETUP FLOW (Not Used Anymore)                               │
└─────────────────────────────────────────────────────────────────┘

Step 1: Create SQLite database
   ↓
Step 2: Seed data into SQLite
   ↓
Step 3: Start PostgreSQL
   ↓
Step 4: Run migration script
   ↓
Step 5: Migrate data from SQLite to PostgreSQL
   ↓
Step 6: Update .env to use PostgreSQL
   ↓
Step 7: Restart backend

❌ Problems:
   • Too many steps
   • Need to maintain SQLite database
   • Migration can fail
   • Data inconsistencies
   • Complex troubleshooting
```

### **NEW WAY (PostgreSQL Direct)**

```
┌─────────────────────────────────────────────────────────────────┐
│ NEW SETUP FLOW (Current)                                        │
└─────────────────────────────────────────────────────────────────┘

Step 1: Start PostgreSQL
   ↓
Step 2: Run setup script
   ↓
Step 3: Done!

✅ Benefits:
   • One-step setup
   • No SQLite needed
   • No migration needed
   • Production-ready from start
   • Simple troubleshooting
```

---

## 📦 Script Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│ setup_postgres_direct.sh / .bat                                 │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │ Check Prerequisites               │
        │ • Docker installed?               │
        │ • Docker Compose installed?       │
        │ • In backend directory?           │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │ Start Containers                  │
        │ $ docker-compose up -d postgres   │
        │   adminer                         │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │ Configure .env                    │
        │ • Copy .env.example → .env        │
        │ • Set DATABASE_URL to PostgreSQL  │
        │ • Set POSTGRES_* variables        │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │ Install Dependencies              │
        │ $ pip install -r requirements.txt │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │ Initialize Database               │
        │ $ python scripts/init_postgres.py │
        └───────────────────────────────────┘
                            │
                            ↓
        ┌───────────────────────────────────┐
        │ Display Success Message           │
        │ • Show credentials                │
        │ • Show access URLs                │
        │ • Show next steps                 │
        └───────────────────────────────────┘
```

---

## 🗄️ Database Schema Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    Database Relationships                        │
└─────────────────────────────────────────────────────────────────┘

                        ┌──────────────┐
                        │    users     │
                        ├──────────────┤
                        │ id (PK)      │
                        │ username     │
                        │ password     │
                        └──────────────┘
                               │
                               │ One-to-Many
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ↓                      ↓                      ↓
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│sensor_       │      │pest_         │      │   alerts     │
│readings      │      │detections    │      │              │
├──────────────┤      ├──────────────┤      ├──────────────┤
│ id (PK)      │      │ id (PK)      │      │ id (PK)      │
│ user_id (FK) │      │ user_id (FK) │      │ user_id (FK) │
│ temperature  │      │ pest_type    │      │ alert_type   │
│ humidity     │      │ confidence   │      │ severity     │
│ ...          │      │ ...          │      │ ...          │
└──────────────┘      └──────────────┘      └──────────────┘

CASCADE DELETE: When user is deleted, all related records are deleted
```

---

## 🎯 Quick Reference

### **Setup Command:**
```bash
# Linux/Mac
bash scripts/setup_postgres_direct.sh

# Windows
scripts\setup_postgres_direct.bat
```

### **Manual Steps:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Initialize database
cd backend
python scripts/init_postgres.py
```

### **Reset Database:**
```bash
# Windows
scripts\reset_postgres.bat

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Then re-initialize
python scripts/init_postgres.py
```

### **Access Points:**
- **Adminer:** http://localhost:8080
- **Backend:** http://localhost:5000
- **API Docs:** http://localhost:5000/docs

---

## 📝 Summary

**What Happens:**
1. PostgreSQL starts in Docker
2. Setup script configures environment
3. `init_postgres.py` creates tables from models
4. Test data is seeded
5. Database is ready to use

**Result:**
- ✅ 4 tables created
- ✅ Test data populated
- ✅ Ready for development

**Time:** ~2-3 minutes for complete setup

---

**Last Updated:** January 2025
