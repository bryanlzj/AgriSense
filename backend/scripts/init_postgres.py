#!/usr/bin/env python3
"""
Initialize PostgreSQL Database for AgriSense

This script:
1. Connects to PostgreSQL
2. Creates all tables using SQLAlchemy models (ORM)
3. Seeds initial test data
4. Verifies the setup

NO SQLite migration - PostgreSQL only!

Usage:
    python scripts/init_postgres.py

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
from database import Base
from models import User, SensorReading, PestDetection, Alert, SeverityLevel, AlertType, AlertSeverity
from utils.password import get_password_hash
from utils.data_simulator import SensorDataSimulator
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def get_postgres_url():
    """Get PostgreSQL connection URL from environment variables"""
    postgres_user = os.getenv("POSTGRES_USER", "agrisense_user")
    postgres_password = os.getenv("POSTGRES_PASSWORD", "changeme")
    postgres_db = os.getenv("POSTGRES_DB", "agrisense")
    postgres_host = os.getenv("POSTGRES_HOST", "localhost")
    postgres_port = os.getenv("POSTGRES_PORT", "5432")
    
    return f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:{postgres_port}/{postgres_db}"


def test_connection(engine):
    """Test if PostgreSQL connection is working"""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            logger.info(f"✅ PostgreSQL connection successful")
            logger.info(f"   Version: {version.split(',')[0]}")
            return True
    except Exception as e:
        logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
        logger.error("   Make sure PostgreSQL is running: docker-compose up postgres")
        return False


def create_tables(engine):
    """Create all tables using SQLAlchemy models"""
    try:
        logger.info("\n📋 Creating database tables from models...")
        
        # Import all models to ensure they're registered
        from models import User, SensorReading, PestDetection, Alert
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            
        logger.info(f"✅ Created {len(tables)} tables:")
        for table in tables:
            logger.info(f"   - {table}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False


def seed_users(session):
    """Create test users"""
    logger.info("\n👥 Creating test users...")
    
    users = [
        User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_active=True
        ),
        User(
            username="farmer1",
            hashed_password=get_password_hash("password123"),
            is_active=True
        ),
        User(
            username="farmer2",
            hashed_password=get_password_hash("password123"),
            is_active=True
        ),
    ]
    
    for user in users:
        session.add(user)
    
    session.commit()
    
    # Refresh to get IDs
    for user in users:
        session.refresh(user)
    
    logger.info(f"✅ Created {len(users)} users:")
    for user in users:
        logger.info(f"   - {user.username} (ID: {user.id})")
    
    return users


def seed_sensor_readings(session, user, days=7):
    """Create historical sensor readings"""
    logger.info(f"\n📊 Creating sensor readings for {user.username}...")
    
    simulator = SensorDataSimulator()
    historical_data = simulator.generate_historical_data(
        days=days,
        readings_per_day=24  # Hourly readings
    )
    
    readings = []
    for data in historical_data:
        reading = SensorReading(
            user_id=user.id,
            temperature=data['temperature'],
            humidity=data['humidity'],
            soil_moisture=data['soil_moisture'],
            light_intensity=data['light_intensity'],
            timestamp=data['timestamp']
        )
        readings.append(reading)
        session.add(reading)
    
    session.commit()
    
    logger.info(f"✅ Created {len(readings)} sensor readings")
    logger.info(f"   Date range: {readings[0].timestamp} to {readings[-1].timestamp}")


def seed_pest_detections(session, user):
    """Create sample pest detections"""
    logger.info(f"\n🐛 Creating pest detections for {user.username}...")
    
    detections = [
        PestDetection(
            user_id=user.id,
            image_url="/uploads/pest_001.jpg",
            pest_type="Fall Armyworm",
            confidence_score=0.92,
            severity_level=SeverityLevel.HIGH,
            recommendations="1. Apply Bt-based insecticide\n2. Scout fields daily\n3. Remove affected plants\n4. Consider trap crops",
            detected_at=datetime.utcnow() - timedelta(days=2)
        ),
        PestDetection(
            user_id=user.id,
            image_url="/uploads/pest_002.jpg",
            pest_type="Aphids",
            confidence_score=0.85,
            severity_level=SeverityLevel.MEDIUM,
            recommendations="1. Spray with neem oil\n2. Introduce ladybugs\n3. Remove infested leaves\n4. Monitor weekly",
            detected_at=datetime.utcnow() - timedelta(days=5)
        ),
        PestDetection(
            user_id=user.id,
            image_url="/uploads/pest_003.jpg",
            pest_type="Whitefly",
            confidence_score=0.78,
            severity_level=SeverityLevel.LOW,
            recommendations="1. Use yellow sticky traps\n2. Spray with insecticidal soap\n3. Maintain air circulation\n4. Monitor population",
            detected_at=datetime.utcnow() - timedelta(days=7)
        ),
    ]
    
    for detection in detections:
        session.add(detection)
    
    session.commit()
    
    logger.info(f"✅ Created {len(detections)} pest detections:")
    for detection in detections:
        logger.info(f"   - {detection.pest_type} ({detection.severity_level.value}, {detection.confidence_score:.0%})")


def seed_alerts(session, user):
    """Create sample alerts"""
    logger.info(f"\n🔔 Creating alerts for {user.username}...")
    
    alerts = [
        Alert(
            user_id=user.id,
            alert_type=AlertType.HEAVY_RAIN,
            severity=AlertSeverity.HIGH,
            title="Heavy Rain Warning",
            message="Heavy rainfall (65mm) expected tomorrow. Take precautions to protect your crops.",
            recommendations="1. Cover sensitive crops\n2. Ensure proper drainage\n3. Secure equipment\n4. Delay fertilizer application",
            is_read=False,
            created_at=datetime.utcnow() - timedelta(hours=2)
        ),
        Alert(
            user_id=user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.CRITICAL,
            title="Fall Armyworm Detected",
            message="Fall Armyworm detected with 92% confidence. Immediate action required.",
            recommendations="1. Apply Bt-based insecticide\n2. Scout all fields\n3. Remove affected plants\n4. Monitor daily",
            is_read=False,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        Alert(
            user_id=user.id,
            alert_type=AlertType.LOW_SOIL_MOISTURE,
            severity=AlertSeverity.MEDIUM,
            title="Low Soil Moisture Detected",
            message="Soil moisture has dropped to 28%. Your crops may need irrigation.",
            recommendations="1. Irrigate crops soon\n2. Check irrigation system\n3. Consider mulching\n4. Monitor daily",
            is_read=True,
            read_at=datetime.utcnow() - timedelta(days=1),
            created_at=datetime.utcnow() - timedelta(days=3)
        ),
        Alert(
            user_id=user.id,
            alert_type=AlertType.EXTREME_HEAT,
            severity=AlertSeverity.HIGH,
            title="Extreme Heat Warning",
            message="Temperatures expected to reach 38°C tomorrow. Protect crops from heat stress.",
            recommendations="1. Irrigate early morning/evening\n2. Provide shade\n3. Avoid fertilizer\n4. Monitor for wilting",
            is_read=False,
            created_at=datetime.utcnow() - timedelta(hours=6)
        ),
    ]
    
    for alert in alerts:
        session.add(alert)
    
    session.commit()
    
    unread_count = sum(1 for alert in alerts if not alert.is_read)
    logger.info(f"✅ Created {len(alerts)} alerts:")
    logger.info(f"   - {unread_count} unread")
    logger.info(f"   - {len(alerts) - unread_count} read")


def verify_setup(session):
    """Verify database setup"""
    logger.info("\n✅ Verifying database setup...")
    
    user_count = session.query(User).count()
    sensor_count = session.query(SensorReading).count()
    pest_count = session.query(PestDetection).count()
    alert_count = session.query(Alert).count()
    
    logger.info("\n📊 Database Summary:")
    logger.info(f"   Users: {user_count}")
    logger.info(f"   Sensor Readings: {sensor_count}")
    logger.info(f"   Pest Detections: {pest_count}")
    logger.info(f"   Alerts: {alert_count}")
    
    return user_count > 0


def main():
    """Main initialization function"""
    logger.info("=" * 80)
    logger.info("🚀 AgriSense: PostgreSQL Database Initialization")
    logger.info("=" * 80)
    
    # Step 1: Get PostgreSQL URL
    postgres_url = get_postgres_url()
    logger.info(f"\n🐘 Connecting to PostgreSQL...")
    logger.info(f"   Host: {os.getenv('POSTGRES_HOST', 'localhost')}")
    logger.info(f"   Port: {os.getenv('POSTGRES_PORT', '5432')}")
    logger.info(f"   Database: {os.getenv('POSTGRES_DB', 'agrisense')}")
    logger.info(f"   User: {os.getenv('POSTGRES_USER', 'agrisense_user')}")
    
    # Step 2: Create engine and test connection
    engine = create_engine(postgres_url)
    if not test_connection(engine):
        logger.error("\n❌ INITIALIZATION FAILED")
        logger.error("   Cannot connect to PostgreSQL")
        sys.exit(1)
    
    # Step 3: Create tables
    if not create_tables(engine):
        logger.error("\n❌ INITIALIZATION FAILED")
        logger.error("   Cannot create tables")
        sys.exit(1)
    
    # Step 4: Seed data
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Create users
        users = seed_users(session)
        
        # Create data for each user
        for user in users:
            seed_sensor_readings(session, user, days=7)
            seed_pest_detections(session, user)
            seed_alerts(session, user)
        
        # Verify setup
        if not verify_setup(session):
            logger.error("\n❌ INITIALIZATION FAILED")
            logger.error("   Database verification failed")
            sys.exit(1)
        
        logger.info("\n" + "=" * 80)
        logger.info("🎉 INITIALIZATION COMPLETE!")
        logger.info("=" * 80)
        
        logger.info("\n📝 Test Credentials:")
        logger.info("   Admin:   username='admin',   password='admin123'")
        logger.info("   Farmer1: username='farmer1', password='password123'")
        logger.info("   Farmer2: username='farmer2', password='password123'")
        
        logger.info("\n🔗 Access Points:")
        logger.info("   Backend API: http://localhost:5000")
        logger.info("   API Docs: http://localhost:5000/docs")
        logger.info("   Adminer: http://localhost:8080")
        
        logger.info("\n🔐 Adminer Login:")
        logger.info("   System: PostgreSQL")
        logger.info("   Server: postgres")
        logger.info(f"   Username: {os.getenv('POSTGRES_USER', 'agrisense_user')}")
        logger.info(f"   Password: {os.getenv('POSTGRES_PASSWORD', 'changeme')}")
        logger.info(f"   Database: {os.getenv('POSTGRES_DB', 'agrisense')}")
        
        logger.info("\n🚀 Next Steps:")
        logger.info("   1. Start backend: python run.py")
        logger.info("   2. Test API: http://localhost:5000/docs")
        logger.info("   3. View data in Adminer: http://localhost:8080")
        
    except Exception as e:
        logger.error(f"\n❌ Error during seeding: {e}")
        session.rollback()
        sys.exit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()
