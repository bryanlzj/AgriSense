# 🏗️ AgriSense Application Architecture

## 📋 High-Level Overview

AgriSense is a **FastAPI backend** application with **PostgreSQL database** for agricultural monitoring and early warning system.

---

## 🚀 How Your Application Starts

### **Development Mode (Local)**

```bash
# 1. Start Database (PostgreSQL + Adminer)
docker compose -f docker-compose.db.yml up -d

# 2. Activate Python environment
cd backend
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Start Backend Server
python run.py
# OR
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**What happens:**
1. ✅ Docker starts PostgreSQL (port 5432) and Adminer (port 8080)
2. ✅ Backend reads `.env` file for configuration
3. ✅ FastAPI app initializes (`main.py`)
4. ✅ SQLAlchemy connects to database (`database.py`)
5. ✅ API routes are registered (`routers/`)
6. ✅ Server listens on http://localhost:8000
7. ✅ Swagger docs available at http://localhost:8000/docs

### **Production Mode (Docker)**

```bash
# Start everything (Backend + Database + Adminer)
docker compose up -d
```

**What happens:**
1. ✅ Docker builds backend image from `Dockerfile`
2. ✅ PostgreSQL starts first (healthcheck)
3. ✅ Backend waits for database to be ready
4. ✅ Alembic runs migrations automatically
5. ✅ Backend starts on port 5000
6. ✅ Adminer starts on port 8080

---

## 🗄️ How Your Database Starts

### **Database Stack**

```
┌─────────────────────────────────────────┐
│         PostgreSQL Database             │
│  (Port 5432)                            │
│  - User: agrisense_user                 │
│  - Database: agrisense                  │
│  - Tables: users, sensor_readings,      │
│            pest_detections, alerts      │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         Adminer (Web UI)                │
│  (Port 8080)                            │
│  - Visual database management           │
│  - Browse/Edit/Query data               │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  (Port 8000 dev / 5000 prod)            │
│  - SQLAlchemy ORM                       │
│  - Alembic Migrations                   │
└─────────────────────────────────────────┘
```

### **Database Initialization Flow**

```
1. Docker starts PostgreSQL container
   └─> Creates empty database "agrisense"

2. Backend connects via SQLAlchemy
   └─> Uses DATABASE_URL from .env

3. Alembic runs migrations
   └─> Creates tables (users, sensor_readings, etc.)

4. (Optional) Seed script populates test data
   └─> Adds sample users, readings, detections, alerts
