# PostgreSQL + Adminer Setup

## Quick Setup (One Command)

```bash
cd backend
bash scripts/quick_postgres_setup.sh
```

This will:
- Start PostgreSQL + Adminer with Docker
- Update .env with PostgreSQL URL
- Run migrations
- Migrate your data from SQLite

## Access Adminer (Database Manager)

**URL:** http://localhost:8080

**Login:**
- System: PostgreSQL
- Server: postgres
- Username: agrisense_user
- Password: changeme
- Database: agrisense

## Manual Setup

```bash
# Start services
docker-compose up -d postgres adminer

# Update .env
# Change DATABASE_URL to: postgresql://agrisense_user:changeme@localhost:5432/agrisense

# Run migrations
cd backend
alembic upgrade head

# Migrate data
python scripts/migrate_sqlite_to_postgres.py
```

## Useful Commands

```bash
# Start/stop services
docker-compose up -d postgres adminer
docker-compose down

# View logs
docker-compose logs -f postgres

# Backup database
docker exec -t agrisense-postgres pg_dump -U agrisense_user agrisense > backup.sql

# Restore database
cat backup.sql | docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense
```
