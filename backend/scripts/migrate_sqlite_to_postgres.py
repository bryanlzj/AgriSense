#!/usr/bin/env python3
"""
Migrate data from SQLite to PostgreSQL

This script:
1. Reads all data from your existing SQLite database (agrisense.db)
2. Connects to PostgreSQL
3. Transfers all data (users, sensor readings, pest detections, alerts)
4. Preserves relationships and IDs

Usage:
    python scripts/migrate_sqlite_to_postgres.py

Prerequisites:
    - PostgreSQL must be running (docker-compose up postgres)
    - .env file must have PostgreSQL credentials
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import User, SensorReading, PestDetection, Alert
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def migrate_data():
    """Migrate all data from SQLite to PostgreSQL"""
    
    # ============================================================================
    # STEP 1: Connect to SQLite (source database)
    # ============================================================================
    
    sqlite_path = backend_dir / "agrisense.db"
    
    if not sqlite_path.exists():
        logger.error(f"❌ SQLite database not found at: {sqlite_path}")
        logger.error("   Make sure you're running this from the backend directory")
        return False
    
    logger.info(f"📂 Found SQLite database: {sqlite_path}")
    
    sqlite_url = f"sqlite:///{sqlite_path}"
    sqlite_engine = create_engine(sqlite_url)
    SQLiteSession = sessionmaker(bind=sqlite_engine)
    sqlite_session = SQLiteSession()
    
    # ============================================================================
    # STEP 2: Connect to PostgreSQL (destination database)
    # ============================================================================
    
    # Get PostgreSQL credentials from environment
    postgres_user = os.getenv("POSTGRES_USER", "agrisense_user")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "changeme")
    postgres_db = os.getenv("POSTGRES_DB", "agrisense")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    
    postgres_url = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"
    
    logger.info(f"🐘 Connecting to PostgreSQL at {postgres_host}:{postgres_port}/{postgres_db}")
    
    try:
        postgres_engine = create_engine(postgres_url)
        # Test connection
        with postgres_engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✅ PostgreSQL connection successful")
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        logger.error("   Make sure PostgreSQL is running: docker-compose up postgres")
        return False
    
    PostgresSession = sessionmaker(bind=postgres_engine)
    postgres_session = PostgresSession()
    
    # ============================================================================
    # STEP 3: Count records in SQLite
    # ============================================================================
    
    user_count = sqlite_session.query(User).count()
    sensor_count = sqlite_session.query(SensorReading).count()
    pest_count = sqlite_session.query(PestDetection).count()
    alert_count = sqlite_session.query(Alert).count()
    
    logger.info("\n📊 Records in SQLite database:")
    logger.info(f"   Users: {user_count}")
    logger.info(f"   Sensor Readings: {sensor_count}")
    logger.info(f"   Pest Detections: {pest_count}")
    logger.info(f"   Alerts: {alert_count}")
    
    if user_count == 0:
        logger.warning("⚠️  No data found in SQLite database")
        logger.warning("   Run 'python scripts/seed_data.py' first to populate data")
        return False
    
    # ============================================================================
    # STEP 4: Clear existing data in PostgreSQL (optional)
    # ============================================================================
    
    logger.info("\n🗑️  Clearing existing data in PostgreSQL...")
    
    try:
        postgres_session.query(Alert).delete()
        postgres_session.query(PestDetection).delete()
        postgres_session.query(SensorReading).delete()
        postgres_session.query(User).delete()
        postgres_session.commit()
        logger.info("✅ PostgreSQL tables cleared")
    except Exception as e:
        logger.error(f"❌ Failed to clear PostgreSQL tables: {e}")
        postgres_session.rollback()
        return False
    
    # ============================================================================
    # STEP 5: Migrate Users
    # ============================================================================
    
    logger.info("\n👤 Migrating users...")
    
    try:
        users = sqlite_session.query(User).all()
        
        for user in users:
            # Create new user object (don't copy the id, let PostgreSQL auto-generate)
            new_user = User(
                id=user.id,  # Preserve original ID for relationships
                username=user.username,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                created_at=user.created_at
            )
            postgres_session.add(new_user)
        
        postgres_session.commit()
        logger.info(f"✅ Migrated {len(users)} users")
    except Exception as e:
        logger.error(f"❌ Failed to migrate users: {e}")
        postgres_session.rollback()
        return False
    
    # ============================================================================
    # STEP 6: Migrate Sensor Readings
    # ============================================================================
    
    logger.info("\n📊 Migrating sensor readings...")
    
    try:
        readings = sqlite_session.query(SensorReading).all()
        
        for reading in readings:
            new_reading = SensorReading(
                id=reading.id,
                user_id=reading.user_id,
                temperature=reading.temperature,
                humidity=reading.humidity,
                soil_moisture=reading.soil_moisture,
                light_intensity=reading.light_intensity,
                timestamp=reading.timestamp
            )
            postgres_session.add(new_reading)
        
        postgres_session.commit()
        logger.info(f"✅ Migrated {len(readings)} sensor readings")
    except Exception as e:
        logger.error(f"❌ Failed to migrate sensor readings: {e}")
        postgres_session.rollback()
        return False
    
    # ============================================================================
    # STEP 7: Migrate Pest Detections
    # ============================================================================
    
    logger.info("\n🐛 Migrating pest detections...")
    
    try:
        detections = sqlite_session.query(PestDetection).all()
        
        for detection in detections:
            # Handle field name differences between old SQLite and new PostgreSQL schema
            confidence = getattr(detection, 'confidence_score', None) or getattr(detection, 'confidence', None)
            severity = getattr(detection, 'severity_level', None) or getattr(detection, 'severity', None)
            image_url = getattr(detection, 'image_url', None) or getattr(detection, 'image_path', None)
            
            new_detection = PestDetection(
                id=detection.id,
                user_id=detection.user_id,
                image_url=image_url,
                pest_type=getattr(detection, 'pest_type', None) or getattr(detection, 'pest_name', None),
                confidence_score=confidence,
                severity_level=severity,
                recommendations=getattr(detection, 'recommendations', None),
                detected_at=detection.detected_at
            )
            postgres_session.add(new_detection)
        
        postgres_session.commit()
        logger.info(f"✅ Migrated {len(detections)} pest detections")
    except Exception as e:
        logger.error(f"❌ Failed to migrate pest detections: {e}")
        postgres_session.rollback()
        return False
    
    # ============================================================================
    # STEP 8: Migrate Alerts
    # ============================================================================
    
    logger.info("\n🔔 Migrating alerts...")
    
    try:
        alerts = sqlite_session.query(Alert).all()
        
        for alert in alerts:
            new_alert = Alert(
                id=alert.id,
                user_id=alert.user_id,
                alert_type=alert.alert_type,
                title=alert.title,
                message=alert.message,
                severity=alert.severity,
                recommendations=alert.recommendations,
                is_read=alert.is_read,
                read_at=alert.read_at,
                created_at=alert.created_at,
                expires_at=alert.expires_at,
                metadata=alert.metadata
            )
            postgres_session.add(new_alert)
        
        postgres_session.commit()
        logger.info(f"✅ Migrated {len(alerts)} alerts")
    except Exception as e:
        logger.error(f"❌ Failed to migrate alerts: {e}")
        postgres_session.rollback()
        return False
    
    # ============================================================================
    # STEP 9: Verify migration
    # ============================================================================
    
    logger.info("\n✅ Verifying migration...")
    
    pg_user_count = postgres_session.query(User).count()
    pg_sensor_count = postgres_session.query(SensorReading).count()
    pg_pest_count = postgres_session.query(PestDetection).count()
    pg_alert_count = postgres_session.query(Alert).count()
    
    logger.info("\n📊 Records in PostgreSQL database:")
    logger.info(f"   Users: {pg_user_count} (expected: {user_count})")
    logger.info(f"   Sensor Readings: {pg_sensor_count} (expected: {sensor_count})")
    logger.info(f"   Pest Detections: {pg_pest_count} (expected: {pest_count})")
    logger.info(f"   Alerts: {pg_alert_count} (expected: {alert_count})")
    
    # Check if counts match
    if (pg_user_count == user_count and 
        pg_sensor_count == sensor_count and 
        pg_pest_count == pest_count and 
        pg_alert_count == alert_count):
        logger.info("\n🎉 Migration completed successfully!")
        logger.info("   All data has been transferred from SQLite to PostgreSQL")
        return True
    else:
        logger.error("\n❌ Migration verification failed!")
        logger.error("   Record counts don't match. Please check the logs above.")
        return False
    
    # Close sessions
    sqlite_session.close()
    postgres_session.close()


if __name__ == "__main__":
    logger.info("=" * 80)
    logger.info("🚀 AgriSense: SQLite to PostgreSQL Migration")
    logger.info("=" * 80)
    
    success = migrate_data()
    
    if success:
        logger.info("\n" + "=" * 80)
        logger.info("✅ MIGRATION COMPLETE")
        logger.info("=" * 80)
        logger.info("\nNext steps:")
        logger.info("1. Update your .env file:")
        logger.info("   DATABASE_URL=postgresql://agrisense_user:changeme@localhost:5432/agrisense")
        logger.info("2. Restart your backend server")
        logger.info("3. Access Adminer at http://localhost:8080")
        logger.info("   - System: PostgreSQL")
        logger.info("   - Server: postgres")
        logger.info("   - Username: agrisense_user")
        logger.info("   - Password: changeme")
        logger.info("   - Database: agrisense")
    else:
        logger.error("\n" + "=" * 80)
        logger.error("❌ MIGRATION FAILED")
        logger.error("=" * 80)
        sys.exit(1)
