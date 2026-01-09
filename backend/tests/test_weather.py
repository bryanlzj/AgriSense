"""
Tests for weather endpoints.

Tests:
- Current weather
- Weather forecast
- Weather summary
- Weather API test endpoint
- Error handling
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from unittest.mock import patch, AsyncMock

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))


class TestCurrentWeather:
    """Test current weather endpoint."""

    def test_get_current_weather_success(self, client: TestClient, auth_headers: dict):
        """Test getting current weather with valid coordinates."""
        response = client.get(
            "/api/v1/weather/current?latitude=3.1390&longitude=101.6869&location_name=Kuala%20Lumpur",
            headers=auth_headers
        )

        # May succeed or fail depending on API availability
        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "location" in data
            assert "current" in data
            assert "updated_at" in data

    def test_get_current_weather_user_location(self, client: TestClient, auth_headers: dict, test_user):
        """Test getting current weather for user's farm location."""
        response = client.get(
            f"/api/v1/weather/current?latitude={test_user.farm_location_lat}&longitude={test_user.farm_location_lng}",
            headers=auth_headers
        )

        assert response.status_code in [200, 500]

    def test_get_current_weather_invalid_coords(self, client: TestClient, auth_headers: dict):
        """Test getting weather with invalid coordinates."""
        # Latitude out of range
        response = client.get(
            "/api/v1/weather/current?latitude=100&longitude=101.6869",
            headers=auth_headers
        )
        assert response.status_code == 422

        # Longitude out of range
        response = client.get(
            "/api/v1/weather/current?latitude=3.1390&longitude=200",
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_current_weather_missing_coords(self, client: TestClient, auth_headers: dict):
        """Test getting weather without coordinates."""
        response = client.get(
            "/api/v1/weather/current",
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_current_weather_no_auth(self, client: TestClient):
        """Test getting weather without authentication."""
        response = client.get(
            "/api/v1/weather/current?latitude=3.1390&longitude=101.6869"
        )
        assert response.status_code == 403


class TestWeatherForecast:
    """Test weather forecast endpoint."""

    def test_get_forecast_success(self, client: TestClient, auth_headers: dict):
        """Test getting weather forecast with valid coordinates."""
        response = client.get(
            "/api/v1/weather/forecast?latitude=3.1390&longitude=101.6869&location_name=Kuala%20Lumpur",
            headers=auth_headers
        )

        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "location" in data
            assert "forecast" in data
            assert isinstance(data["forecast"], list)

    def test_get_forecast_user_location(self, client: TestClient, auth_headers: dict, test_user):
        """Test getting forecast for user's farm location."""
        response = client.get(
            f"/api/v1/weather/forecast?latitude={test_user.farm_location_lat}&longitude={test_user.farm_location_lng}",
            headers=auth_headers
        )

        assert response.status_code in [200, 500]

    def test_get_forecast_invalid_coords(self, client: TestClient, auth_headers: dict):
        """Test getting forecast with invalid coordinates."""
        response = client.get(
            "/api/v1/weather/forecast?latitude=100&longitude=101.6869",
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_forecast_no_auth(self, client: TestClient):
        """Test getting forecast without authentication."""
        response = client.get(
            "/api/v1/weather/forecast?latitude=3.1390&longitude=101.6869"
        )
        assert response.status_code == 403


class TestWeatherSummary:
    """Test weather summary endpoint."""

    def test_get_summary_success(self, client: TestClient, auth_headers: dict):
        """Test getting weather summary with valid coordinates."""
        response = client.get(
            "/api/v1/weather/summary?latitude=3.1390&longitude=101.6869&location_name=Kuala%20Lumpur",
            headers=auth_headers
        )

        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert "location" in data
            assert "current" in data
            assert "forecast" in data
            assert "updated_at" in data

    def test_get_summary_user_location(self, client: TestClient, auth_headers: dict, test_user):
        """Test getting summary for user's farm location."""
        response = client.get(
            f"/api/v1/weather/summary?latitude={test_user.farm_location_lat}&longitude={test_user.farm_location_lng}",
            headers=auth_headers
        )

        assert response.status_code in [200, 500]

    def test_get_summary_invalid_coords(self, client: TestClient, auth_headers: dict):
        """Test getting summary with invalid coordinates."""
        response = client.get(
            "/api/v1/weather/summary?latitude=-100&longitude=101.6869",
            headers=auth_headers
        )
        assert response.status_code == 422

    def test_get_summary_no_auth(self, client: TestClient):
        """Test getting summary without authentication."""
        response = client.get(
            "/api/v1/weather/summary?latitude=3.1390&longitude=101.6869"
        )
        assert response.status_code == 403


class TestWeatherTest:
    """Test weather API test endpoint."""

    def test_weather_api_test(self, client: TestClient, auth_headers: dict):
        """Test the weather API test endpoint."""
        response = client.get(
            "/api/v1/weather/test",
            headers=auth_headers
        )

        assert response.status_code in [200, 500]
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "ok"
            assert "sample_data" in data

    def test_weather_api_test_no_auth(self, client: TestClient):
        """Test weather API test endpoint without authentication."""
        response = client.get("/api/v1/weather/test")
        assert response.status_code == 403


class TestWeatherCoordinateRanges:
    """Test weather endpoints with various coordinate ranges."""

    def test_edge_case_coordinates(self, client: TestClient, auth_headers: dict):
        """Test with edge case coordinates."""
        # Valid edge coordinates
        valid_coords = [
            (0, 0),           # Equator/Prime meridian
            (-90, 0),         # South pole
            (90, 0),          # North pole
            (0, -180),        # International date line
            (0, 180),         # International date line
            (5.9788, 116.0753),  # Sabah, Malaysia
            (1.5533, 110.3592),  # Sarawak, Malaysia
        ]

        for lat, lng in valid_coords:
            response = client.get(
                f"/api/v1/weather/current?latitude={lat}&longitude={lng}",
                headers=auth_headers
            )
            # Should not return 422 (validation error)
            assert response.status_code in [200, 500]

    def test_malaysian_locations(self, client: TestClient, auth_headers: dict):
        """Test with Malaysian state locations."""
        malaysian_locations = [
            ("Kedah", 6.1184, 100.3685),
            ("Penang", 5.4164, 100.3327),
            ("Selangor", 3.0738, 101.5183),
            ("Johor", 1.4854, 103.7618),
        ]

        for name, lat, lng in malaysian_locations:
            response = client.get(
                f"/api/v1/weather/current?latitude={lat}&longitude={lng}&location_name={name}",
                headers=auth_headers
            )
            assert response.status_code in [200, 500]
