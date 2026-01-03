# 🗄️ Database Migration Guide - Task 0.3.5

This guide walks you through running the **initial database migration** to create all tables in your SQLite database.

---

## 📋 What This Migration Does

This migration will create **4 database tables**:

1. ✅ **users** - User authentication and profiles
2. ✅ **sensor_readings** - Environmental sensor data (temp, humidity, soil moisture)
3. ✅ **pest_detections** - AI pest detection results with images
4. ✅ **alerts** - Weather warnings and pest risk notifications

---

## 🚀 Step-by-Step Instructions

### **Prerequisites**

Make sure you have:
- ✅ Python 3.10+ installed
- ✅ Virtual environment activated
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ✅ Backend folder structure created

---

### **Step 1: Navigate to Backend Directory**

```bash
cd backend
```

---

### **Step 2: Verify Alembic Configuration**

Check that `alembic.ini` exists:

```bash
ls -la alembic.ini
```

You should see the file. If not, something went wrong in Task 0.2.3.

---

### **Step 3: Generate Migration**

Run this command to auto-generate the migration:

```bash
alembic revision --autogenerate -m "Initial migration: users, sensor_readings, pest_detections, alerts"
```

**What this does:**
- Alembic compares your models to the current database
- Generates a migration file in `alembic/versions/`
- The file contains SQL commands to create tables

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'users'
INFO  [alembic.autogenerate.compare] Detected added table 'sensor_readings'
INFO  [alembic.autogenerate.compare] Detected added table 'pest_detections'
INFO  [alembic.autogenerate.compare] Detected added table 'alerts'
INFO  [alembic.autogenerate.compare] Detected added index 'idx_username_active' on 'users'
INFO  [alembic.autogenerate.compare] Detected added index 'idx_user_timestamp' on 'sensor_readings'
INFO  [alembic.autogenerate.compare] Detected added index 'idx_user_unread_created' on 'alerts'
  Generating /path/to/backend/alembic/versions/xxxx_initial_migration.py ...  done
