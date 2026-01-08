# 🐘 PostgreSQL Direct Setup Guide

This guide explains how to set up AgriSense with PostgreSQL **without** SQLite migration.

## 🎯 Overview

The system now uses **PostgreSQL as the primary database** from the start:
- ✅ Tables created directly from SQLAlchemy models
- ✅ No SQLite database needed
- ✅ No migration from SQLite to PostgreSQL
- ✅ Simpler and faster setup

---

## 🚀 Quick Start

### **Option 1: Automated Setup (Recommended)**

#### **Windows:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup script
cd backend
scripts\setup_postgres_direct.bat
```

#### **Linux/Mac:**
```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Run setup script
cd backend
bash scripts/setup_postgres_direct.sh
```

**What this does:**
- ✅ Starts PostgreSQL + Adminer containers
- ✅ Configures .env file for PostgreSQL
- ✅ Installs Python dependencies
- ✅ Creates all database tables from models
- ✅ Seeds test data (users, sensor readings, pest detections, alerts)

---

### **Option 2: Manual Setup**

```bash
# 1. Start PostgreSQL
docker-compose up -d postgres adminer

# 2. Copy and configure .env
cd backend
cp .env.example .env
# Edit .env to ensure DATABASE_URL uses PostgreSQL

# 3. Install dependencies
pip install -r requirements.txt

# 4. Initialize database
python scripts/init_postgres.py
```

---

## 📋 Prerequisites

### **Required:**
- Docker & Docker Compose installed
- Python 3.8+ installed
- Git (for cloning repository)

### **Check Prerequisites:**
```bash
# Check Docker
docker --version

# Check Docker Compose
docker-compose --version

# Check Python
python --version
```

---

## 🗄️ Database Configuration

### **Default PostgreSQL Credentials:**
```env
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
POSTGRES_USER=agrisense_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=agrisense
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

These are configured in `.env.example` and automatically set during setup.

---

## 📊 Database Schema

Tables are created from SQLAlchemy models in `/backend/models/`:

### **1. users**
- User accounts for authentication
- Fields: id, username, hashed_password, is_active, created_at, updated_at

### **2. sensor_readings**
- Environmental sensor data (simulated IoT)
- Fields: id, user_id, temperature, humidity, soil_moisture, light_intensity, timestamp

### **3. pest_detections**
- ML-based pest detection results
- Fields: id, user_id, image_url, pest_type, confidence_score, severity_level, recommendations, detected_at

### **4. alerts**
- Weather warnings and pest risk notifications
- Fields: id, user_id, alert_type, severity, title, message, recommendations, is_read, created_at

---

## 🔧 How It Works

### **1. Models Define Schema**
SQLAlchemy models in `/backend/models/` define the database structure:
```python
# Example: User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    # ... more fields
```

### **2. Tables Created from Models**
The `init_postgres.py` script uses SQLAlchemy to create tables:
```python
Base.metadata.create_all(bind=engine)
```

This reads all models and creates corresponding PostgreSQL tables.

### **3. No Migrations Needed (Initially)**
For initial setup, we create tables directly. For schema changes later, use Alembic migrations.

---

## 🧪 Test Data

The setup automatically creates test data:

### **Test Users:**
| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| farmer1 | password123 | Farmer |
| farmer2 | password123 | Farmer |

### **Sample Data:**
- **Sensor Readings:** 7 days of hourly data (168 readings per user)
- **Pest Detections:** 3 sample detections per user (Fall Armyworm, Aphids, Whitefly)
- **Alerts:** 4 sample alerts per user (weather warnings, pest risks)

---

## 🔍 Verify Setup

### **1. Check PostgreSQL is Running**
```bash
docker ps
```
Should show `agrisense-postgres` and `agrisense-adminer` containers.

### **2. Access Adminer (Database UI)**
Open http://localhost:8080

**Login:**
- System: `PostgreSQL`
- Server: `postgres`
- Username: `agrisense_user`
- Password: `changeme`
- Database: `agrisense`

### **3. Check Tables**
In Adminer, you should see 4 tables:
- users
- sensor_readings
- pest_detections
- alerts

### **4. Test Backend API**
```bash
# Start backend
python run.py

# Open API docs
# http://localhost:5000/docs
```

---

## 🔄 Reset Database

If you need to start fresh:

### **Windows:**
```bash
scripts\reset_postgres.bat
python scripts\init_postgres.py
```

### **Linux/Mac:**
```bash
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
python scripts/init_postgres.py
```

---

## 📦 Add More Test Data

```bash
python scripts/seed_data.py
```

This adds more users and data without clearing existing data.

---

## 🛠️ Troubleshooting

### **"Cannot connect to PostgreSQL"**

**Check if PostgreSQL is running:**
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

This is normal! The scripts handle existing tables gracefully.

To reset:
```bash
# Windows
scripts\reset_postgres.bat

# Linux/Mac
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

Then run:
```bash
python scripts/init_postgres.py
```

---

### **"Module not found" errors**

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

## 🔐 Security Notes

### **Development vs Production:**

**Development (Current Setup):**
- Password: `changeme` (simple, easy to remember)
- Database: Local Docker container
- Debug mode enabled

**Production (Change These!):**
- Use strong passwords (generate with `openssl rand -hex 32`)
- Use managed PostgreSQL service (AWS RDS, Azure Database, etc.)
- Disable debug mode
- Use environment-specific .env files

### **Change Production Credentials:**
```env
# .env.production
DATABASE_URL=postgresql://prod_user:STRONG_PASSWORD@prod-host:5432/agrisense_prod
POSTGRES_USER=prod_user
POSTGRES_PASSWORD=STRONG_PASSWORD
POSTGRES_DB=agrisense_prod
```

---

## 📚 Related Documentation

- [Scripts README](scripts/SCRIPTS_README.md) - Detailed script documentation
- [Database Models](models/) - SQLAlchemy model definitions
- [API Documentation](http://localhost:5000/docs) - FastAPI interactive docs

---

## 🎓 Understanding the Setup

### **Why PostgreSQL?**
- ✅ Production-ready database
- ✅ Better performance than SQLite
- ✅ Supports concurrent connections
- ✅ Advanced features (JSON columns, full-text search, etc.)
- ✅ Industry standard for web applications

### **Why No SQLite?**
- ❌ SQLite is file-based (not ideal for production)
- ❌ Limited concurrent write support
- ❌ No user management
- ❌ Migration from SQLite to PostgreSQL adds complexity

### **Why Direct Model Creation?**
- ✅ Simpler for initial setup
- ✅ No migration history to manage
- ✅ Faster development iteration
- ✅ Still use Alembic for future schema changes

---

## 🚀 Next Steps

After setup is complete:

1. **Start Backend:**
   ```bash
   python run.py
   ```

2. **Test API:**
   - Open http://localhost:5000/docs
   - Try the `/auth/login` endpoint with test credentials
   - Explore other endpoints

3. **View Data:**
   - Open http://localhost:8080 (Adminer)
   - Browse tables and data

4. **Develop:**
   - Models are in `/backend/models/`
   - API routes are in `/backend/routers/`
   - Add new features and endpoints

5. **Deploy:**
   - Use `scripts/deploy.sh` for production deployment
   - Configure production .env file
   - Set up CI/CD pipeline

---

## 📞 Support

If you encounter issues:

1. Check PostgreSQL is running: `docker ps`
2. Check .env configuration
3. Review logs: `docker logs agrisense-postgres`
4. Reset database and try again
5. Check [Scripts README](scripts/SCRIPTS_README.md) for detailed troubleshooting

---

**Last Updated:** January 2025

**System:** AgriSense - Agricultural Monitoring System
