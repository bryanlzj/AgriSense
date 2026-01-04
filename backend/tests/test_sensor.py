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

from models.sensor_data import SensorData


class TestCreateSensorData:
    """Test creating sensor data."""
    
    def test_create_sensor_data_success(self, client: TestClient, auth_headers: dict, test_user):
        """Test successful sensor data creation."""
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "humidity": 70.0,
                "soil_moisture": 50.0,
                "rainfall": 5.2
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["temperature"] == 28.5
        assert data["humidity"] == 70.0
        assert data["soil_moisture"] == 50.0
        assert data["rainfall"] == 5.2
        assert data["user_id"] == test_user.id
        assert "id" in data
        assert "created_at" in data
    
    def test_create_sensor_data_no_auth(self, client: TestClient):
        """Test creating sensor data without authentication fails."""
        response = client.post(
            "/api/v1/sensor/",
            json={
                "temperature": 28.5,
                "humidity": 70.0,
                "soil_moisture": 50.0,
                "rainfall": 5.2
            }
        )
        
        assert response.status_code == 401
    
    def test_create_sensor_data_invalid_values(self, client: TestClient, auth_headers: dict):
        """Test creating sensor data with invalid values fails."""
        # Negative humidity
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "humidity": -10.0,
                "soil_moisture": 50.0,
                "rainfall": 5.2
            }
        )
        assert response.status_code == 422
        
        # Humidity > 100
        response = client.post(
            "/api/v1/sensor/",
            headers=auth_headers,
            json={
                "temperature": 28.5,
                "humidity": 150.0,
                "soil_moisture": 50.0,
                "rainfall": 5.2
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
            sensor = SensorData(
                user_id=test_user.id,
                temperature=20.0 + i,
                humidity=60.0,
                soil_moisture=40.0,
                rainfall=0.0
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
            sensor = SensorData(
                user_id=test_user.id,
                temperature=temp,
                humidity=60.0,
                soil_moisture=40.0,
                rainfall=0.0
            )
            db.add(sensor)
        db.commit()
        
        # Filter for temperature between 20 and 30
        response = client.get(
            "/api/v1/sensor/?min_temp=20&max_temp=30",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["temperature"] == 25.0
    
    def test_list_sensor_data_no_auth(self, client: TestClient):
        """Test listing sensor data without authentication fails."""
        response = client.get("/api/v1/sensor/")
        assert response.status_code == 401


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
                "humidity": 75.0,
                "soil_moisture": 55.0,
                "rainfall": 10.0
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["temperature"] == 30.0
        assert data["humidity"] == 75.0
    
    def test_update_sensor_data_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent sensor data fails."""
        response = client.put(
            "/api/v1/sensor/99999",
            headers=auth_headers,
            json={
                "temperature": 30.0,
                "humidity": 75.0,
                "soil_moisture": 55.0,
                "rainfall": 10.0
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
        
        assert response.status_code == 200
        assert response.json()["message"] == "Sensor data deleted successfully"
        
        # Verify deletion
        sensor = db.query(SensorData).filter(SensorData.id == test_sensor_data.id).first()
        assert sensor is None
    
    def test_delete_sensor_data_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent sensor data fails."""
        response = client.delete("/api/v1/sensor/99999", headers=auth_headers)
        assert response.status_code == 404


class TestSensorStatistics:
    """Test sensor statistics endpoint."""
    
    def test_get_statistics(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test getting sensor statistics."""
        # Create multiple sensor data entries
        for temp in [20.0, 25.0, 30.0]:
            sensor = SensorData(
                user_id=test_user.id,
                temperature=temp,
                humidity=60.0,
                soil_moisture=40.0,
                rainfall=5.0
            )
            db.add(sensor)
        db.commit()
        
        response = client.get("/api/v1/sensor/stats/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "avg_temperature" in data
        assert "min_temperature" in data
        assert "max_temperature" in data
        assert data["avg_temperature"] == 25.0
        assert data["min_temperature"] == 20.0
        assert data["max_temperature"] == 30.0
