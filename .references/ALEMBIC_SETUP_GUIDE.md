# Alembic Database Migrations - Setup Guide

**Created:** January 3, 2025  
**Task:** 0.2.4 - Set up Alembic for migrations  
**Status:** ✅ Complete

---

## 📚 What is Alembic?

Alembic is a **database migration tool** for SQLAlchemy. Think of it as "Git for your database schema."

### Why Use Migrations?

✅ **Version Control** - Track all changes to your database structure  
✅ **Reproducibility** - Apply same changes across dev/staging/production  
✅ **Collaboration** - Multiple developers can work on database changes  
✅ **Rollback** - Undo changes if something goes wrong  
✅ **Documentation** - Each migration documents what changed and why  

---

## 📁 Files Created

### 1. `backend/alembic.ini` (106 lines)
Main configuration file for Alembic.

**Key Settings:**
- `script_location = alembic` - Where migration scripts are stored
- `file_template` - How migration files are named (includes timestamp)
- `sqlalchemy.url` - Database connection (overridden by env.py)
- Logging configuration

### 2. `backend/alembic/env.py` (126 lines)
Environment configuration - runs when migrations execute.

**Key Functions:**
- `get_url()` - Gets database URL from config.py (uses environment variables)
- `run_migrations_offline()` - Generate SQL scripts without connecting to DB
- `run_migrations_online()` - Connect to DB and apply migrations directly

**Important:**
```python
from models import *  # Imports all models so Alembic can detect them
target_metadata = Base.metadata  # Links to SQLAlchemy models
```

### 3. `backend/alembic/script.py.mako` (36 lines)
Template for generating new migration files.

**Structure:**
```python
def upgrade():
    """Apply changes to database"""
    pass

def downgrade():
    """Revert changes (rollback)"""
    pass
```

### 4. `backend/alembic/README` (72 lines)
Documentation with common commands and workflow.

### 5. `backend/alembic/versions/` (directory)
Where migration scripts will be stored (currently empty).

---

## 🚀 How to Use Alembic (When Running Locally)

### Step 1: Create Your First Migration

After you create database models (e.g., User, SensorReading), generate a migration:

```bash
cd backend
source venv/bin/activate  # Activate virtual environment

# Auto-generate migration from model changes
alembic revision --autogenerate -m "Create users table"
```

This creates a file like: `alembic/versions/20250103_1400_create_users_table.py`

### Step 2: Review the Migration

Open the generated file and check:
- ✅ Does `upgrade()` create the table correctly?
- ✅ Does `downgrade()` drop the table?
- ✅ Are column types correct?
- ✅ Are foreign keys defined?

**Always review auto-generated migrations!** Alembic is smart but not perfect.

### Step 3: Apply the Migration

```bash
# Apply all pending migrations
alembic upgrade head

# Or apply one migration at a time
alembic upgrade +1
```

### Step 4: Verify

```bash
# Check current database version
alembic current

# View migration history
alembic history --verbose
```

---

## 🔄 Common Migration Workflows

### Adding a New Column

1. **Edit your model:**
```python
# models/user.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))  # NEW COLUMN
```

2. **Generate migration:**
```bash
alembic revision --autogenerate -m "Add email to users"
```

3. **Review and apply:**
```bash
# Review the generated file first!
alembic upgrade head
```

### Rolling Back a Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade abc123

# Rollback all migrations
alembic downgrade base
```

### Viewing Migration Status

```bash
# Current database version
alembic current

# All migrations (applied and pending)
alembic history

# Detailed history
alembic history --verbose
```

---

## 🎓 Learning Concepts

### 1. **Revision Chain**
Migrations form a linked list:
```
None → abc123 → def456 → ghi789 (current)
```

Each migration knows:
- `revision` - Its own ID
- `down_revision` - Previous migration ID

### 2. **Autogenerate vs Manual**

**Autogenerate** (recommended):
```bash
alembic revision --autogenerate -m "Add users table"
```
- Compares models to database
- Generates upgrade/downgrade automatically
- Still requires review!

**Manual** (for complex changes):
```bash
alembic revision -m "Custom data migration"
```
- You write upgrade/downgrade yourself
- Useful for data transformations
- More control, more work

### 3. **Upgrade vs Downgrade**

**Upgrade:**
- Moves database forward (apply changes)
- `alembic upgrade head`

**Downgrade:**
- Moves database backward (undo changes)
- `alembic downgrade -1`

Always write downgrade functions! You'll thank yourself later.

---

## 🔧 Integration with AgriSense

### Database Configuration Flow

```
1. config.py reads DATABASE_URL from .env
2. database.py creates SQLAlchemy engine
3. alembic/env.py imports config.py
4. Alembic uses same database URL
5. Migrations apply to correct database
```

### Environment-Specific Migrations

**Development (SQLite):**
```bash
# .env
DATABASE_URL=sqlite:///./agrisense.db
```

**Production (PostgreSQL):**
```bash
# .env
DATABASE_URL=postgresql://user:pass@localhost/agrisense
```

Alembic automatically uses the correct database!

---

## ⚠️ Important Best Practices

### DO:
✅ **Review all auto-generated migrations** before applying  
✅ **Write downgrade functions** for every migration  
✅ **Test migrations on development database** first  
✅ **Keep migrations small** - one logical change per migration  
✅ **Commit migrations to Git** - they're part of your code  
✅ **Run migrations in order** - never skip or reorder  

### DON'T:
❌ **Never edit applied migrations** - create a new one instead  
❌ **Don't delete migrations** - breaks the revision chain  
❌ **Don't run migrations manually** - use Alembic commands  
❌ **Don't skip reviewing** - auto-generate isn't perfect  
❌ **Don't forget downgrade** - you'll need it someday  

---

## 🐛 Troubleshooting

### "Target database is not up to date"
```bash
# Check current version
alembic current

# Apply pending migrations
alembic upgrade head
```

### "Can't locate revision identified by 'abc123'"
```bash
# Revision chain is broken - check versions/ folder
ls alembic/versions/

# Stamp database to specific version (use carefully!)
alembic stamp head
```

### "No module named 'models'"
```bash
# Make sure you're in the backend directory
cd backend

# Make sure models are imported in env.py
# Check: from models import *
```

### Alembic can't detect model changes
```bash
# Make sure models inherit from Base
from database import Base

class User(Base):
    __tablename__ = "users"
    # ...

# Make sure models are imported in env.py
```

---

## 📖 Next Steps

After Alembic is set up, you'll:

1. **Create database models** (Task 0.3.1 - User model)
2. **Generate first migration** (`alembic revision --autogenerate`)
3. **Apply migration** (`alembic upgrade head`)
4. **Verify tables created** (check database)

---

## 🔗 Resources

- **Alembic Documentation:** https://alembic.sqlalchemy.org/
- **Tutorial:** https://alembic.sqlalchemy.org/en/latest/tutorial.html
- **Auto-generate:** https://alembic.sqlalchemy.org/en/latest/autogenerate.html
- **SQLAlchemy ORM:** https://docs.sqlalchemy.org/en/20/orm/

---

**Status:** ✅ Alembic is configured and ready to use!  
**Next Task:** 0.3.1 - Create User model (first database table)
