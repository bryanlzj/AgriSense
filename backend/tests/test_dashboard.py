"""
Tests for dashboard endpoints.

Tests:
- Get full dashboard
- Get quick dashboard
- Dashboard with various data states
- Error handling
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

from models.alert import Alert, AlertType, AlertSeverity
from models.pest_detection import PestDetection


class TestGetDashboard:
    """Test full dashboard endpoint."""

    def test_get_dashboard_success(self, client: TestClient, auth_headers: dict):
        """Test getting dashboard data."""
        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Check required sections
        assert "user" in data
        assert "weather" in data
        assert "alerts" in data
        assert "detections" in data
        assert "pest_risk" in data
        assert "generated_at" in data

    def test_dashboard_user_info(self, client: TestClient, auth_headers: dict, test_user):
        """Test dashboard includes correct user info."""
        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["user"]["username"] == test_user.username
        assert data["user"]["crop_type"] == test_user.crop_type
        assert data["user"]["farm_location"] == test_user.farm_location_name

    def test_dashboard_with_alerts(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test dashboard shows alert data."""
        # Create test alerts
        for i in range(5):
            alert = Alert(
                user_id=test_user.id,
                alert_type=AlertType.PEST_RISK,
                severity=AlertSeverity.MEDIUM,
                title=f"Test Alert {i}",
                message="Test message",
                is_read=(i < 2),
                is_acknowledged=False
            )
            db.add(alert)
        db.commit()

        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["alerts"]["total_unread"] == 3
        assert len(data["alerts"]["recent"]) <= 3

    def test_dashboard_with_detections(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test dashboard shows recent detections."""
        # Create test detections
        for i in range(5):
            detection = PestDetection(
                user_id=test_user.id,
                pest_type=f"Pest {i}",
                confidence_score=0.8,
                image_url=f"uploads/test{i}.jpg"
            )
            db.add(detection)
        db.commit()

        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["detections"]["total_recent"] >= 0
        assert len(data["detections"]["recent"]) <= 3

    def test_dashboard_no_auth(self, client: TestClient):
        """Test dashboard without authentication fails."""
        response = client.get("/api/v1/dashboard")
        assert response.status_code == 403


class TestQuickDashboard:
    """Test quick dashboard endpoint."""

    def test_get_quick_dashboard(self, client: TestClient, auth_headers: dict):
        """Test getting quick dashboard data."""
        response = client.get("/api/v1/dashboard/quick", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert "user" in data
        assert "crop_type" in data
        assert "location" in data
        assert "unread_alerts" in data
        assert "recent_detections" in data
        assert "generated_at" in data

    def test_quick_dashboard_user_info(self, client: TestClient, auth_headers: dict, test_user):
        """Test quick dashboard includes correct user info."""
        response = client.get("/api/v1/dashboard/quick", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        assert data["user"] == test_user.username
        assert data["crop_type"] == test_user.crop_type

    def test_quick_dashboard_alert_count(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test quick dashboard shows correct unread alert count."""
        # Create unread alerts
        for i in range(3):
            alert = Alert(
                user_id=test_user.id,
                alert_type=AlertType.PEST_RISK,
                severity=AlertSeverity.MEDIUM,
                title=f"Unread Alert {i}",
                message="Test",
                is_read=False,
                is_acknowledged=False
            )
            db.add(alert)
        db.commit()

        response = client.get("/api/v1/dashboard/quick", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["unread_alerts"] == 3

    def test_quick_dashboard_detection_count(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test quick dashboard shows correct recent detection count."""
        # Create recent detections
        for i in range(4):
            detection = PestDetection(
                user_id=test_user.id,
                pest_type=f"Pest {i}",
                confidence_score=0.75,
                image_url=f"uploads/test{i}.jpg"
            )
            db.add(detection)
        db.commit()

        response = client.get("/api/v1/dashboard/quick", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["recent_detections"] >= 4

    def test_quick_dashboard_no_auth(self, client: TestClient):
        """Test quick dashboard without authentication fails."""
        response = client.get("/api/v1/dashboard/quick")
        assert response.status_code == 403


class TestDashboardEdgeCases:
    """Test dashboard edge cases."""

    def test_dashboard_empty_user(self, client: TestClient, auth_headers: dict):
        """Test dashboard for user with no data."""
        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should return empty/zero values, not errors
        assert data["alerts"]["total_unread"] == 0
        assert len(data["alerts"]["recent"]) == 0
        assert data["detections"]["total_recent"] == 0

    def test_dashboard_weather_error_handling(self, client: TestClient, auth_headers: dict):
        """Test dashboard handles weather service errors gracefully."""
        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Weather may have error but dashboard should still return
        assert "weather" in data
        # If weather failed, it should have error info
        if data["weather"] and "error" in data["weather"]:
            assert "location" in data["weather"]

    def test_dashboard_pest_risk_error_handling(self, client: TestClient, auth_headers: dict):
        """Test dashboard handles pest risk service errors gracefully."""
        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Pest risk may have error but dashboard should still return
        assert "pest_risk" in data


class TestDashboardPerformance:
    """Test dashboard performance aspects."""

    def test_dashboard_with_many_alerts(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test dashboard with many alerts only returns top 3."""
        # Create many alerts
        for i in range(20):
            alert = Alert(
                user_id=test_user.id,
                alert_type=AlertType.PEST_RISK,
                severity=AlertSeverity.MEDIUM,
                title=f"Alert {i}",
                message="Test",
                is_read=False,
                is_acknowledged=False
            )
            db.add(alert)
        db.commit()

        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should only return top 3 recent alerts
        assert len(data["alerts"]["recent"]) == 3
        # But total count should reflect all unread
        assert data["alerts"]["total_unread"] == 20

    def test_dashboard_with_many_detections(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test dashboard with many detections only returns top 3."""
        # Create many detections
        for i in range(15):
            detection = PestDetection(
                user_id=test_user.id,
                pest_type=f"Pest {i}",
                confidence_score=0.8,
                image_url=f"uploads/test{i}.jpg"
            )
            db.add(detection)
        db.commit()

        response = client.get("/api/v1/dashboard", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()

        # Should only return top 3 recent detections
        assert len(data["detections"]["recent"]) == 3
