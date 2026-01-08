# 🔄 Migration to PostgreSQL Direct Setup

## 📋 Summary of Changes

The AgriSense backend has been updated to use **PostgreSQL as the primary database** from the start, eliminating the need for SQLite and migration scripts.

---

## ✅ What Changed

### **1. Database Configuration**

**Before:**
```env
# SQLite by default
DATABASE_URL=sqlite:///./agrisense.db

# PostgreSQL commented out
# DATABASE_URL=postgresql://...
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

### **2. New Setup Scripts**

#### **Created:**
- ✅ `scripts/init_postgres.py` - Initialize PostgreSQL directly from models
- ✅ `scripts/setup_postgres_direct.sh` - Automated setup (Linux/Mac)
- ✅ `scripts/setup_postgres_direct.bat` - Automated setup (Windows)
- ✅ `scripts/SCRIPTS_README.md` - Comprehensive script documentation
- ✅ `POSTGRESQL_DIRECT_SETUP.md` - Setup guide

#### **Legacy (Not Needed for New Setups):**
- ❌ `scripts/migrate_sqlite_to_postgres.py` - SQLite to PostgreSQL migration
- ❌ `scripts/quick_postgres_setup.sh` - Old setup with migration
- ❌ `scripts/setup_postgres.bat` - Old Windows setup with migration
- ❌ `scripts/setup_postgres.ps1` - Old PowerShell setup with migration
- ❌ `scripts/START_HERE.bat` - Old Windows quick start with migration

**Note:** Legacy scripts are kept for reference but not needed for new setups.

---

### **3. Model Updates**

#### **Fixed: Alert Model**
```python
# Before (caused error - 'metadata' is reserved)
metadata = Column(Text, nullable=True)

# After (renamed to avoid conflict)
alert_metadata = Column(Text, nullable=True)
```

**Impact:** The `to_dict()` method now correctly returns `alert_metadata` as `metadata` in API responses.

---

### **4. Updated seed_data.py**

**Enhancement:**
```python
# Now ensures tables exist before seeding
Base.metadata.create_all(bind=engine)
```

**Benefit:** Works with both SQLite and PostgreSQL, creates tables if they don't exist.

---

## 🎯 Benefits

### **1. Simpler Setup**
- ✅ No SQLite database to create first
- ✅ No migration step needed
- ✅ One-step setup process

### **2. PostgreSQL-First**
- ✅ Production-ready from day one
- ✅ No database switching needed
- ✅ Consistent development and production environments

### **3. Model-Driven**
- ✅ Tables created directly from SQLAlchemy models
- ✅ Single source of truth (models)
- ✅ Easier to understand and maintain

### **4. Better Documentation**
- ✅ Clear setup instructions
- ✅ Comprehensive script documentation
- ✅ Troubleshooting guides

---

## 🚀 How to Use

### **For New Developers:**

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

**That's it!** No SQLite, no migration, just PostgreSQL.

---

### **For Existing Developers:**

If you have an existing SQLite database and want to switch to PostgreSQL:

**Option 1: Fresh Start (Recommended)**
```bash
# 1. Backup your SQLite data if needed
cp agrisense.db agrisense.db.backup

