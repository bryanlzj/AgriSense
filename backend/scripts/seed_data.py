"""
Seed Data Script for AgriSense Database

This script populates the database with initial test data for development and testing.
It creates:
- Test users (admin and regular users)
- Historical sensor readings (7 days of data)
- Sample pest detections
- Sample alerts

This is useful for:
- Testing the API without manually creating data
- Demonstrating the system with realistic data
- Developing the mobile app with pre-populated data
- Learning how the database models work together

Usage:
    python scripts/seed_data.py

Note: This script will clear existing data before seeding!
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path so we can import from backend modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import User, SensorReading, PestDetection, Alert
from models.pest_detection import PestSeverity
from models.alert import AlertType, AlertSeverity
from utils.password import get_password_hash
from utils.data_simulator import SensorDataSimulator


def clear_database(db: Session):
    """
    Clear all existing data from the database.
    
    This is useful for starting fresh during development.
    In production, you would NEVER do this!
    
    Args:
        db: Database session
    """
    print("🗑️  Clearing existing data...")
    
    # Delete in reverse order of dependencies (children first, parents last)
    db.query(Alert).delete()
    db.query(PestDetection).delete()
    db.query(SensorReading).delete()
    db.query(User).delete()
    
    db.commit()
    print("✅ Database cleared")


def create_users(db: Session) -> list[User]:
    """
    Create test users with different roles.
    
    Creates:
    - Admin user (for testing admin features)
    - Regular user (typical farmer)
    - Another regular user (for testing multi-user scenarios)
    
    Args:
        db: Database session
        
    Returns:
        List of created User objects
    """
    print("\n👥 Creating users...")
    
    users = [
        User(
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="Admin User",
            phone_number="+254700000000",
            farm_location="Nairobi, Kenya"
        ),
        User(
            username="farmer1",
            hashed_password=get_password_hash("password123"),
            full_name="John Kamau",
            phone_number="+254712345678",
            farm_location="Kiambu County, Kenya"
        ),
        User(
            username="farmer2",
            hashed_password=get_password_hash("password123"),
            full_name="Mary Wanjiku",
            phone_number="+254723456789",
            farm_location="Nakuru County, Kenya"
        ),
    ]
    
    for user in users:
        db.add(user)
    
    db.commit()
    
    # Refresh to get IDs
    for user in users:
        db.refresh(user)
    
    print(f"✅ Created {len(users)} users")
    for user in users:
        print(f"   - {user.username} (ID: {user.id})")
    
    return users


def create_sensor_readings(db: Session, user: User, days: int = 7):
    """
    Create historical sensor readings for a user.
    
    Generates realistic sensor data for the past N days:
    - Temperature (20-35°C)
    - Humidity (40-90%)
    - Soil moisture (20-80%)
    - Light intensity (0-100000 lux)
    
    Creates 24 readings per day (one per hour) to show daily patterns.
    
    Args:
        db: Database session
        user: User to create readings for
        days: Number of days of historical data to generate
    """
    print(f"\n📊 Creating sensor readings for {user.username}...")
    
    simulator = SensorDataSimulator()
    
    # Generate historical data (24 readings per day = hourly)
    historical_data = simulator.generate_historical_data(
        days=days,
        readings_per_day=24
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
        db.add(reading)
    
    db.commit()
    
    print(f"✅ Created {len(readings)} sensor readings")
    print(f"   - Date range: {readings[0].timestamp} to {readings[-1].timestamp}")


def create_pest_detections(db: Session, user: User):
    """
    Create sample pest detections.
    
    Creates a few pest detections with different severities and confidence levels.
    This demonstrates the pest detection feature without needing actual images.
    
    Args:
        db: Database session
        user: User to create detections for
    """
    print(f"\n🐛 Creating pest detections for {user.username}...")
    
    # Sample pest detections with different scenarios
    detections = [
        PestDetection(
            user_id=user.id,
            image_path="/uploads/pest_001.jpg",
            pest_name="Fall Armyworm",
            confidence=0.92,
            severity=PestSeverity.HIGH,
            recommendations="1. Apply Bt-based insecticide\n2. Scout fields daily\n3. Remove affected plants\n4. Consider trap crops",
            detected_at=datetime.utcnow() - timedelta(days=2)
        ),
        PestDetection(
            user_id=user.id,
            image_path="/uploads/pest_002.jpg",
            pest_name="Aphids",
            confidence=0.85,
            severity=PestSeverity.MEDIUM,
            recommendations="1. Spray with neem oil\n2. Introduce ladybugs (natural predator)\n3. Remove heavily infested leaves\n4. Monitor weekly",
            detected_at=datetime.utcnow() - timedelta(days=5)
        ),
        PestDetection(
            user_id=user.id,
            image_path="/uploads/pest_003.jpg",
            pest_name="Whitefly",
            confidence=0.78,
            severity=PestSeverity.LOW,
            recommendations="1. Use yellow sticky traps\n2. Spray with insecticidal soap\n3. Maintain good air circulation\n4. Monitor population",
            detected_at=datetime.utcnow() - timedelta(days=7)
        ),
    ]
    
    for detection in detections:
        db.add(detection)
    
    db.commit()
    
    # Refresh to get IDs
    for detection in detections:
        db.refresh(detection)
    
    print(f"✅ Created {len(detections)} pest detections")
    for detection in detections:
        print(f"   - {detection.pest_name} ({detection.severity.value}, {detection.confidence:.0%} confidence)")


def create_alerts(db: Session, user: User):
    """
    Create sample alerts for different scenarios.
    
    Creates alerts for:
    - Weather warnings (heavy rain, extreme heat)
    - Pest risks (based on detections)
    - Environmental conditions (low soil moisture)
    
    Args:
        db: Database session
        user: User to create alerts for
    """
    print(f"\n🔔 Creating alerts for {user.username}...")
    
    alerts = [
        # Weather alert - Heavy rain warning
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
        
        # Pest alert - High confidence detection
        Alert(
            user_id=user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.CRITICAL,
            title="Fall Armyworm Detected",
            message="Fall Armyworm detected with 92% confidence. Immediate action required to prevent crop damage.",
            recommendations="1. Apply Bt-based insecticide immediately\n2. Scout all fields\n3. Remove affected plants\n4. Monitor daily",
            is_read=False,
            created_at=datetime.utcnow() - timedelta(days=2)
        ),
        
        # Environmental alert - Low soil moisture
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
        
        # Weather alert - Extreme heat
        Alert(
            user_id=user.id,
            alert_type=AlertType.EXTREME_HEAT,
            severity=AlertSeverity.HIGH,
            title="Extreme Heat Warning",
            message="Temperatures expected to reach 38°C tomorrow. Protect crops from heat stress.",
            recommendations="1. Irrigate early morning or evening\n2. Provide shade for sensitive crops\n3. Avoid fertilizer application\n4. Monitor for wilting",
            is_read=False,
            created_at=datetime.utcnow() - timedelta(hours=6)
        ),
    ]
    
    for alert in alerts:
        db.add(alert)
    
    db.commit()
    
    # Refresh to get IDs
    for alert in alerts:
        db.refresh(alert)
    
    print(f"✅ Created {len(alerts)} alerts")
    
    # Count unread alerts
    unread_count = sum(1 for alert in alerts if not alert.is_read)
    print(f"   - {unread_count} unread alerts")
    print(f"   - {len(alerts) - unread_count} read alerts")


def seed_database():
    """
    Main function to seed the database with test data.
    
    This function:
    1. Clears existing data
    2. Creates test users
    3. Creates sensor readings for each user
    4. Creates pest detections for each user
    5. Creates alerts for each user
    
    After running this script, you'll have a fully populated database
    ready for testing and development.
    """
    print("=" * 60)
    print("🌱 AgriSense Database Seeding Script")
    print("=" * 60)
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Step 1: Clear existing data
        clear_database(db)
        
        # Step 2: Create users
        users = create_users(db)
        
        # Step 3: Create data for each user
        for user in users:
            # Create 7 days of sensor readings (hourly)
            create_sensor_readings(db, user, days=7)
            
            # Create pest detections
            create_pest_detections(db, user)
            
            # Create alerts
            create_alerts(db, user)
        
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        
        print("\n📝 Test Credentials:")
        print("   Admin:   username='admin',   password='admin123'")
        print("   Farmer1: username='farmer1', password='password123'")
        print("   Farmer2: username='farmer2', password='password123'")
        
        print("\n📊 Data Summary:")
        print(f"   - Users: {db.query(User).count()}")
        print(f"   - Sensor Readings: {db.query(SensorReading).count()}")
        print(f"   - Pest Detections: {db.query(PestDetection).count()}")
        print(f"   - Alerts: {db.query(Alert).count()}")
        
    except Exception as e:
        print(f"\n❌ Error seeding database: {e}")
        db.rollback()
        raise
    
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
