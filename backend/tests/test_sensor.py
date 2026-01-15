"""
Tests for sensor data endpoints.

Tests:
- Create sensor data
- List sensor data with filtering
- Get specific sensor data
- Update sensor data
- Delete sensor data
- Statistics endpoint
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from models.sensor_reading import SensorReading


class TestCreateSensorData:
    """Test creating sensor data."""
    
    def test_create_sensor_data_success(self, client: TestClient, auth_headers: dict, test_user):
        """Test successful sensor data creation with Open-Meteo aligned fields."""
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "relative_humidity": 70.0,
                "rain": 0.5,
                "wind_speed": 15.0,
                "solar_radiation": 500.0,
                "soil_temperature": 26.0,
                "soil_moisture": 0.35,  # Volumetric m³/m³
                "weather_code": 1
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["temperature"] == 28.5
        assert data["relative_humidity"] == 70.0
        assert data["rain"] == 0.5
        assert data["wind_speed"] == 15.0
        assert data["solar_radiation"] == 500.0
        assert data["soil_temperature"] == 26.0
        assert data["soil_moisture"] == 0.35
        assert data["weather_code"] == 1
        assert data["user_id"] == test_user.id
        assert "id" in data
        assert "timestamp" in data
    
    def test_create_sensor_data_no_auth(self, client: TestClient):
        """Test creating sensor data without authentication fails."""
        response = client.post(
            "/api/v1/sensor/",
            json={
                "temperature": 28.5,
                "relative_humidity": 70.0,
                "rain": 0.0,
                "wind_speed": 10.0,
                "soil_moisture": 0.35
            }
        )

        assert response.status_code == 403

    def test_create_sensor_data_invalid_values(self, client: TestClient, auth_headers: dict):
        """Test creating sensor data with invalid values fails."""
        # Negative relative_humidity
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "relative_humidity": -10.0,
                "rain": 0.0,
                "wind_speed": 10.0,
                "soil_moisture": 0.35
            }
        )
        assert response.status_code == 422

        # relative_humidity > 100
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "relative_humidity": 150.0,
                "rain": 0.0,
                "wind_speed": 10.0,
                "soil_moisture": 0.35
            }
        )
        assert response.status_code == 422

        # soil_moisture > 1.0 (invalid for volumetric m³/m³)
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "relative_humidity": 70.0,
                "rain": 0.0,
                "wind_speed": 10.0,
                "soil_moisture": 1.5
            }
        )
        assert response.status_code == 422


class TestListSensorData:
    """Test listing sensor data."""
    
    def test_list_sensor_data(self, client: TestClient, auth_headers: dict, test_sensor_data):
        """Test listing sensor data returns user's data."""
        response = client.get("/api/v1/sensor/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["id"] == test_sensor_data.id
    
    def test_list_sensor_data_pagination(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test pagination works correctly."""
        # Create multiple sensor data entries
        for i in range(5):
            sensor = SensorReading(
                user_id=test_user.id,
                temperature=20.0 + i,
                relative_humidity=60.0,
                rain=0.0,
                wind_speed=10.0,
                soil_moisture=0.35
            )
            db.add(sensor)
        db.commit()

        # Get first 2
        response = client.get("/api/v1/sensor/?skip=0&limit=2", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

        # Get next 2
        response = client.get("/api/v1/sensor/?skip=2&limit=2", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_sensor_data_temperature_filter(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test filtering by temperature range."""
        # Create sensor data with different temperatures
        for temp in [15.0, 25.0, 35.0]:
            sensor = SensorReading(
                user_id=test_user.id,
                temperature=temp,
                relative_humidity=60.0,
                rain=0.0,
                wind_speed=10.0,
                soil_moisture=0.35
            )
            db.add(sensor)
        db.commit()

        # Filter for temperature between 20 and 30
        response = client.get(
            "/api/v1/sensor/?min_temperature=20&max_temperature=30",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["temperature"] == 25.0
    
    def test_list_sensor_data_no_auth(self, client: TestClient):
        """Test listing sensor data without authentication fails."""
        response = client.get("/api/v1/sensor/")
        assert response.status_code == 403


class TestGetSensorData:
    """Test getting specific sensor data."""
    
    def test_get_sensor_data_success(self, client: TestClient, auth_headers: dict, test_sensor_data):
        """Test getting specific sensor data."""
        response = client.get(
            f"/api/v1/sensor/{test_sensor_data.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_sensor_data.id
        assert data["temperature"] == test_sensor_data.temperature
    
    def test_get_sensor_data_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent sensor data fails."""
        response = client.get("/api/v1/sensor/99999", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateSensorData:
    """Test updating sensor data."""
    
    def test_update_sensor_data_success(self, client: TestClient, auth_headers: dict, test_sensor_data):
        """Test successful sensor data update."""
        response = client.put(
            f"/api/v1/sensor/{test_sensor_data.id}",
            headers=auth_headers,
            json={
                "temperature": 30.0,
                "relative_humidity": 75.0,
                "rain": 2.5,
                "wind_speed": 20.0,
                "soil_moisture": 0.40
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert data["temperature"] == 30.0
        assert data["relative_humidity"] == 75.0
        assert data["rain"] == 2.5
        assert data["wind_speed"] == 20.0
        assert data["soil_moisture"] == 0.40

    def test_update_sensor_data_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent sensor data fails."""
        response = client.put(
            "/api/v1/sensor/99999",
            headers=auth_headers,
            json={
                "temperature": 30.0,
                "relative_humidity": 75.0,
                "rain": 0.0,
                "wind_speed": 10.0,
                "soil_moisture": 0.35
            }
        )
        assert response.status_code == 404


class TestDeleteSensorData:
    """Test deleting sensor data."""
    
    def test_delete_sensor_data_success(self, client: TestClient, auth_headers: dict, test_sensor_data, db: Session):
        """Test successful sensor data deletion."""
        response = client.delete(
            f"/api/v1/sensor/{test_sensor_data.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        # 204 No Content responses don't have a body
        
        # Verify deletion
        sensor = db.query(SensorReading).filter(SensorReading.id == test_sensor_data.id).first()
        assert sensor is None
    
    def test_delete_sensor_data_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent sensor data fails."""
        response = client.delete("/api/v1/sensor/99999", headers=auth_headers)
        assert response.status_code == 404


class TestSensorStatistics:
    """Test sensor statistics endpoint."""

    def test_get_statistics(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test getting sensor statistics with Open-Meteo aligned fields."""
        # Create multiple sensor data entries
        for temp in [20.0, 25.0, 30.0]:
            sensor = SensorReading(
                user_id=test_user.id,
                temperature=temp,
                relative_humidity=60.0,
                rain=1.0,
                wind_speed=15.0,
                solar_radiation=400.0,
                soil_temperature=24.0,
                soil_moisture=0.35
            )
            db.add(sensor)
        db.commit()

        response = client.get("/api/v1/sensor/stats/summary", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        # Check all Open-Meteo aligned fields
        assert "temperature" in data
        assert "relative_humidity" in data
        assert "rain" in data
        assert "wind_speed" in data
        assert "solar_radiation" in data
        assert "soil_temperature" in data
        assert "soil_moisture" in data
        # Verify temperature statistics
        assert data["temperature"]["average"] == 25.0
        assert data["temperature"]["minimum"] == 20.0
        assert data["temperature"]["maximum"] == 30.0
