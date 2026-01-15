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
from models.pest_weather_correlation import PestWeatherCorrelation
from models.weather_cache import WeatherCache

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
        
        # Create test users (PRD v2 format with Malaysian locations)
        users_data = [
            {
                "username": "admin",
                "password": "admin123",
                "full_name": "Admin User",
                "farm_location_name": "Kuala Lumpur",
                "farm_location_lat": 3.1390,
                "farm_location_lng": 101.6869,
                "crop_type": "rice",
                "is_active": True
            },
            {
                "username": "ahmad",
                "password": "password123",
                "full_name": "Ahmad bin Ibrahim",
                "farm_location_name": "Kedah",
                "farm_location_lat": 6.1184,
                "farm_location_lng": 100.3685,
                "crop_type": "rice",
                "is_active": True
            },
            {
                "username": "mei_ling",
                "password": "password123",
                "full_name": "Tan Mei Ling",
                "farm_location_name": "Johor",
                "farm_location_lat": 1.4854,
                "farm_location_lng": 103.7618,
                "crop_type": "vegetables",
                "is_active": True
            },
            {
                "username": "raj",
                "password": "password123",
                "full_name": "Raj Kumar",
                "farm_location_name": "Perak",
                "farm_location_lat": 4.5921,
                "farm_location_lng": 101.0901,
                "crop_type": "oil_palm",
                "is_active": True
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
        # Fields aligned with Open-Meteo API parameters
        sensor_readings = []
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=7)

        # WMO weather codes for random selection (simplified for Malaysian agriculture)
        weather_codes = [0, 1, 2, 3, 51, 53, 55, 61, 63, 65]

        for user in created_users:
            current_time = start_time
            while current_time <= end_time:
                reading = SensorReading(
                    user_id=user.id,
                    temperature=round(random.uniform(22, 32), 1),
                    relative_humidity=round(random.uniform(50, 85), 1),
                    rain=round(random.uniform(0, 5), 1) if random.random() < 0.2 else 0.0,
                    wind_speed=round(random.uniform(5, 30), 1),
                    solar_radiation=round(random.uniform(0, 800), 1) if 6 <= current_time.hour <= 18 else 0.0,
                    soil_temperature=round(random.uniform(24, 30), 1),
                    soil_moisture=round(random.uniform(0.2, 0.45), 4),
                    weather_code=random.choice(weather_codes),
                    timestamp=current_time
                )
                sensor_readings.append(reading)
                current_time += timedelta(hours=1)

        db.bulk_save_objects(sensor_readings)
        db.commit()
        logger.info(f"✓ Created {len(sensor_readings)} sensor readings")
        
        # Create pest detections
        pest_types = ["Brown Planthopper", "Rice Leaf Roller", "Stem Borer", "Rice Bug", "Green Leafhopper"]
        pest_detections = []

        for user in created_users:
            for i in range(3):
                detection = PestDetection(
                    user_id=user.id,
                    pest_type=random.choice(pest_types),
                    confidence_score=round(random.uniform(0.75, 0.98), 2),
                    severity_level=random.choice(["low", "medium", "high"]),
                    image_path=f"/uploads/pest_{user.id}_{i}.jpg",
                    location=user.farm_location_name,
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

        # Create pest-weather correlations (reference data for risk prediction)
        existing_correlations = db.query(PestWeatherCorrelation).count()
        if existing_correlations == 0:
            correlations_data = [
                {
                    "pest_name": "Rice Stem Borer",
                    "scientific_name": "Scirpophaga incertulas",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"temp_min": 25, "temp_max": 35, "humidity_min": 70, "trigger": "after_rain"},
                    "risk_level": "high",
                    "risk_message": "Stem Borer activity increases in warm, humid conditions following rainfall. Moths lay eggs on leaves, larvae bore into stems.",
                    "prevention_tips": [
                        "Monitor rice stems for entry holes and frass",
                        "Apply Trichogramma biological control",
                        "Remove and destroy infected stems",
                        "Avoid excessive nitrogen fertilizer"
                    ],
                    "data_source": "MARDI Pest Management Guidelines"
                },
                {
                    "pest_name": "Rice Leaf Folder",
                    "scientific_name": "Cnaphalocrocis medinalis",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"temp_min": 25, "temp_max": 30, "humidity_min": 60, "humidity_max": 80, "condition": "cloudy"},
                    "risk_level": "medium",
                    "risk_message": "Leaf Folder larvae fold leaves and feed inside. Common during cloudy, humid weather.",
                    "prevention_tips": [
                        "Scout for folded leaves with larvae inside",
                        "Maintain field hygiene",
                        "Avoid dense planting",
                        "Apply neem-based spray if >10% damage"
                    ],
                    "data_source": "MARDI Pest Management Guidelines"
                },
                {
                    "pest_name": "Brown Planthopper",
                    "scientific_name": "Nilaparvata lugens",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"humidity_min": 85, "temp_min": 25, "temp_max": 30},
                    "risk_level": "high",
                    "risk_message": "Brown Planthopper thrives in high humidity with dense crop canopy. Can cause hopper burn.",
                    "prevention_tips": [
                        "Avoid excessive nitrogen application",
                        "Maintain proper plant spacing",
                        "Drain fields periodically",
                        "Use resistant varieties if available"
                    ],
                    "data_source": "IRRI Rice Knowledge Bank"
                },
                {
                    "pest_name": "Rice Bug",
                    "scientific_name": "Leptocorisa oratorius",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"humidity_max": 70, "trigger": "dry_period", "stage": "grain_filling"},
                    "risk_level": "medium",
                    "risk_message": "Rice bugs attack during grain filling stage, especially in dry periods. Cause empty or discolored grains.",
                    "prevention_tips": [
                        "Monitor during flowering and grain filling",
                        "Remove weeds around field",
                        "Early morning collection when bugs are sluggish",
                        "Apply insecticide if >5 bugs per hill"
                    ],
                    "data_source": "Philippine Rice Research Institute"
                },
                {
                    "pest_name": "Rice Blast",
                    "scientific_name": "Magnaporthe oryzae",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"humidity_min": 90, "humidity_sustained_hours": 48, "temp_min": 24, "temp_max": 28},
                    "risk_level": "high",
                    "risk_message": "Fungal disease favored by prolonged high humidity and moderate temperatures. Causes lesions on leaves and neck rot.",
                    "prevention_tips": [
                        "Use certified disease-free seeds",
                        "Apply fungicide preventively in high-risk conditions",
                        "Avoid excessive nitrogen",
                        "Ensure good field drainage"
                    ],
                    "data_source": "IRRI Rice Knowledge Bank"
                },
                {
                    "pest_name": "Bacterial Leaf Blight",
                    "scientific_name": "Xanthomonas oryzae",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"trigger": "after_heavy_rain", "humidity_min": 80, "condition": "flooding"},
                    "risk_level": "high",
                    "risk_message": "Bacterial disease spreads rapidly after heavy rain and flooding. Causes yellowing leaf margins.",
                    "prevention_tips": [
                        "Avoid field flooding",
                        "Ensure proper drainage",
                        "Remove infected plant debris",
                        "Use resistant varieties"
                    ],
                    "data_source": "MARDI Pest Management Guidelines"
                },
                {
                    "pest_name": "Sheath Blight",
                    "scientific_name": "Rhizoctonia solani",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"humidity_min": 85, "temp_min": 28, "temp_max": 32},
                    "risk_level": "medium",
                    "risk_message": "Fungal disease common in dense plantings with high humidity. Causes oval lesions on leaf sheaths.",
                    "prevention_tips": [
                        "Maintain proper plant spacing",
                        "Avoid excessive nitrogen",
                        "Remove crop residue after harvest",
                        "Apply fungicide if lesions spread"
                    ],
                    "data_source": "IRRI Rice Knowledge Bank"
                },
                {
                    "pest_name": "Green Leafhopper",
                    "scientific_name": "Nephotettix virescens",
                    "affected_crops": ["rice"],
                    "risk_conditions": {"temp_min": 25, "temp_max": 32, "humidity_min": 70},
                    "risk_level": "medium",
                    "risk_message": "Vector for tungro virus disease. Common in warm, humid conditions.",
                    "prevention_tips": [
                        "Monitor for hopper populations",
                        "Remove infected plants immediately",
                        "Synchronize planting in area",
                        "Use resistant varieties"
                    ],
                    "data_source": "Philippine Rice Research Institute"
                }
            ]

            correlations = [PestWeatherCorrelation(**data) for data in correlations_data]
            db.bulk_save_objects(correlations)
            db.commit()
            logger.info(f"✓ Created {len(correlations)} pest-weather correlations")
        else:
            logger.info(f"✓ Pest-weather correlations already exist ({existing_correlations}) - skipping")

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
            correlation_count = db.query(PestWeatherCorrelation).count()

            logger.info(f"Records: {user_count} users, {reading_count} readings, "
                       f"{pest_count} pests, {alert_count} alerts, {correlation_count} correlations")
        finally:
            db.close()
        
        return True
        
    except Exception as e:
        logger.error(f"✗ Database initialization failed: {e}")
        return False


# Export main function
__all__ = ["initialize_database"]
