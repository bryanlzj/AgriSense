# PostgreSQL + Adminer Setup

## Quick Start (Windows)

Just double-click: **`start-database.bat`**

This will start PostgreSQL and Adminer in Docker.

## Access Adminer

Open your browser: **http://localhost:8080**

**Login:**
- System: **PostgreSQL**
- Server: **postgres**
- Username: **agrisense_user**
- Password: **changeme**
- Database: **agrisense**

## Migrate Your Data

After starting the database, run:

```bash
cd backend
python scripts/migrate_sqlite_to_postgres.py
```

This will copy all your data from `agrisense.db` (SQLite) to PostgreSQL.

## Stop Database

Double-click: **`stop-database.bat`**

## Manual Commands

```bash
# Start
docker compose -f docker-compose.db.yml up -d

# Stop
docker compose -f docker-compose.db.yml down

# View logs
docker compose -f docker-compose.db.yml logs -f
```
