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

# Use in-memory SQLite for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with special settings for SQLite
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # Use static pool for in-memory database
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db() -> Generator[Session, None, None]:
    """
    Create a fresh database for each test.
    
    This fixture:
    1. Creates all tables
    2. Yields a database session
    3. Drops all tables after the test
    
    Scope: function (new database for each test)
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db_session = TestingSessionLocal()
    
    try:
        yield db_session
    finally:
        db_session.close()
        # Drop all tables
        Base.metadata.drop_all(bind=engine)


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
    
    Usage:
        def test_example(test_user):
            assert test_user.username == "testuser"
    """
    user = User(
        username="testuser",
        hashed_password=get_password_hash("testpassword123")
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
        rainfall=0.0
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
    pest = PestDetection(
        user_id=test_user.id,
        image_path="uploads/test_image.jpg",
        pest_type="Aphid",
        confidence=0.85,
        severity="medium",
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
    alert = Alert(
        user_id=test_user.id,
        type="sensor",
        severity="warning",
        title="High Temperature Alert",
        message="Temperature exceeds 32°C",
        is_read=False,
        is_acknowledged=False
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


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
