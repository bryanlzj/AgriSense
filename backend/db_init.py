"""
Database Initialization Module

This module handles automatic database setup on backend startup:
1. Checks if database tables exist
2. Creates missing tables from SQLAlchemy models
3. Optionally seeds test data based on SEED_DATABASE flag

No manual scripts needed - everything happens automatically!
"""

import logging
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError
from database import engine, SessionLocal, Base
from config import settings

# Import all models to ensure they're registered with Base.metadata
from models.user import User
from models.sensor_reading import SensorReading
from models.pest_detection import PestDetection
from models.alert import Alert

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_database_connection() -> bool:
    """
    Check if database is accessible
    
    Returns:
        bool: True if database is accessible, False otherwise
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("✓ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False


def get_existing_tables() -> set:
    """
    Get list of existing tables in the database
    
    Returns:
        set: Set of table names that exist in the database
    """
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    return existing_tables


def get_model_tables() -> set:
    """
    Get list of tables defined in SQLAlchemy models
    
    Returns:
        set: Set of table names from models
    """
    model_tables = set(Base.metadata.tables.keys())
    return model_tables


def create_missing_tables():
    """
    Create any missing tables in the database
    
    This function:
    1. Compares existing tables with model definitions
    2. Creates only the missing tables
    3. Does not drop or modify existing tables
    """
    try:
        existing_tables = get_existing_tables()
        model_tables = get_model_tables()
        
        missing_tables = model_tables - existing_tables
        
        if not missing_tables:
            logger.info("✓ All tables exist - no changes needed")
            return
        
        logger.info(f"Creating missing tables: {', '.join(missing_tables)}")
        
        # Create only missing tables
        Base.metadata.create_all(bind=engine, checkfirst=True)
        
        logger.info(f"✓ Successfully created {len(missing_tables)} table(s)")
        
    except SQLAlchemyError as e:
        logger.error(f"✗ Error creating tables: {e}")
        raise


def verify_tables():
    """
    Verify that all required tables exist
    
    Returns:
        bool: True if all tables exist, False otherwise
    """
    existing_tables = get_existing_tables()
    model_tables = get_model_tables()
    
    missing_tables = model_tables - existing_tables
    
    if missing_tables:
        logger.warning(f"Missing tables: {', '.join(missing_tables)}")
        return False
    
    logger.info(f"✓ All {len(model_tables)} tables verified")
    return True


def seed_test_data():
    """
    Seed the database with test data
    
    Creates:
    - 3 test users (admin, farmer1, farmer2)
    - 7 days of sensor readings (hourly)
    - Sample pest detections
    - Sample alerts
    """
    from datetime import datetime, timedelta
    from passlib.context import CryptContext
    import random
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_users = db.query(User).count()
        if existing_users > 0:
            logger.info(f"✓ Database already has {existing_users} user(s) - skipping seed")
            return
        
        logger.info("Seeding test data...")
        
        # Create test users
        users_data = [
            {
                "username": "admin",
                "email": "admin@agrisense.com",
                "password": "admin123",
                "full_name": "Admin User",
                "phone_number": "+60123456789",
                "farm_location": "Kuala Lumpur",
                "farm_size": 10.0,
                "crop_types": "Rice, Vegetables",
                "is_active": True,
                "is_admin": True
            },
            {
                "username": "farmer1",
                "email": "farmer1@agrisense.com",
                "password": "password123",
                "full_name": "John Farmer",
                "phone_number": "+60123456790",
                "farm_location": "Penang",
                "farm_size": 5.5,
                "crop_types": "Rice",
                "is_active": True,
                "is_admin": False
            },
            {
                "username": "farmer2",
                "email": "farmer2@agrisense.com",
                "password": "password123",
                "full_name": "Jane Grower",
                "phone_number": "+60123456791",
                "farm_location": "Johor",
                "farm_size": 8.0,
                "crop_types": "Vegetables, Fruits",
                "is_active": True,
                "is_admin": False
            }
        ]
        
        created_users = []
        for user_data in users_data:
            password = user_data.pop("password")
            user = User(
                **user_data,
                hashed_password=pwd_context.hash(password)
            )
            db.add(user)
            created_users.append(user)
        
        db.commit()
        logger.info(f"✓ Created {len(created_users)} test users")
        
        # Create sensor readings (7 days of hourly data)
        sensor_readings = []
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)
        
        for user in created_users:
            current_time = start_time
            while current_time <= end_time:
                reading = SensorReading(
                    user_id=user.id,
                    temperature=round(random.uniform(22, 32), 1),
                    humidity=round(random.uniform(50, 85), 1),
                    soil_moisture=round(random.uniform(30, 70), 1),
                    light_intensity=round(random.uniform(200, 900), 1),
                    timestamp=current_time
                )
                sensor_readings.append(reading)
                current_time += timedelta(hours=1)
        
        db.bulk_save_objects(sensor_readings)
        db.commit()
        logger.info(f"✓ Created {len(sensor_readings)} sensor readings")
        
        # Create pest detections
        pest_types = ["Brown Planthopper", "Rice Leaf Roller", "Stem Borer"]
        pest_detections = []
        
        for user in created_users:
            for i in range(3):
                detection = PestDetection(
                    user_id=user.id,
                    pest_type=random.choice(pest_types),
                    confidence_score=round(random.uniform(0.75, 0.98), 2),
                    severity_level=random.choice(["low", "medium", "high"]),
                    image_path=f"/uploads/pest_{user.id}_{i}.jpg",
                    location=user.farm_location,
                    detected_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
                )
                pest_detections.append(detection)
        
        db.bulk_save_objects(pest_detections)
        db.commit()
        logger.info(f"✓ Created {len(pest_detections)} pest detections")
        
        # Create alerts
        alert_types = ["temperature_high", "humidity_high", "soil_moisture_low", "pest_detected"]
        alerts = []
        
        for user in created_users:
            for i in range(4):
                alert = Alert(
                    user_id=user.id,
                    alert_type=alert_types[i],
                    severity=random.choice(["low", "medium", "high"]),
                    title=f"Alert: {alert_types[i].replace('_', ' ').title()}",
                    message=f"Test alert message for {alert_types[i]}",
                    is_read=random.choice([True, False]),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
                )
                alerts.append(alert)
        
        db.bulk_save_objects(alerts)
        db.commit()
        logger.info(f"✓ Created {len(alerts)} alerts")
        
        logger.info("✓ Test data seeding completed successfully")
        
    except Exception as e:
        db.rollback()
        logger.error(f"✗ Error seeding test data: {e}")
        raise
    finally:
        db.close()


def initialize_database():
    """
    Main initialization function
    
    This function is called on backend startup and:
    1. Checks database connection
    2. Creates missing tables
    3. Seeds test data if SEED_DATABASE=True
    
    Returns:
        bool: True if initialization successful, False otherwise
    """
    logger.info("=" * 60)
    logger.info("Starting database initialization...")
    logger.info("=" * 60)
    
    try:
        # Step 1: Check database connection
        if not check_database_connection():
            logger.error("Cannot proceed without database connection")
            return False
        
        # Step 2: Create missing tables
        logger.info("Checking database schema...")
        create_missing_tables()
        
        # Step 3: Verify all tables exist
        if not verify_tables():
            logger.error("Table verification failed")
            return False
        
        # Step 4: Seed test data if enabled
        if settings.seed_database:
            logger.info("SEED_DATABASE=True - seeding test data...")
            seed_test_data()
        else:
            logger.info("SEED_DATABASE=False - skipping test data")
        
        logger.info("=" * 60)
        logger.info("✓ Database initialization completed successfully")
        logger.info("=" * 60)
        
        # Print summary
        existing_tables = get_existing_tables()
        logger.info(f"Database: {engine.url.database}")
        logger.info(f"Tables: {', '.join(sorted(existing_tables))}")
        
        # Print record counts
        db = SessionLocal()
        try:
            user_count = db.query(User).count()
            reading_count = db.query(SensorReading).count()
            pest_count = db.query(PestDetection).count()
            alert_count = db.query(Alert).count()
            
            logger.info(f"Records: {user_count} users, {reading_count} readings, "
                       f"{pest_count} pests, {alert_count} alerts")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False


# Export main function
__all__ = ["initialize_database"]
