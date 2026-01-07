@echo off
REM ================================================================================
REM AgriSense - Complete Setup Script (Windows)
REM ================================================================================
REM This script will set up your entire AgriSense application
REM ================================================================================

echo.
echo ================================================================================
echo AgriSense - Complete Setup
echo ================================================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

echo [1/4] Starting PostgreSQL and Adminer...
echo.
cd ..\..\
docker compose up postgres adminer -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to start Docker services!
    pause
    exit /b 1
)

echo.
echo [2/4] Waiting for PostgreSQL to be ready...
timeout /t 5 /nobreak >nul

echo.
echo [3/4] Setting up database...
cd backend
powershell -ExecutionPolicy Bypass -File scripts\setup_postgres.ps1
if %errorlevel% neq 0 (
    echo [ERROR] Database setup failed!
    pause
    exit /b 1
)

echo.
echo [4/4] Setup complete!
echo.
echo ================================================================================
echo Next Steps:
echo ================================================================================
echo.
echo 1. Start the backend:
echo    cd backend
echo    python run.py
echo.
echo 2. Access your application:
echo    - Backend API: http://localhost:8000
echo    - API Docs: http://localhost:8000/docs
echo    - Adminer: http://localhost:8080
echo.
echo 3. Adminer Login:
echo    - System: PostgreSQL
echo    - Server: postgres
echo    - Username: agrisense_user
echo    - Password: changeme
echo    - Database: agrisense
echo.
echo ================================================================================
echo.
pause
