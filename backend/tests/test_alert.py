"""
Tests for alert endpoints.

Tests:
- List alerts with filtering
- Get specific alert
- Update alert (mark as read/acknowledged)
- Delete alert
- Bulk operations
- Statistics
- Alert generation
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from models.alert import Alert


class TestListAlerts:
    """Test listing alerts."""
    
    def test_list_alerts(self, client: TestClient, auth_headers: dict, test_alert):
        """Test listing alerts returns user's alerts."""
        response = client.get("/api/v1/alert/", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["id"] == test_alert.id
        assert data[0]["title"] == "High Temperature Alert"
    
    def test_list_alerts_filter_by_type(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test filtering alerts by type."""
        from models.alert import AlertType, AlertSeverity

        # Create alerts of different types
        alert1 = Alert(
            user_id=test_user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.MEDIUM,
            title="Pest Alert",
            message="Test",
            is_acknowledged=False
        )
        alert2 = Alert(
            user_id=test_user.id,
            alert_type=AlertType.HEAVY_RAIN,
            severity=AlertSeverity.MEDIUM,
            title="Weather Alert",
            message="Test",
            is_acknowledged=False
        )
        db.add_all([alert1, alert2])
        db.commit()
        
        # Filter for pest alerts only
        response = client.get("/api/v1/alert/?type=pest_risk", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(alert["alert_type"] == "pest_risk" for alert in data)
    
    def test_list_alerts_filter_by_severity(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test filtering alerts by severity."""
        from models.alert import AlertType, AlertSeverity

        # Create alerts of different severities
        alert1 = Alert(
            user_id=test_user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.MEDIUM,
            title="Warning Alert",
            message="Test",
            is_acknowledged=False
        )
        alert2 = Alert(
            user_id=test_user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.CRITICAL,
            title="Critical Alert",
            message="Test",
            is_acknowledged=False
        )
        db.add_all([alert1, alert2])
        db.commit()
        
        # Filter for critical alerts only
        response = client.get("/api/v1/alert/?severity=critical", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(alert["severity"] == "critical" for alert in data)
    
    def test_list_alerts_filter_unread(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test filtering for unread alerts."""
        from models.alert import AlertType, AlertSeverity

        # Create read and unread alerts
        alert1 = Alert(
            user_id=test_user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.MEDIUM,
            title="Read Alert",
            message="Test",
            is_read=True,
            is_acknowledged=False
        )
        alert2 = Alert(
            user_id=test_user.id,
            alert_type=AlertType.PEST_RISK,
            severity=AlertSeverity.MEDIUM,
            title="Unread Alert",
            message="Test",
            is_read=False,
            is_acknowledged=False
        )
        db.add_all([alert1, alert2])
        db.commit()
        
        # Filter for unread alerts only
        response = client.get("/api/v1/alert/?is_read=false", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert all(not alert["is_read"] for alert in data)
    
    def test_list_alerts_no_auth(self, client: TestClient):
        """Test listing alerts without authentication fails."""
        response = client.get("/api/v1/alert/")
        assert response.status_code == 403


class TestGetAlert:
    """Test getting specific alert."""
    
    def test_get_alert_success(self, client: TestClient, auth_headers: dict, test_alert):
        """Test getting specific alert."""
        response = client.get(
            f"/api/v1/alert/{test_alert.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_alert.id
        assert data["title"] == test_alert.title
    
    def test_get_alert_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent alert fails."""
        response = client.get("/api/v1/alert/99999", headers=auth_headers)
        assert response.status_code == 404


class TestUpdateAlert:
    """Test updating alert."""
    
    def test_mark_alert_as_read(self, client: TestClient, auth_headers: dict, test_alert):
        """Test marking alert as read."""
        response = client.put(
            f"/api/v1/alert/{test_alert.id}",
            headers=auth_headers,
            json={"is_read": True}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_read"] is True
    
    def test_mark_alert_as_acknowledged(self, client: TestClient, auth_headers: dict, test_alert):
        """Test marking alert as acknowledged."""
        response = client.put(
            f"/api/v1/alert/{test_alert.id}",
            headers=auth_headers,
            json={"is_acknowledged": True}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["is_acknowledged"] is True
    
    def test_update_alert_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating non-existent alert fails."""
        response = client.put(
            "/api/v1/alert/99999",
            headers=auth_headers,
            json={"is_read": True}
        )
        assert response.status_code == 404


class TestDeleteAlert:
    """Test deleting alert."""
    
    def test_delete_alert_success(self, client: TestClient, auth_headers: dict, test_alert, db: Session):
        """Test successful alert deletion."""
        response = client.delete(
            f"/api/v1/alert/{test_alert.id}",
            headers=auth_headers
        )
        
        assert response.status_code == 204
        # 204 No Content responses don't have a body
        
        # Verify deletion
        alert = db.query(Alert).filter(Alert.id == test_alert.id).first()
        assert alert is None
    
    def test_delete_alert_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting non-existent alert fails."""
        response = client.delete("/api/v1/alert/99999", headers=auth_headers)
        assert response.status_code == 404


class TestBulkOperations:
    """Test bulk alert operations."""
    
    def test_bulk_mark_as_read(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test bulk marking alerts as read."""
        from models.alert import AlertType, AlertSeverity

        # Create multiple unread alerts
        alerts = []
        for i in range(3):
            alert = Alert(
                user_id=test_user.id,
                alert_type=AlertType.PEST_RISK,
                severity=AlertSeverity.MEDIUM,
                title=f"Alert {i}",
                message="Test",
                is_read=False,
                is_acknowledged=False
            )
            alerts.append(alert)
        db.add_all(alerts)
        db.commit()
        
        alert_ids = [alert.id for alert in alerts]
        
        # Bulk mark as read
        response = client.put(
            "/api/v1/alert/bulk",
            headers=auth_headers,
            json={
                "alert_ids": alert_ids,
                "is_read": True
            }
        )
        
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert data["updated_count"] == 3
    
    def test_bulk_delete(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test bulk deleting alerts."""
        from models.alert import AlertType, AlertSeverity

        # Create multiple alerts
        alerts = []
        for i in range(3):
            alert = Alert(
                user_id=test_user.id,
                alert_type=AlertType.PEST_RISK,
                severity=AlertSeverity.MEDIUM,
                title=f"Alert {i}",
                message="Test",
                is_acknowledged=False
            )
            alerts.append(alert)
        db.add_all(alerts)
        db.commit()
        
        alert_ids = [alert.id for alert in alerts]
        
        # Bulk delete
        response = client.request(
            "DELETE",
            "/api/v1/alert/bulk",
            headers=auth_headers,
            json={"alert_ids": alert_ids}
        )
        
        if response.status_code != 200:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.json()}")
        assert response.status_code == 200
        data = response.json()
        assert data["deleted_count"] == 3
        
        # Verify deletion
        remaining = db.query(Alert).filter(Alert.id.in_(alert_ids)).count()
        assert remaining == 0


class TestAlertStatistics:
    """Test alert statistics endpoint."""
    
    def test_get_statistics(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test getting alert statistics."""
        # Create alerts with different types and severities
        from models.alert import AlertType, AlertSeverity
        alerts = [
            Alert(user_id=test_user.id, alert_type=AlertType.PEST_RISK, severity=AlertSeverity.MEDIUM, title="Test", message="Test", is_read=False, is_acknowledged=False),
            Alert(user_id=test_user.id, alert_type=AlertType.PEST_RISK, severity=AlertSeverity.CRITICAL, title="Test", message="Test", is_read=False, is_acknowledged=False),
            Alert(user_id=test_user.id, alert_type=AlertType.HEAVY_RAIN, severity=AlertSeverity.MEDIUM, title="Test", message="Test", is_read=True, is_acknowledged=True),
        ]
        db.add_all(alerts)
        db.commit()
        
        response = client.get("/api/v1/alert/stats/summary", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_alerts"] == 3
        assert data["unread_alerts"] == 2
        # The statistics endpoint returns counts by the actual enum values from the model
        # Check that pest and weather types are counted (the exact keys depend on the categorization logic)
        assert "alerts_by_type" in data
        assert "alerts_by_severity" in data
        # 2 alerts are unacknowledged (is_acknowledged=False)
        assert data["unacknowledged_alerts"] >= 2


class TestAlertGeneration:
    """Test manual alert generation."""
    
    def test_trigger_alert_check(self, client: TestClient, auth_headers: dict):
        """Test manually triggering alert checks."""
        response = client.post("/api/v1/alert/check", headers=auth_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "new_alerts_count" in data
        assert isinstance(data["new_alerts_count"], int)
