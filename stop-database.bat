@echo off
REM ===================================
REM Stop PostgreSQL + Adminer
REM ===================================

echo Stopping PostgreSQL and Adminer...
docker compose -f docker-compose.db.yml down

echo.
echo ===================================
echo Database services stopped!
echo ===================================
echo.
pause
