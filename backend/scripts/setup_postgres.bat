@echo off
REM ================================================================================
REM AgriSense: PostgreSQL Setup Script (Windows)
REM ================================================================================
REM This script will:
REM 1. Update .env to use PostgreSQL
REM 2. Run Alembic migrations to create tables
REM 3. Migrate data from SQLite to PostgreSQL
REM ================================================================================

echo.
echo ================================================================================
echo AgriSense: PostgreSQL Setup
echo ================================================================================
echo.

REM Check if .env exists, if not copy from .env.example
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
)

REM Backup current .env
echo Backing up .env to .env.backup...
copy .env .env.backup
echo.

REM Update DATABASE_URL in .env
echo Updating DATABASE_URL in .env...
powershell -Command "(Get-Content .env) -replace '^DATABASE_URL=.*', 'DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense' | Set-Content .env"
echo.

REM Run Alembic migrations
echo ================================================================================
echo Running Alembic migrations to create tables...
echo ================================================================================
echo.
alembic upgrade head
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Alembic migration failed!
    echo Please check the error above.
    pause
    exit /b 1
)
echo.

REM Migrate data from SQLite to PostgreSQL
echo ================================================================================
echo Migrating data from SQLite to PostgreSQL...
echo ================================================================================
echo.
python scripts/migrate_sqlite_to_postgres.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Data migration failed!
    echo Please check the error above.
    pause
    exit /b 1
)
echo.

echo ================================================================================
echo SUCCESS! PostgreSQL setup complete!
echo ================================================================================
echo.
echo Next steps:
echo 1. Open Adminer: http://localhost:8080
echo 2. Login with:
echo    - System: PostgreSQL
echo    - Server: postgres
echo    - Username: agrisense_user
echo    - Password: changeme
echo    - Database: agrisense
echo.
echo 3. Start your backend server (it will now use PostgreSQL)
echo.
pause