# 2. Run new setup
bash scripts/setup_postgres_direct.sh
```

**Option 2: Migrate Existing Data**
```bash
# Use legacy migration script
python scripts/migrate_sqlite_to_postgres.py
```

---

## 📊 Database Schema

All tables are created from SQLAlchemy models:

### **Models Location:** `/backend/models/`

1. **user.py** → `users` table
2. **sensor_reading.py** → `sensor_readings` table
3. **pest_detection.py** → `pest_detections` table
4. **alert.py** → `alerts` table

### **Schema Creation:**
```python
# In init_postgres.py
Base.metadata.create_all(bind=engine)
```

This reads all models and creates corresponding PostgreSQL tables with:
- ✅ Correct column types
- ✅ Foreign key constraints
- ✅ Indexes
- ✅ Default values
- ✅ Enums (for alert types, severity levels, etc.)

---

## 🔧 PostgreSQL Compliance

All models are PostgreSQL-compliant:

### **1. Column Types**
- ✅ `String(length)` - VARCHAR
- ✅ `Integer` - INTEGER
- ✅ `Float` - DOUBLE PRECISION
- ✅ `Boolean` - BOOLEAN
- ✅ `DateTime(timezone=True)` - TIMESTAMP WITH TIME ZONE
- ✅ `Text` - TEXT
- ✅ `JSON` - JSONB (PostgreSQL native)
- ✅ `Enum` - PostgreSQL ENUM type

### **2. Constraints**
- ✅ Primary keys
- ✅ Foreign keys with CASCADE
- ✅ Unique constraints
- ✅ NOT NULL constraints
- ✅ Default values

### **3. Indexes**
- ✅ Single-column indexes
- ✅ Composite indexes
- ✅ Unique indexes

### **4. Relationships**
- ✅ One-to-many (User → SensorReadings)
- ✅ Cascade deletes
- ✅ Back-populates for bidirectional access

---

## 🛠️ Troubleshooting

### **"Cannot connect to PostgreSQL"**
```bash
# Check if running
docker ps

# Start PostgreSQL
docker-compose up -d postgres

# Check logs
docker logs agrisense-postgres
```

---

### **"Tables already exist"**
This is normal! The scripts handle existing tables.

To reset:
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
```bash
pip install -r requirements.txt
```

---

## 📚 Documentation

- **[POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md)** - Complete setup guide
- **[scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md)** - Script documentation
- **[models/](models/)** - SQLAlchemy model definitions

---

## 🔄 Migration Path

### **From SQLite to PostgreSQL (Existing Projects):**

1. **Backup SQLite data:**
   ```bash
   cp agrisense.db agrisense.db.backup
   ```

2. **Start PostgreSQL:**
   ```bash
   docker-compose up -d postgres adminer
   ```

3. **Migrate data (if needed):**
   ```bash
   python scripts/migrate_sqlite_to_postgres.py
   ```

4. **Update .env:**
   ```env
   DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
   ```

5. **Restart backend:**
   ```bash
   python run.py
   ```

---

### **New Projects:**

Just use the new setup scripts - no SQLite needed!

```bash
bash scripts/setup_postgres_direct.sh
```

---

## 🎓 Key Concepts

### **1. ORM (Object-Relational Mapping)**
SQLAlchemy models define database schema:
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
```

This creates a PostgreSQL table:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE
);
```

---

### **2. No Migrations (Initially)**
For initial setup, we create tables directly from models:
```python
Base.metadata.create_all(bind=engine)
```

For schema changes later, use Alembic migrations.

---

### **3. Seed Data**
Test data is created programmatically:
```python
user = User(username="admin", hashed_password="...")
db.add(user)
db.commit()
```

---

## 🚀 Next Steps

1. **Run Setup:**
   ```bash
   bash scripts/setup_postgres_direct.sh
   ```

2. **Start Backend:**
   ```bash
   python run.py
   ```

3. **Test API:**
   - http://localhost:5000/docs

4. **View Database:**
   - http://localhost:8080 (Adminer)

5. **Develop:**
   - Add new models in `/backend/models/`
   - Create API routes in `/backend/routers/`
   - Use Alembic for schema changes

---

## 📞 Support

Questions or issues?

1. Check [POSTGRESQL_DIRECT_SETUP.md](POSTGRESQL_DIRECT_SETUP.md)
2. Check [scripts/SCRIPTS_README.md](scripts/SCRIPTS_README.md)
3. Review PostgreSQL logs: `docker logs agrisense-postgres`
4. Reset and try again

---

**Last Updated:** January 2025

**Changes By:** System Migration to PostgreSQL Direct Setup
