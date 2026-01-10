"""
Pytest configuration and fixtures for testing.

This file provides shared fixtures for all tests including:
- Test database setup/teardown
- Test client for API requests
- Authentication fixtures
- Sample data fixtures
"""

import os
import sys
from pathlib import Path
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Add parent directory to path to allow imports
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from database import Base, get_db
from main import app
from models.user import User
from models.sensor_reading import SensorReading
from models.pest_detection import PestDetection
from models.alert import Alert
from utils.password import get_password_hash
from utils.security import create_access_token

# Use PostgreSQL for testing - defaults to main agrisense database
# Set TEST_DATABASE_URL environment variable to override
# Password matches root .env: strongpassword
SQLALCHEMY_TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://agrisense_user:strongpassword@localhost:5432/agrisense"
)

# Create test engine
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    pool_pre_ping=True
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Provide a database session for each test with transaction rollback.

    This fixture:
    1. Ensures tables exist (creates if missing)
    2. Starts a transaction
    3. Yields a database session
    4. Rolls back the transaction (test data is discarded)

    Benefits:
    - Existing tables and data are preserved
    - Each test is isolated (changes rolled back)
    - Fast (no drop/create overhead)
    """
    # Ensure tables exist (won't recreate if they already exist)
    Base.metadata.create_all(bind=engine)

    # Start a connection and transaction
    connection = engine.connect()
    transaction = connection.begin()

    # Create session bound to this connection
    db_session = TestingSessionLocal(bind=connection)

    try:
        yield db_session
    finally:
        db_session.close()
        # Rollback transaction - all test changes are discarded
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with overridden database dependency.
    
    This fixture:
    1. Overrides the get_db dependency to use test database
    2. Creates a TestClient for making API requests
    3. Yields the client for testing
    
    Usage:
        def test_example(client):
            response = client.get("/api/v1/endpoint")
            assert response.status_code == 200
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user(db: Session) -> User:
    """
    Create a test user in the database.

    Returns:
        User object with:
        - username: "testuser"
        - password: "testpassword123" (hashed)
        - full_name: "Test User"
        - farm_location_name: "Kedah"
        - farm_location_lat: 6.1184
        - farm_location_lng: 100.3685
        - crop_type: "rice"

    Usage:
        def test_example(test_user):
            assert test_user.username == "testuser"
    """
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        farm_location_name="Kedah",
        farm_location_lat=6.1184,
        farm_location_lng=100.3685,
        crop_type="rice"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_token(test_user: User) -> str:
    """
    Create a JWT token for the test user.
    
    Returns:
        JWT token string that can be used in Authorization headers
    
    Usage:
        def test_protected_endpoint(client, test_user_token):
            response = client.get(
                "/api/v1/protected",
                headers={"Authorization": f"Bearer {test_user_token}"}
            )
            assert response.status_code == 200
    """
    return create_access_token(data={"sub": test_user.username})


@pytest.fixture(scope="function")
def auth_headers(test_user_token: str) -> dict:
    """
    Create authorization headers with test user token.
    
    Returns:
        Dictionary with Authorization header
    
    Usage:
        def test_protected_endpoint(client, auth_headers):
            response = client.get("/api/v1/protected", headers=auth_headers)
            assert response.status_code == 200
    """
    return {"Authorization": f"Bearer {test_user_token}"}


@pytest.fixture(scope="function")
def test_sensor_data(db: Session, test_user: User) -> SensorReading:
    """
    Create sample sensor data for testing.
    
    Returns:
        SensorReading object with realistic values
    """
    sensor_data = SensorReading(
        user_id=test_user.id,
        temperature=25.5,
        humidity=65.0,
        soil_moisture=45.0,
        light_intensity=50000.0
    )
    db.add(sensor_data)
    db.commit()
    db.refresh(sensor_data)
    return sensor_data


@pytest.fixture(scope="function")
def test_pest_detection(db: Session, test_user: User) -> PestDetection:
    """
    Create sample pest detection for testing.
    
    Returns:
        PestDetection object with mock data
    """
    from models.pest_detection import SeverityLevel

    pest = PestDetection(
        user_id=test_user.id,
        image_url="uploads/test_image.jpg",
        pest_type="Aphid",
        confidence_score=0.85,
        severity_level=SeverityLevel.MEDIUM,
        recommendations="Apply neem oil spray"
    )
    db.add(pest)
    db.commit()
    db.refresh(pest)
    return pest


@pytest.fixture(scope="function")
def test_alert(db: Session, test_user: User) -> Alert:
    """
    Create sample alert for testing.

    Returns:
        Alert object with test data
    """
    from models.alert import AlertType, AlertSeverity

    alert = Alert(
        user_id=test_user.id,
        alert_type=AlertType.PEST_RISK,
        severity=AlertSeverity.MEDIUM,
        title="High Temperature Alert",
        message="Temperature exceeds 32°C",
        is_read=False,
        is_acknowledged=False,
        recommendations="Increase irrigation, provide shade for crops"
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


@pytest.fixture(scope="function")
def test_pest_weather_correlation(db: Session):
    """
    Create sample pest-weather correlation for testing.

    Returns:
        PestWeatherCorrelation object with test data
    """
    from models.pest_weather_correlation import PestWeatherCorrelation

    correlation = PestWeatherCorrelation(
        pest_name="Rice Stem Borer",
        affected_crops=["rice"],
        risk_conditions={
            "temp_min": 25,
            "temp_max": 35,
            "humidity_min": 70,
            "humidity_max": 95,
            "trigger": "after_rain"
        },
        risk_level="high",
        risk_message="Warm, humid conditions following recent rain increase stem borer activity.",
        prevention_tips=[
            "Monitor stems for entry holes",
            "Apply biological control (Trichogramma)",
            "Avoid excessive nitrogen fertilization"
        ],
        data_source="MARDI Research"
    )
    db.add(correlation)
    db.commit()
    db.refresh(correlation)
    return correlation


# Environment variable fixtures
@pytest.fixture(scope="session", autouse=True)
def set_test_env():
    """
    Set test environment variables.
    
    This fixture runs once per test session and sets up
    environment variables needed for testing.
    """
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only"
    os.environ["DATABASE_URL"] = SQLALCHEMY_TEST_DATABASE_URL
