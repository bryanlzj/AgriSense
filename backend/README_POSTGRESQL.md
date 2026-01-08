# 🐘 AgriSense PostgreSQL Setup - Complete Guide

## 📚 Documentation Index

Welcome to the AgriSense PostgreSQL setup documentation. This system uses **PostgreSQL as the primary database** with tables created directly from SQLAlchemy models.

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup
cd backend
bash scripts/setup_postgres_direct.sh    # Linux/Mac
# OR
scripts\setup_postgres_direct.bat        # Windows

# 3. Start backend
python run.py

# 4. Access
# - API Docs: http://localhost:5000/docs
# - Adminer:  http://localhost:8080
```

**That's it!** No SQLite, no migration, just PostgreSQL.

---

## 📖 Documentation Files

### **🎯 Start Here**

1. **[CHANGES_SUMMARY.md](CHANGES_SUMMARY.md)** ⭐ **READ THIS FIRST**
   - Quick overview of what changed
   - How to use the new setup
   - Verification checklist
   - **Best for:** Quick reference

2. **[POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md)** ⭐ **COMPLETE GUIDE**
   - Detailed setup instructions
   - Prerequisites and configuration
   - Troubleshooting
   - Security notes
   - **Best for:** First-time setup

3. **[SETUP_FLOW.md](SETUP_FLOW.md)** ⭐ **VISUAL GUIDE**
   - Visual diagrams of setup flow
   - Data flow from models to database
   - Old vs new comparison
   - **Best for:** Understanding the process

---

### **🔧 Technical Documentation**

4. **[scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md)**
   - Detailed script documentation
   - Common tasks and usage
   - Script categories
   - **Best for:** Script reference

5. **[MIGRATION_TO_POSTGRESQL_DIRECT.md](MIGRATION_TO_POSTGRESQL_DIRECT.md)**
   - Summary of changes
   - Benefits and key concepts
   - Migration path from SQLite
   - **Best for:** Understanding the transition

---

## 🎯 Choose Your Path

### **Path 1: I'm New to This Project**

1. Read [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) (5 min)
2. Follow [POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md) (10 min)
3. Run setup script (2 min)
4. Start developing! 🚀

**Total Time:** ~20 minutes

---

### **Path 2: I Want to Understand the System**

1. Read [SETUP_FLOW.md](SETUP_FLOW.md) - Visual overview
2. Read [MIGRATION_TO_POSTGRESQL_DIRECT.md](MIGRATION_TO_POSTGRESQL_DIRECT.md) - Why and how
3. Review [scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md) - Available tools
4. Explore models in `/backend/models/`

**Total Time:** ~30 minutes

---

### **Path 3: I Just Want It Working**

```bash
# Run this:
bash scripts/setup_postgres_direct.sh
```

**Total Time:** ~2 minutes

---

## 📊 What You Get

After setup, you'll have:

### **Database:**
- ✅ PostgreSQL running in Docker
- ✅ 4 tables created from SQLAlchemy models
- ✅ Test data populated

### **Tables:**
1. **users** - 3 test users (admin, farmer1, farmer2)
2. **sensor_readings** - 504 readings (7 days × 24 hours × 3 users)
3. **pest_detections** - 9 detections (3 per user)
4. **alerts** - 12 alerts (4 per user)

### **Access Points:**
- **Backend API:** http://localhost:5000
- **API Docs:** http://localhost:5000/docs
- **Adminer (DB UI):** http://localhost:8080

### **Test Credentials:**
- Admin: `admin` / `admin123`
- Farmer 1: `farmer1` / `password123`
- Farmer 2: `farmer2` / `password123`

---

## 🗂️ Project Structure

```
backend/
├── models/                          # SQLAlchemy models (define schema)
│   ├── user.py                      # User model → users table
│   ├── sensor_reading.py            # SensorReading → sensor_readings
│   ├── pest_detection.py            # PestDetection → pest_detections
│   └── alert.py                     # Alert → alerts
│
├── scripts/                         # Database management scripts
│   ├── init_postgres.py             # ⭐ Main setup script
│   ├── setup_postgres_direct.sh     # ⭐ Automated setup (Linux/Mac)
│   ├── setup_postgres_direct.bat    # ⭐ Automated setup (Windows)
│   ├── seed_data.py                 # Add more test data
│   ├── backup.sh                    # Backup database
│   ├── restore.sh                   # Restore from backup
│   ├── rollback.sh                  # Rollback migrations
│   └── SCRIPTS_README.md            # Script documentation
│
├── docs/                            # Documentation
│   ├── CHANGES_SUMMARY.md           # ⭐ Quick reference
│   ├── POSTGRESQL_DIRECT_SETUP.md   # ⭐ Complete setup guide
│   ├── SETUP_FLOW.md                # ⭐ Visual diagrams
│   ├── MIGRATION_TO_POSTGRESQL...   # Migration guide
│   └── README_POSTGRESQL.md         # This file
│
├── .env.example                     # Environment variables template
├── database.py                      # Database configuration
├── alembic.ini                      # Alembic configuration
└── requirements.txt                 # Python dependencies
```

---

## 🔄 How It Works

### **1. Models Define Schema**

SQLAlchemy models in `/backend/models/` define the database structure:

```python
# models/user.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    hashed_password = Column(String(255))
    # ... more fields
