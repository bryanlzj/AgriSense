"""
Database Configuration and Session Management

This module sets up SQLAlchemy for database operations.
It supports both SQLite (for development/learning) and PostgreSQL (for production).

Key Concepts:
- Engine: Manages database connections
- SessionLocal: Creates database sessions for transactions
- Base: Base class for all database models (tables)
"""

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
import logging

from config import settings, get_database_url, is_development, is_production

# Set up logging
logger = logging.getLogger(__name__)

# ============================================================================
# DATABASE ENGINE SETUP
# ============================================================================

# Get database URL from config (SQLite or PostgreSQL)
DATABASE_URL = get_database_url()

# Create engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite Configuration (for development/learning)
    # - check_same_thread=False: Allow multiple threads (needed for FastAPI)
    # - StaticPool: Keep connection alive (good for SQLite)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG  # Log SQL queries in debug mode (great for learning!)
    )
    
    # Enable foreign key constraints for SQLite (disabled by default)
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
    
    logger.info("🗄️  Using SQLite database (Development Mode)")

else:
    # PostgreSQL Configuration (for production)
    # - pool_size: Number of connections to keep open
    # - max_overflow: Additional connections when pool is full
    # - pool_pre_ping: Test connections before using (handles disconnects)
    engine = create_engine(
        DATABASE_URL,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        echo=settings.DEBUG
    )
    
    logger.info("🗄️  Using PostgreSQL database (Production Mode)")

# ============================================================================
# SESSION FACTORY
# ============================================================================

# SessionLocal: Factory for creating database sessions
# - autocommit=False: Transactions must be explicitly committed
# - autoflush=False: Don't automatically flush changes (more control)
# - bind=engine: Connect to our database engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ============================================================================
# BASE MODEL CLASS
# ============================================================================

# Base: All database models (tables) will inherit from this
# Example: class User(Base): ...
Base = declarative_base()

# ============================================================================
# DATABASE SESSION DEPENDENCY
# ============================================================================

def get_db() -> Session:
    """
    Dependency function for FastAPI routes to get database sessions.
    
    Usage in FastAPI:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            users = db.query(User).all()
            return users
    
    How it works:
    1. Creates a new database session
    2. Yields it to the route function
    3. Automatically closes the session when done (even if error occurs)
    
    This is called "Dependency Injection" - FastAPI handles it automatically!
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """
    Initialize the database by creating all tables.
    
    This should be called when the application starts.
    It creates tables for all models that inherit from Base.
    
    Note: In production, use Alembic migrations instead!
    """
    try:
        # Import all models here so they're registered with Base
        # We'll add these imports as we create the models
        # from app.models import user, sensor_data, pest_detection, alert
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise

def drop_db():
    """
    Drop all database tables.
    
    ⚠️ WARNING: This deletes ALL data!
    Only use this for testing or resetting development database.
    """
    try:
        Base.metadata.drop_all(bind=engine)
        logger.info("🗑️  All database tables dropped")
    except Exception as e:
        logger.error(f"❌ Error dropping database tables: {e}")
        raise

# ============================================================================
# DATABASE HEALTH CHECK
# ============================================================================

def check_db_connection() -> bool:
    """
    Check if database connection is working.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        # Try to execute a simple query
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_db_info() -> dict:
    """
    Get information about the current database configuration.
    
    Useful for debugging and health checks.
    """
    return {
        "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,  # Hide password
        "database_type": "sqlite" if DATABASE_URL.startswith("sqlite") else "postgresql",
        "is_development": is_development(),
        "is_production": is_production(),
        "debug_mode": settings.DEBUG
    }

# ============================================================================
# LEARNING NOTES
# ============================================================================

"""
📚 Key Concepts Explained:

1. **SQLAlchemy ORM (Object-Relational Mapping)**
   - Lets you work with database tables as Python classes
   - No need to write raw SQL (SQLAlchemy generates it)
   - Example: db.query(User).filter(User.username == "ahmad").first()

2. **Database Session**
   - A "conversation" with the database
   - Groups multiple operations into a transaction
   - Must be closed after use (we use try/finally for this)

3. **Dependency Injection (get_db)**
   - FastAPI automatically calls get_db() for each request
   - Provides a fresh database session to your route
   - Automatically closes the session when done

4. **Base Class**
   - All your models inherit from Base
   - SQLAlchemy uses this to track all your tables
   - Base.metadata.create_all() creates all tables at once

5. **Connection Pooling**
   - Keeps database connections open for reuse
   - Faster than creating new connections each time
   - Configured differently for SQLite vs PostgreSQL

6. **SQLite vs PostgreSQL**
   - SQLite: Single file, great for learning/development
   - PostgreSQL: Full database server, better for production
   - This code supports both seamlessly!

Next Steps:
- Create database models (User, SensorData, PestDetection, Alert)
- Use Alembic for database migrations (tracks schema changes)
- Add CRUD operations (Create, Read, Update, Delete)
"""
