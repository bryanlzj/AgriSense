# 🌾 AgriSense Backend

Agricultural Early Warning System - Backend API

## 🚀 Quick Start

### 1. Start PostgreSQL

```bash
docker-compose up -d postgres adminer
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed (default values work for local development)
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Backend

```bash
python run.py
```

**That's it!** The backend will automatically:
- ✅ Check database connection
- ✅ Create missing tables from models
- ✅ Seed test data (if `SEED_DATABASE=True`)

## 📊 Access Points

- **API Documentation:** http://localhost:5000/docs
- **Alternative Docs:** http://localhost:5000/redoc
- **Database UI (Adminer):** http://localhost:8080

## 🔐 Default Credentials

### PostgreSQL
```
Host:     localhost:5432
Database: agrisense
Username: agrisense_user
Password: changeme
```

### Test Users
```
Admin:    admin / admin123
Farmer 1: farmer1 / password123
Farmer 2: farmer2 / password123
```

## ⚙️ Configuration

### Database Seeding

Control test data seeding via `.env`:

```bash
# Seed test data on startup (for development)
SEED_DATABASE=True

# Don't seed test data (for production)
SEED_DATABASE=False
```

When `SEED_DATABASE=True`, the backend creates:
- 3 test users (admin, farmer1, farmer2)
- 7 days of hourly sensor readings
- Sample pest detections
- Sample alerts

**Note:** Seeding only happens if the database is empty. Existing data is never overwritten.

### Database URL

```bash
# PostgreSQL (only supported database)
DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense
```

## 🗄️ Database Schema

Tables are automatically created from SQLAlchemy models:

1. **users** - User accounts and profiles
2. **sensor_readings** - Environmental sensor data
3. **pest_detections** - Pest detection results
4. **alerts** - System alerts and notifications

## 🔄 How It Works

### Automatic Database Initialization

On backend startup, the system:

1. **Checks Connection** - Verifies database is accessible
2. **Checks Schema** - Compares existing tables with models
3. **Creates Missing Tables** - Adds any missing tables
4. **Seeds Data** (optional) - Populates test data if enabled

This happens automatically in `main.py` via the `lifespan` event handler.

### No Manual Scripts Needed

Unlike traditional setups, you don't need to run migration scripts. The ORM handles everything:

```python
# Old way (manual)
python scripts/init_postgres.py
python scripts/seed_data.py

# New way (automatic)
python run.py  # Everything happens automatically!
```

## 🛠️ Development

### Adding New Models

1. Create model in `models/` directory
2. Import model in `db_init.py`
3. Restart backend - table is created automatically!

Example:

```python
# models/new_model.py
from database import Base
from sqlalchemy import Column, Integer, String

class NewModel(Base):
    __tablename__ = "new_table"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
```

```python
# db_init.py
from models.new_model import NewModel  # Add this import
```

### Reset Database

```bash
# Drop all tables
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Restart backend - tables recreated automatically
python run.py
```

### View Database

Open Adminer at http://localhost:8080:
- System: `PostgreSQL`
- Server: `postgres`
- Username: `agrisense_user`
- Password: `changeme`
- Database: `agrisense`

## 📁 Project Structure

```
backend/
├── models/              # SQLAlchemy models (define database schema)
│   ├── user.py
│   ├── sensor_reading.py
│   ├── pest_detection.py
│   └── alert.py
├── routers/             # API endpoints
│   ├── auth.py
│   ├── sensor.py
│   ├── pest.py
│   └── alert.py
├── services/            # Business logic
├── schemas/             # Pydantic schemas
├── db_init.py          # Database initialization (auto-runs on startup)
├── database.py         # Database configuration
├── config.py           # Application settings
├── main.py             # FastAPI application
└── run.py              # Entry point
```

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html
```

## 🐳 Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down
```

## 🔧 Troubleshooting

### "Cannot connect to database"

Check if PostgreSQL is running:
```bash
docker ps
```

Start PostgreSQL:
```bash
docker-compose up -d postgres
```

### "Tables already exist"

This is normal! The system detects existing tables and skips creation.

### "Module not found"

Install dependencies:
```bash
pip install -r requirements.txt
```

### Reset Everything

```bash
# Stop containers
docker-compose down -v

# Start fresh
docker-compose up -d postgres adminer
python run.py
```

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI:** http://localhost:5000/docs
- **ReDoc:** http://localhost:5000/redoc

## 🔐 Security Notes

**For Production:**

1. Change default passwords in `.env`
2. Set `SEED_DATABASE=False`
3. Use strong `SECRET_KEY`
4. Enable HTTPS
5. Restrict CORS origins
6. Use environment-specific configs

## 📝 Environment Variables

See `.env.example` for all available configuration options:

- **Database:** Connection settings
- **Authentication:** JWT settings
- **Weather API:** OpenWeatherMap integration
- **ML Service:** Pest detection service
- **Alerts:** Threshold configurations
- **File Uploads:** Size and type restrictions

## 🚀 Deployment

The backend automatically initializes the database on startup, making deployment simple:

1. Set environment variables
2. Set `SEED_DATABASE=False`
3. Start the application
4. Database is ready!

No manual migration scripts needed.

## 📞 Support

For issues or questions:
1. Check logs: `docker-compose logs backend`
2. Verify `.env` configuration
3. Check database connection
4. Review API docs at `/docs`

---

**Built with:** FastAPI, SQLAlchemy, PostgreSQL, Docker
