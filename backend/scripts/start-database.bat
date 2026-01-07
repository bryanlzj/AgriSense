@echo off
REM ===================================
REM Start PostgreSQL + Adminer
REM ===================================

echo Starting PostgreSQL and Adminer...
docker compose -f docker-compose.db.yml up -d

echo.
echo ===================================
echo Database services started!
echo ===================================
echo.
echo PostgreSQL: localhost:5432
echo Adminer: http://localhost:8080
echo.
echo Adminer Login:
echo   System: PostgreSQL
echo   Server: postgres
echo   Username: agrisense_user
echo   Password: changeme
echo   Database: agrisense
echo.
pause