```

---

## 🔧 ORM: SQLAlchemy (NOT Sequelize)

**You asked about Sequelize - that's for Node.js!**

AgriSense uses **SQLAlchemy**, which is the Python equivalent:

| Feature | Sequelize (Node.js) | SQLAlchemy (Python) |
|---------|---------------------|---------------------|
| Language | JavaScript/TypeScript | Python |
| ORM Type | Active Record | Data Mapper |
| Migrations | Sequelize CLI | Alembic |
| Models | `sequelize.define()` | `class User(Base)` |
| Queries | `User.findAll()` | `db.query(User).all()` |

### **Your Current Setup:**

✅ **SQLAlchemy** - ORM for database operations  
✅ **Alembic** - Database migration tool  
✅ **Pydantic** - Data validation (schemas)  
✅ **FastAPI** - Web framework with dependency injection  

---

## 📁 Project Structure

```
AgriSense/
├── backend/
│   ├── .env                    # ❌ MISSING - Need to create!
│   ├── .env.example            # ✅ Template for .env
│   ├── main.py                 # 🚀 FastAPI app entry point
│   ├── run.py                  # 🏃 Development server starter
│   ├── config.py               # ⚙️ Configuration management
│   ├── database.py             # 🗄️ SQLAlchemy setup
│   ├── requirements.txt        # 📦 Python dependencies
│   │
│   ├── models/                 # 📊 Database models (tables)
│   │   ├── user.py
│   │   ├── sensor_reading.py
│   │   ├── pest_detection.py
│   │   └── alert.py
│   │
│   ├── schemas/                # 📝 Pydantic schemas (validation)
│   │   ├── user.py
│   │   ├── sensor.py
│   │   ├── pest.py
│   │   └── alert.py
│   │
│   ├── routers/                # 🛣️ API endpoints
│   │   ├── auth.py             # /api/v1/auth/*
│   │   ├── sensor.py           # /api/v1/sensors/*
│   │   ├── pest.py             # /api/v1/pest/*
│   │   ├── weather.py          # /api/v1/weather/*
│   │   └── alert.py            # /api/v1/alerts/*
│   │
│   ├── services/               # 💼 Business logic
│   │   ├── auth_service.py
│   │   ├── sensor_service.py
│   │   ├── pest_service.py
│   │   └── weather_service.py
│   │
│   ├── alembic/                # 🔄 Database migrations
│   │   ├── versions/           # Migration files
│   │   ├── env.py              # Alembic config
│   │   └── alembic.ini         # Alembic settings
│   │
│   ├── scripts/                # 🛠️ Utility scripts
│   │   ├── migrate_sqlite_to_postgres.py
│   │   ├── setup_postgres.ps1
│   │   └── seed_database.py
│   │
│   └── tests/                  # 🧪 Unit tests
│
├── docker-compose.yml          # 🐳 Full stack (prod)
├── docker-compose.db.yml       # 🐳 Database only (dev)
└── .env                        # ❌ MISSING - Need to create!
```

---

## 🔐 Environment Files Setup

### **What's Missing:**

❌ `backend/.env` - Backend configuration  
❌ `.env` (root) - Docker Compose variables  

### **What You Need:**

1. **`backend/.env`** - Backend application config
2. **`.env`** (root) - Docker Compose config (optional, has defaults)

---

## 📝 Environment Files Content

### **1. Create `backend/.env`** (Required)

```bash
# Copy from example
cp backend/.env.example backend/.env
```

**Then edit `backend/.env` with these values:**

```env
# ===================================
# Application Settings
# ===================================
APP_NAME=AgriSense
APP_VERSION=1.0.0
DEBUG=True
ENVIRONMENT=development

# ===================================
# Server Configuration
# ===================================
HOST=0.0.0.0
PORT=8000

# ===================================
# Database Configuration
# ===================================
# For PostgreSQL (recommended)
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense

# For SQLite (fallback)
# DATABASE_URL=sqlite:///./agrisense.db

# ===================================
# Authentication & Security
# ===================================
# Generate with: openssl rand -hex 32
SECRET_KEY=your-secret-key-here-change-this-to-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_DAYS=30
BCRYPT_ROUNDS=12

# ===================================
# Weather API (OpenWeatherMap)
# ===================================
# Get free key from: https://openweathermap.org/api
OPENWEATHER_API_KEY=your_api_key_here
OPENWEATHER_BASE_URL=https://api.openweathermap.org/data/2.5
DEFAULT_LATITUDE=3.1390
DEFAULT_LONGITUDE=101.6869
DEFAULT_LOCATION=Kuala Lumpur
WEATHER_CACHE_DURATION=1800

# ===================================
# ML Service Configuration
# ===================================
USE_MOCK_ML=True
ML_SERVICE_URL=http://localhost:8001/predict
ML_SERVICE_TIMEOUT=10

# ===================================
# File Upload Configuration
# ===================================
UPLOAD_DIR=./uploads
MAX_UPLOAD_SIZE=10485760
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png

# ===================================
# Alert System Configuration
# ===================================
TEMP_HIGH_THRESHOLD=32
TEMP_LOW_THRESHOLD=18
HUMIDITY_HIGH_THRESHOLD=85
SOIL_MOISTURE_LOW_THRESHOLD=30
PEST_CONFIDENCE_THRESHOLD=0.80
ALERT_CHECK_INTERVAL=60

# ===================================
# CORS Configuration
# ===================================
CORS_ORIGINS=http://localhost:3000,http://localhost:5173

# ===================================
# Logging Configuration
# ===================================
LOG_LEVEL=INFO
LOG_FILE=./logs/agrisense.log
```

### **2. Create `.env` (root)** (Optional - has defaults)

```env
# PostgreSQL Configuration
POSTGRES_USER=agrisense_user
POSTGRES_PASSWORD=changeme
POSTGRES_DB=agrisense

