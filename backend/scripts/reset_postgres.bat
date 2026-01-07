@echo off
REM Reset PostgreSQL database (drop and recreate schema)

echo ================================================================================
echo Resetting PostgreSQL Database
echo ================================================================================
echo.

echo Dropping and recreating schema...
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Failed to reset database
    echo Make sure PostgreSQL container is running: docker ps
    pause
    exit /b 1
)

echo.
echo ✅ Database reset successfully!
echo.
echo Now run: START_HERE.bat
echo.
pause