```

### **2. Tables Created from Models**

The `init_postgres.py` script creates tables:

```python
Base.metadata.create_all(bind=engine)
```

This reads all models and creates PostgreSQL tables with:
- ✅ Correct column types
- ✅ Foreign key constraints
- ✅ Indexes
- ✅ Default values
- ✅ Enums

### **3. Test Data Seeded**

The script then populates tables with test data:

```python
user = User(username="admin", hashed_password="...")
db.add(user)
db.commit()
```

---

## 🎯 Common Tasks

### **First-Time Setup**
```bash
bash scripts/setup_postgres_direct.sh
```

### **Reset Database**
```bash
scripts\reset_postgres.bat              # Windows
python scripts/init_postgres.py

# OR

docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"  # Linux/Mac
python scripts/init_postgres.py
```

### **Add More Test Data**
```bash
python scripts/seed_data.py
```

### **Backup Database**
```bash
bash scripts/backup.sh
```

### **Restore Database**
```bash
bash scripts/restore.sh backups/agrisense_backup_YYYYMMDD_HHMMSS.sql.gz
```

### **View Database**
- Open http://localhost:8080 (Adminer)
- Login with credentials (see below)

---

## 🔐 Credentials

### **PostgreSQL:**
```
Host:     localhost
Port:     5432
Database: agrisense
Username: agrisense_user
Password: changeme
```

### **Adminer:**
```
URL:      http://localhost:8080
System:   PostgreSQL
Server:   postgres
Username: agrisense_user
Password: changeme
Database: agrisense
```

### **Test Users:**
```
Admin:    admin / admin123
Farmer 1: farmer1 / password123
Farmer 2: farmer2 / password123
```

---

## 🛠️ Troubleshooting

### **"Cannot connect to PostgreSQL"**

**Check if running:**
```bash
docker ps
```

**Start PostgreSQL:**
```bash
docker-compose up -d postgres adminer
```

**Check logs:**
```bash
docker logs agrisense-postgres
```

---

### **"Tables already exist"**

This is normal! To reset:

```bash
# Windows
scripts\reset_postgres.bat

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

Then re-run:
```bash
python scripts/init_postgres.py
```

---

### **"Module not found"**

Install dependencies:
```bash
pip install -r requirements.txt
```

---

### **"Permission denied" (Linux/Mac)**

Make scripts executable:
```bash
chmod +x scripts/*.sh
```

---

## 📚 Learn More

### **SQLAlchemy ORM:**
- Models in `/backend/models/` show how to define tables
- Each model class becomes a database table
- Relationships define connections between tables

### **Database Migrations:**
- For schema changes, use Alembic migrations
- Run `alembic revision --autogenerate -m "description"`
- Apply with `alembic upgrade head`

### **API Development:**
- Routes in `/backend/routers/`
- Use `Depends(get_db)` to get database session
- Query models: `db.query(User).filter(...).all()`

---

## 🎓 Key Concepts

### **PostgreSQL-First Approach**
- ✅ No SQLite needed
- ✅ Production-ready from start
- ✅ Consistent dev/prod environments

### **Model-Driven Schema**
- ✅ Models define database structure
- ✅ Single source of truth
- ✅ Type-safe with Python

### **ORM Benefits**
- ✅ Write Python, not SQL
- ✅ Automatic query generation
- ✅ Type checking and validation

---

## 🚀 Next Steps

1. **Complete Setup:**
   - Follow [POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md)

2. **Verify Setup:**
   - Check PostgreSQL is running
   - Access Adminer
   - View tables and data

3. **Start Backend:**
   ```bash
   python run.py
   ```

4. **Test API:**
   - http://localhost:5000/docs
   - Try `/auth/login` endpoint

5. **Develop:**
   - Add new models
   - Create API routes
   - Build features

---

## 📞 Support

**Documentation:**
- [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) - Quick reference
- [POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md) - Complete guide
- [scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md) - Script docs

**Troubleshooting:**
1. Check PostgreSQL logs: `docker logs agrisense-postgres`
2. Verify .env configuration
3. Reset database and try again

---

## ✅ Verification Checklist

After setup, verify:

- [ ] PostgreSQL container running (`docker ps`)
- [ ] Adminer accessible (http://localhost:8080)
- [ ] Can login to Adminer
- [ ] 4 tables exist (users, sensor_readings, pest_detections, alerts)
- [ ] Tables have data
- [ ] Backend starts (`python run.py`)
- [ ] API docs accessible (http://localhost:5000/docs)
- [ ] Can login with test credentials

---

## 📝 Summary

**Setup Process:**
1. Start PostgreSQL → 2. Run setup script → 3. Done!

**Result:**
- 🐘 PostgreSQL database ready
- 📊 4 tables with test data
- 🚀 Ready for development

**Time:** ~2-3 minutes

---

## 🔗 Quick Links

| Link | Description |
|------|-------------|
| [CHANGES_SUMMARY.md](CHANGES_SUMMARY.md) | Quick reference guide |
| [POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md) | Complete setup guide |
| [SETUP_FLOW.md](SETUP_FLOW.md) | Visual diagrams |
| [scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md) | Script documentation |
| [MIGRATION_TO_POSTGRESQL_DIRECT.md](MIGRATION_TO_POSTGRESQL_DIRECT.md) | Migration guide |
| http://localhost:8080 | Adminer (Database UI) |
| http://localhost:5000/docs | API Documentation |

---

**Last Updated:** January 2025

**System:** AgriSense - Agricultural Monitoring System

**Database:** PostgreSQL (Primary)

**Setup Method:** Direct from SQLAlchemy Models
