@echo off
REM ================================================================================
REM AgriSense: PostgreSQL Direct Setup Script (Windows)
REM ================================================================================
REM This script sets up PostgreSQL database directly using SQLAlchemy models
REM NO SQLite migration - PostgreSQL only!
REM ================================================================================

echo.
echo ================================================================================
echo AgriSense: PostgreSQL Direct Setup
echo ================================================================================
echo.

REM Check if .env exists, if not copy from .env.example
if not exist .env (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
) else (
    echo Backing up .env to .env.backup...
    copy .env .env.backup
    echo.
)

REM Update DATABASE_URL in .env
echo Updating DATABASE_URL to PostgreSQL...
powershell -Command "(Get-Content .env) -replace '^DATABASE_URL=.*', 'DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^# POSTGRES_USER=', 'POSTGRES_USER=' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^# POSTGRES_PASSWORD=', 'POSTGRES_PASSWORD=' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^# POSTGRES_DB=', 'POSTGRES_DB=' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^# POSTGRES_HOST=', 'POSTGRES_HOST=' | Set-Content .env"
powershell -Command "(Get-Content .env) -replace '^# POSTGRES_PORT=', 'POSTGRES_PORT=' | Set-Content .env"
echo.

REM Install dependencies
echo ================================================================================
echo Installing/Upgrading dependencies...
echo ================================================================================
echo.
python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet
echo.

REM Initialize PostgreSQL database
echo ================================================================================
echo Initializing PostgreSQL database...
echo   - Creating tables from SQLAlchemy models
echo   - Seeding test data
echo ================================================================================
echo.

python scripts/init_postgres.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Database initialization failed!
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
echo 3. Start your backend server
echo.
pause
