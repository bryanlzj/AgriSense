# Fix Migration Issue

The migration failed because the database schema was partially created with the wrong structure.

## Quick Fix (2 steps):

### Step 1: Reset PostgreSQL Database
```bash
cd backend\scripts
reset_postgres.bat
```

This will drop and recreate the database schema.

### Step 2: Run Setup Again
```bash
START_HERE.bat
```

This will:
- Create tables with correct schema
- Migrate data from SQLite to PostgreSQL

---

## What Was Fixed:

1. **PestDetection Model Fields:**
   - Old: `pest_name`, `confidence`, `severity`, `image_path`
   - New: `pest_type`, `confidence_score`, `severity_level`, `image_url`

2. **Migration Script:**
   - Updated to handle field name differences between SQLite and PostgreSQL
   - Uses `getattr()` to safely access fields that may have different names

3. **Alembic Migration:**
   - Updated to match the actual PestDetection model structure
   - Added `detections_json` field for complex ML results

---

## Alternative: Manual Reset

If the batch script doesn't work, run this command directly:

```bash
docker exec -i agrisense-postgres psql -U agrisense_user -d agrisense -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
```

Then run `START_HERE.bat` again.