# Backend Configuration
SECRET_KEY=your-secret-key-here
OPENWEATHER_API_KEY=your_api_key_here
DEBUG=False
ENVIRONMENT=production
USE_MOCK_ML=True
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000
```

---

## 🎯 Quick Setup Commands

### **Option 1: Automated Setup (Recommended)**

```powershell
# 1. Start database
docker compose -f docker-compose.db.yml up -d

# 2. Create .env file
cd backend
cp .env.example .env
# Edit .env and set DATABASE_URL to PostgreSQL

# 3. Run setup script
powershell -ExecutionPolicy Bypass -File scripts/setup_postgres.ps1
```

### **Option 2: Manual Setup**

```bash
# 1. Start database
docker compose -f docker-compose.db.yml up -d

# 2. Create .env
cd backend
cp .env.example .env
# Edit .env: DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
alembic upgrade head

# 5. (Optional) Seed data
python scripts/seed_database.py

# 6. Start backend
python run.py
```

---

## 🌐 Access Points

After setup, you can access:

| Service | URL | Description |
|---------|-----|-------------|
| **Backend API** | http://localhost:8000 | FastAPI REST API |
| **Swagger Docs** | http://localhost:8000/docs | Interactive API documentation |
| **ReDoc** | http://localhost:8000/redoc | Alternative API docs |
| **Adminer** | http://localhost:8080 | Database management UI |
| **PostgreSQL** | localhost:5432 | Direct database connection |

---

## 🔄 Database Migration Flow

```
1. Create/modify models in models/*.py
   └─> Example: Add new field to User model

2. Generate migration
   └─> alembic revision --autogenerate -m "add email to user"

3. Review migration file
   └─> Check alembic/versions/xxxxx_add_email_to_user.py

4. Apply migration
   └─> alembic upgrade head

5. Verify in Adminer
   └─> http://localhost:8080
```

---

## 🛠️ Common Commands

### **Database Management**

```bash
# Start database
docker compose -f docker-compose.db.yml up -d

# Stop database
docker compose -f docker-compose.db.yml down

# View database logs
docker compose -f docker-compose.db.yml logs -f postgres

# Access PostgreSQL CLI
docker exec -it agrisense-postgres psql -U agrisense_user -d agrisense
```

### **Backend Development**

```bash
# Start backend (development)
cd backend
python run.py

# Start backend (production mode)
uvicorn main:app --host 0.0.0.0 --port 8000

# Run tests
pytest

# Check code style
flake8 .
```

### **Alembic Migrations**

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

---

## 🐛 Troubleshooting

### **Issue: "No module named 'psycopg2'"**
```bash
pip install psycopg2-binary
```

### **Issue: "relation does not exist"**
```bash
alembic upgrade head
```

### **Issue: "Can't connect to database"**
```bash
# Check if PostgreSQL is running
docker compose -f docker-compose.db.yml ps

# Check logs
docker compose -f docker-compose.db.yml logs postgres
```

### **Issue: "SECRET_KEY not set"**
```bash
# Generate a secure key
openssl rand -hex 32

# Add to backend/.env
SECRET_KEY=<generated_key>
```

---

## 📊 Current Database Status

Based on your migration script output:

✅ **SQLite Database:** `agrisense.db` (exists)  
✅ **Data:** 5 users, 506 sensor readings, 9 pest detections, 12 alerts  
⚠️ **PostgreSQL:** Not migrated yet  
⚠️ **Alembic:** No migrations run yet  

---

## 🎯 Next Steps

1. ✅ **Create `backend/.env`** file
2. ✅ **Start PostgreSQL** with `docker compose -f docker-compose.db.yml up -d`
3. ✅ **Run setup script** to migrate data
4. ✅ **Access Adminer** at http://localhost:8080
5. ✅ **Start backend** with `python run.py`
6. ✅ **Test API** at http://localhost:8000/docs

---

**Ready to set up? Let me know which step you want to start with!** 🚀
