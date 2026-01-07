# Troubleshooting Guide

## Common Issues

### 1. "alembic is not recognized"

**Problem:** Alembic is not installed or not in PATH

**Solution:** The scripts now automatically install dependencies. If you still see this error:

```bash
cd backend
pip install -r requirements.txt
```

Then run migrations manually:
```bash
python -m alembic upgrade head
```

---

### 2. "No module named 'psycopg2'"

**Problem:** PostgreSQL driver not installed

**Solution:**
```bash
cd backend
pip install psycopg2-binary==2.9.9
```

---

### 3. "Docker is not running"

**Problem:** Docker Desktop is not started

**Solution:**
1. Start Docker Desktop
2. Wait for it to fully start (whale icon in system tray)
3. Run the setup script again

---

### 4. "Failed to connect to PostgreSQL"

**Problem:** PostgreSQL container is not running or not ready

**Solution:**
```bash
# Check if containers are running
docker compose ps

# If not running, start them
docker compose up postgres adminer -d

# Wait 10 seconds for PostgreSQL to be ready
# Then run the setup script again
```

---

### 5. "relation does not exist"

**Problem:** Database tables haven't been created yet

**Solution:**
```bash
cd backend
python -m alembic upgrade head
```

---

### 6. Manual Setup (if scripts fail)

If the automated scripts fail, follow these steps manually:

```bash
# 1. Start database
docker compose up postgres adminer -d

# 2. Wait 10 seconds
# (Let PostgreSQL fully start)

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Update .env file
# Change DATABASE_URL to:
# DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense

# 5. Run migrations
python -m alembic upgrade head

# 6. Migrate data (optional)
python scripts/migrate_sqlite_to_postgres.py

# 7. Start backend
python run.py
```

---

## Need More Help?

Check the logs:
```bash
# Docker logs
docker compose logs postgres
docker compose logs adminer

# Backend logs
# (visible in terminal when running python run.py)
```
