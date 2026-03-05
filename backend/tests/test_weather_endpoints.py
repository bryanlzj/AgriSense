"""
Tests for the sensor-based weather endpoints.

Tests cover:
- GET /api/v1/weather/current (sensor-based current weather)
- GET /api/v1/weather/historical (historical weather from sensor readings)
"""

import pytest
from datetime import datetime, timedelta, timezone


# ---------------------------------------------------------------------------
# Helper: create a sensor reading via the API
# ---------------------------------------------------------------------------

def _create_sensor_reading(client, auth_headers, **overrides):
    """Post a sensor reading and return the response JSON."""
    payload = {
        "temperature": 28.5,
        "relative_humidity": 75.0,
        "rain": 1.2,
        "wind_speed": 12.5,
        "solar_radiation": 650.0,
        "soil_temperature": 26.0,
        "soil_moisture": 0.35,
        "weather_code": 1,
    }
    payload.update(overrides)
    resp = client.post("/api/v1/sensor/", json=payload, headers=auth_headers)
    assert resp.status_code == 201, f"Sensor creation failed: {resp.text}"
    return resp.json()


# ============================================================================
# /weather/current
# ============================================================================

class TestCurrentWeather:
    """Tests for GET /api/v1/weather/current."""

    def test_current_weather_returns_200_when_sensor_data_exists(self, client, auth_headers):
        """Current weather should return 200 when a sensor reading exists."""
        _create_sensor_reading(client, auth_headers)
        resp = client.get("/api/v1/weather/current", headers=auth_headers)
        assert resp.status_code == 200

    def test_current_weather_returns_expected_fields(self, client, auth_headers):
        """Response should contain source, temperature, weather_condition, timestamp."""
        _create_sensor_reading(client, auth_headers)
        resp = client.get("/api/v1/weather/current", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()

        assert data["source"] == "sensor"
        assert "temperature" in data
        assert "weather_condition" in data
        assert "timestamp" in data
        assert "confidence" in data
        assert "probabilities" in data
        assert "relative_humidity" in data
        assert "rain" in data
        assert "wind_speed" in data
        assert "soil_moisture" in data
        assert "model_loaded" in data

    def test_current_weather_returns_404_when_no_sensor_data(self, client, auth_headers):
        """Should return 404 when no sensor readings exist for the user."""
        resp = client.get("/api/v1/weather/current", headers=auth_headers)
        assert resp.status_code == 404
        assert "No sensor data available" in resp.json()["detail"]


# ============================================================================
# /weather/historical
# ============================================================================

class TestHistoricalWeather:
    """Tests for GET /api/v1/weather/historical."""

    def test_historical_24h_returns_correct_structure(self, client, auth_headers):
        """24h historical endpoint should return correct response structure."""
        _create_sensor_reading(client, auth_headers)
        resp = client.get(
            "/api/v1/weather/historical",
            params={"period": "24h"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()

        assert data["period"] == "24h"
        assert "start" in data
        assert "end" in data
        assert "readings_count" in data
        assert "readings" in data
        assert "summary" in data
        assert data["readings_count"] >= 1
        assert len(data["readings"]) >= 1

    def test_historical_7d_returns_correct_structure(self, client, auth_headers):
        """7d historical endpoint should return correct response structure."""
        _create_sensor_reading(client, auth_headers)
        resp = client.get(
            "/api/v1/weather/historical",
            params={"period": "7d"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()

        assert data["period"] == "7d"
        assert "readings" in data
        assert "summary" in data
        assert data["readings_count"] >= 1

    def test_historical_custom_missing_dates_returns_400(self, client, auth_headers):
        """Custom period without dates should return 400."""
        resp = client.get(
            "/api/v1/weather/historical",
            params={"period": "custom"},
            headers=auth_headers,
        )
        assert resp.status_code == 400
        assert "start_date and end_date are required" in resp.json()["detail"]

    def test_historical_custom_exceeding_30_days_returns_400(self, client, auth_headers):
        """Custom period exceeding 30 days should return 400."""
        now = datetime.now(timezone.utc)
        start = (now - timedelta(days=31)).isoformat()
        end = now.isoformat()
        resp = client.get(
            "/api/v1/weather/historical",
            params={"period": "custom", "start_date": start, "end_date": end},
            headers=auth_headers,
        )
        assert resp.status_code == 400
        assert "cannot exceed 30 days" in resp.json()["detail"]

    def test_historical_custom_valid_range(self, client, auth_headers):
        """Custom period with valid dates should return 200."""
        _create_sensor_reading(client, auth_headers)
        now = datetime.now(timezone.utc)
        start = (now - timedelta(days=1)).isoformat()
        end = now.isoformat()
        resp = client.get(
            "/api/v1/weather/historical",
            params={"period": "custom", "start_date": start, "end_date": end},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["period"] == "custom"

    def test_historical_summary_has_expected_fields(self, client, auth_headers):
        """Summary object should contain all expected statistical fields."""
        _create_sensor_reading(client, auth_headers)
        resp = client.get(
            "/api/v1/weather/historical",
            params={"period": "24h"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        summary = resp.json()["summary"]

        assert "avg_temperature" in summary
        assert "max_temperature" in summary
        assert "min_temperature" in summary
        assert "avg_humidity" in summary
        assert "total_rain" in summary
        assert "dominant_condition" in summary
        assert "condition_breakdown" in summary
