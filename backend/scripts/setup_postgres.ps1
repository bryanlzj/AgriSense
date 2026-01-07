# ================================================================================
# AgriSense: PostgreSQL Setup Script (PowerShell)
# ================================================================================
# This script will:
# 1. Update .env to use PostgreSQL
# 2. Run Alembic migrations to create tables
# 3. Migrate data from SQLite to PostgreSQL
# ================================================================================

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "AgriSense: PostgreSQL Setup" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists, if not copy from .env.example
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env from .env.example..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
}

# Backup current .env
Write-Host "Backing up .env to .env.backup..." -ForegroundColor Yellow
Copy-Item ".env" ".env.backup" -Force
Write-Host ""

# Update DATABASE_URL in .env
Write-Host "Updating DATABASE_URL in .env..." -ForegroundColor Yellow
$envContent = Get-Content ".env"
$newContent = $envContent -replace '^DATABASE_URL=.*', 'DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense'
$newContent | Set-Content ".env"
Write-Host "✅ DATABASE_URL updated to PostgreSQL" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Installing/Upgrading dependencies..." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

python -m pip install --upgrade pip --quiet
python -m pip install -r requirements.txt --quiet

# Run Alembic migrations
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Running Alembic migrations to create tables..." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

python -m alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ ERROR: Alembic migration failed!" -ForegroundColor Red
    Write-Host "Please check the error above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "✅ Tables created successfully!" -ForegroundColor Green
Write-Host ""

# Migrate data from SQLite to PostgreSQL
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Migrating data from SQLite to PostgreSQL..." -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

python scripts/migrate_sqlite_to_postgres.py

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ ERROR: Data migration failed!" -ForegroundColor Red
    Write-Host "Please check the error above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Green
Write-Host "✅ SUCCESS! PostgreSQL setup complete!" -ForegroundColor Green
Write-Host "================================================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Open Adminer: http://localhost:8080" -ForegroundColor White
Write-Host "2. Login with:" -ForegroundColor White
Write-Host "   - System: PostgreSQL" -ForegroundColor White
Write-Host "   - Server: postgres" -ForegroundColor White
Write-Host "   - Username: agrisense_user" -ForegroundColor White
Write-Host "   - Password: changeme" -ForegroundColor White
Write-Host "   - Database: agrisense" -ForegroundColor White
Write-Host ""
Write-Host "3. Start your backend server (it will now use PostgreSQL)" -ForegroundColor White
Write-Host ""

Read-Host "Press Enter to exit"