```

---

### **Step 4: Review the Migration File**

Open the generated migration file:

```bash
ls alembic/versions/
# You'll see a file like: xxxx_initial_migration_users_sensor_readings.py
```

Open it and verify it contains:
- `create_table('users', ...)` 
- `create_table('sensor_readings', ...)`
- `create_table('pest_detections', ...)`
- `create_table('alerts', ...)`
- Index creation statements
- Foreign key constraints

**Example migration file structure:**

```python
def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index('idx_username_active', 'users', ['username', 'is_active'], unique=False)
    
    # Create sensor_readings table
    op.create_table('sensor_readings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=True),
        sa.Column('humidity', sa.Float(), nullable=True),
        sa.Column('soil_moisture', sa.Float(), nullable=True),
        # ... more columns
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create pest_detections table
    op.create_table('pest_detections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('image_path', sa.String(length=500), nullable=False),
        sa.Column('pest_name', sa.String(length=100), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
        sa.Column('severity', sa.Enum('low', 'medium', 'high', 'critical', name='severitylevel'), nullable=True),
        # ... more columns
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create alerts table
    op.create_table('alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('alert_type', sa.Enum('heavy_rain', 'extreme_heat', 'storm_warning', 'low_temperature', 'pest_risk', 'low_soil_moisture', 'high_humidity', 'system', name='alerttype'), nullable=False),
        sa.Column('severity', sa.Enum('low', 'medium', 'high', 'critical', name='alertseverity'), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('recommendations', sa.Text(), nullable=True),
        sa.Column('is_read', sa.Boolean(), nullable=False),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('metadata', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_user_unread_created', 'alerts', ['user_id', 'is_read', 'created_at'], unique=False)
    op.create_index('idx_user_type_severity', 'alerts', ['user_id', 'alert_type', 'severity'], unique=False)
    op.create_index('idx_severity_created', 'alerts', ['severity', 'created_at'], unique=False)

def downgrade():
    # Drop tables in reverse order (to handle foreign keys)
    op.drop_table('alerts')
    op.drop_table('pest_detections')
    op.drop_table('sensor_readings')
    op.drop_table('users')
```

---

### **Step 5: Run the Migration**

Apply the migration to create the tables:

```bash
alembic upgrade head
```

**What this does:**
- Executes the SQL commands in the migration file
- Creates all 4 tables in `agrisense.db`
- Creates all indexes and constraints
- Updates Alembic version tracking

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> xxxx, Initial migration: users, sensor_readings, pest_detections, alerts
```

---

### **Step 6: Verify Tables Were Created**

Check that the database file exists:

```bash
ls -la agrisense.db
```

You should see a file (size will be small, ~20-40 KB).

---

### **Step 7: Inspect Database Tables (Optional)**

Use SQLite command-line tool to verify:

```bash
sqlite3 agrisense.db
```

Then run these SQL commands:

```sql
-- List all tables
.tables

-- Expected output:
-- alembic_version  alerts  pest_detections  sensor_readings  users

-- Show users table structure
.schema users

-- Show alerts table structure
.schema alerts

-- Show sensor_readings table structure
.schema sensor_readings

-- Show pest_detections table structure
.schema pest_detections

-- Exit SQLite
.quit
```

---

### **Step 8: Verify Alembic Version**

Check current migration version:

```bash
alembic current
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
xxxx (head)
```

This confirms the migration was applied successfully!

---

## ✅ Success Checklist

After completing these steps, verify:

- [ ] Migration file generated in `alembic/versions/`
- [ ] Migration file contains all 4 table definitions
- [ ] `alembic upgrade head` ran without errors
- [ ] `agrisense.db` file exists in backend folder
- [ ] `.tables` command shows 5 tables (4 models + alembic_version)
- [ ] `alembic current` shows migration version

---

## 🎓 Understanding What Happened

### **Database Tables Created:**

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **users** | Authentication | username, hashed_password, is_active |
| **sensor_readings** | Environmental data | temperature, humidity, soil_moisture, timestamp |
| **pest_detections** | AI pest detection | image_path, pest_name, confidence, severity |
| **alerts** | Notifications | alert_type, severity, title, message, is_read |

### **Relationships:**

```
users (1) ──→ (many) sensor_readings
users (1) ──→ (many) pest_detections
users (1) ──→ (many) alerts
```

### **Indexes Created:**

- `idx_username_active` - Fast user lookups
- `idx_user_timestamp` - Fast sensor reading queries by time
- `idx_user_confidence` - Fast pest detection queries by confidence
- `idx_user_unread_created` - Fast unread alert queries
- `idx_user_type_severity` - Fast alert filtering by type/severity
- `idx_severity_created` - Fast urgent alert queries

---

## 🐛 Troubleshooting

### **Error: "Can't locate revision identified by 'xxxx'"**

**Solution:** Delete `agrisense.db` and run migration again:

```bash
rm agrisense.db
alembic upgrade head
```

---

### **Error: "Target database is not up to date"**

**Solution:** Check current version and upgrade:

```bash
alembic current
alembic upgrade head
```

---

### **Error: "Table 'users' already exists"**

**Solution:** Database already has tables. Either:

1. **Drop and recreate** (DESTROYS DATA):
   ```bash
   rm agrisense.db
   alembic upgrade head
   ```

2. **Stamp current version** (if tables match models):
   ```bash
   alembic stamp head
   ```

---

### **Error: "No module named 'backend'"**

**Solution:** Make sure you're in the backend directory and PYTHONPATH is set:

```bash
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."
alembic upgrade head
```

---

## 📚 Alembic Commands Reference

| Command | Purpose |
|---------|---------|
| `alembic revision --autogenerate -m "message"` | Generate new migration |
| `alembic upgrade head` | Apply all pending migrations |
| `alembic downgrade -1` | Undo last migration |
| `alembic current` | Show current migration version |
| `alembic history` | Show all migrations |
| `alembic stamp head` | Mark database as up-to-date without running migrations |

---

## 🎯 Next Steps

After successful migration:

1. ✅ **Task 0.3.5 Complete** - Database tables created
2. ⏭️ **Task 0.4.1** - Create password hashing utilities
3. ⏭️ **Task 0.4.2** - Create JWT token utilities
4. ⏭️ **Task 0.4.3** - Create authentication dependencies

---

## 📝 Notes for Learning

### **Why Use Migrations?**

- **Version Control for Database:** Like Git for your database schema
- **Team Collaboration:** Everyone has same database structure
- **Rollback Support:** Can undo changes if something breaks
- **Production Safety:** Apply changes without manual SQL

### **Alembic Workflow:**

```
1. Create/modify models (Python code)
   ↓
2. Generate migration (alembic revision --autogenerate)
   ↓
3. Review migration file (check SQL commands)
   ↓
4. Apply migration (alembic upgrade head)
   ↓
5. Database updated! ✅
```

### **Migration Best Practices:**

- ✅ Always review auto-generated migrations
- ✅ Test migrations on development database first
- ✅ Never edit applied migrations (create new one instead)
- ✅ Commit migration files to Git
- ✅ Use descriptive migration messages

---

## 🎉 Congratulations!

You've successfully created your database schema! All 4 core models are now tables in SQLite, ready to store data for the **AgriSense** dual core features:

- 🌤️ **Weather Early Warning System** (alerts, sensor_readings)
- 🐛 **Pest Risk Management System** (pest_detections, alerts)

---

**Ready to continue?** Next task is **0.4.1: Create Password Hashing Utilities** 🚀
