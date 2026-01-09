"""
Tests for pest detection endpoints.

Tests:
- Image upload
- Pest detection (basic and enhanced)
- Detection history
- Pest reports
- Pest risk assessment
- Statistics
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from io import BytesIO
from PIL import Image

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from models.pest_detection import PestDetection
from models.pest_report import PestReport


def create_test_image(width=300, height=300, format="JPEG"):
    """Create a test image for upload tests."""
    img = Image.new('RGB', (width, height), color='green')
    img_bytes = BytesIO()
    img.save(img_bytes, format=format)
    img_bytes.seek(0)
    return img_bytes


class TestImageUpload:
    """Test pest image upload endpoint."""

    def test_upload_image_success(self, client: TestClient, auth_headers: dict):
        """Test successful image upload."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/upload",
            headers=auth_headers,
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 201
        data = response.json()
        assert "filename" in data
        assert "file_url" in data
        assert data["message"] == "Image uploaded successfully. Use /pest/analyze to detect pests."

    def test_upload_image_no_auth(self, client: TestClient):
        """Test image upload without authentication fails."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/upload",
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 403

    def test_upload_image_too_small(self, client: TestClient, auth_headers: dict):
        """Test image upload with too small image fails."""
        img = create_test_image(width=100, height=100)
        response = client.post(
            "/api/v1/pest/upload",
            headers=auth_headers,
            files={"file": ("small.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 400


class TestPestDetection:
    """Test pest detection endpoints."""

    def test_detect_pest_success(self, client: TestClient, auth_headers: dict):
        """Test successful pest detection."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/detect",
            headers=auth_headers,
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 201
        data = response.json()
        assert "detection_id" in data
        assert "image_url" in data
        assert "detections" in data
        assert "primary_detection" in data
        assert len(data["detections"]) > 0

    def test_detect_pest_with_notes(self, client: TestClient, auth_headers: dict):
        """Test pest detection with notes."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/detect?notes=Found%20on%20rice%20leaves",
            headers=auth_headers,
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 201
        data = response.json()
        assert "detection_id" in data

    def test_detect_pest_no_auth(self, client: TestClient):
        """Test pest detection without authentication fails."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/detect",
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 403


class TestEnhancedDetection:
    """Test enhanced pest detection with confidence tiering."""

    def test_enhanced_detect_success(self, client: TestClient, auth_headers: dict):
        """Test enhanced pest detection."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/detect/enhanced",
            headers=auth_headers,
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 201
        data = response.json()
        assert "status" in data
        assert data["status"] in ["detected", "partial", "unknown"]
        assert "confidence" in data
        assert "confidence_percent" in data
        assert "image_url" in data

    def test_enhanced_detect_with_retry(self, client: TestClient, auth_headers: dict):
        """Test enhanced detection with retry count."""
        img = create_test_image()
        response = client.post(
            "/api/v1/pest/detect/enhanced?retry_count=2",
            headers=auth_headers,
            files={"file": ("test.jpg", img, "image/jpeg")}
        )

        assert response.status_code == 201
        data = response.json()
        # After 2 retries, offer_report should be True if status is not detected
        if data["status"] != "detected":
            assert "offer_report" in data


class TestDetectionHistory:
    """Test pest detection history endpoints."""

    def test_list_detections(self, client: TestClient, auth_headers: dict, test_pest_detection):
        """Test listing pest detections."""
        response = client.get("/api/v1/pest/", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_list_detections_with_filter(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test listing detections with filters."""
        # Create test detection
        detection = PestDetection(
            user_id=test_user.id,
            pest_type="Rice Stem Borer",
            confidence_score=0.85,
            image_url="uploads/test.jpg"
        )
        db.add(detection)
        db.commit()

        # Filter by pest type
        response = client.get(
            "/api/v1/pest/?pest_type=Rice%20Stem%20Borer",
            headers=auth_headers
        )

        assert response.status_code == 200

    def test_list_detections_no_auth(self, client: TestClient):
        """Test listing detections without auth fails."""
        response = client.get("/api/v1/pest/")
        assert response.status_code == 403

    def test_get_detection_by_id(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test getting specific detection by ID."""
        # Create test detection
        detection = PestDetection(
            user_id=test_user.id,
            pest_type="Brown Planthopper",
            confidence_score=0.75,
            image_url="uploads/test.jpg"
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)

        response = client.get(
            f"/api/v1/pest/{detection.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["pest_type"] == "Brown Planthopper"

    def test_get_detection_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent detection fails."""
        response = client.get("/api/v1/pest/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_delete_detection(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test deleting a detection."""
        # Create test detection
        detection = PestDetection(
            user_id=test_user.id,
            pest_type="Rice Leaf Folder",
            confidence_score=0.80,
            image_url="uploads/test.jpg"
        )
        db.add(detection)
        db.commit()
        db.refresh(detection)

        response = client.delete(
            f"/api/v1/pest/{detection.id}",
            headers=auth_headers
        )

        assert response.status_code == 204

        # Verify deletion
        deleted = db.query(PestDetection).filter(PestDetection.id == detection.id).first()
        assert deleted is None


class TestPestStatistics:
    """Test pest statistics endpoint."""

    def test_get_statistics(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test getting pest statistics."""
        # Create test detections
        for i in range(3):
            detection = PestDetection(
                user_id=test_user.id,
                pest_type="Rice Stem Borer" if i < 2 else "Brown Planthopper",
                confidence_score=0.7 + i * 0.05,
                image_url=f"uploads/test{i}.jpg"
            )
            db.add(detection)
        db.commit()

        response = client.get("/api/v1/pest/stats/summary?days=30", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "total_detections" in data
        assert "unique_pests" in data
        assert "most_common_pest" in data
        assert "average_confidence" in data
        assert "detections_by_pest" in data

    def test_get_statistics_no_detections(self, client: TestClient, auth_headers: dict):
        """Test statistics with no detections."""
        response = client.get("/api/v1/pest/stats/summary?days=30", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert data["total_detections"] == 0


class TestPestRisk:
    """Test pest risk assessment endpoints."""

    def test_get_pest_risk(self, client: TestClient, auth_headers: dict, test_pest_weather_correlation):
        """Test getting pest risk assessment."""
        response = client.get("/api/v1/pest/risk", headers=auth_headers)

        # May return 503 if weather service is unavailable, or 200 on success
        assert response.status_code in [200, 503]
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "overall_risk" in data

    def test_get_pest_risk_summary(self, client: TestClient, auth_headers: dict, test_pest_weather_correlation):
        """Test getting pest risk summary."""
        response = client.get("/api/v1/pest/risk/summary", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "headline" in data
        assert "description" in data

    def test_pest_risk_no_auth(self, client: TestClient):
        """Test pest risk without auth fails."""
        response = client.get("/api/v1/pest/risk")
        assert response.status_code == 403


class TestPestReports:
    """Test manual pest report endpoints."""

    def test_submit_pest_report(self, client: TestClient, auth_headers: dict):
        """Test submitting a manual pest report."""
        response = client.post(
            "/api/v1/pest/report",
            headers=auth_headers,
            json={
                "image_url": "/uploads/test.jpg",
                "description": "Small green insects on rice leaves",
                "observed_severity": "moderate"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert "report_id" in data
        assert data["status"] == "submitted"
        assert "ai_response" in data

    def test_submit_pest_report_minimal(self, client: TestClient, auth_headers: dict):
        """Test submitting pest report with minimal data."""
        response = client.post(
            "/api/v1/pest/report",
            headers=auth_headers,
            json={
                "image_url": "/uploads/test.jpg",
                "observed_severity": "minor"
            }
        )

        assert response.status_code == 201

    def test_list_pest_reports(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test listing pest reports."""
        # Create test report
        report = PestReport(
            user_id=test_user.id,
            image_url="/uploads/test.jpg",
            description="Test description",
            observed_severity="moderate",
            ai_response={"possible_pest": "Unknown", "advice": "Consult expert"},
            status="pending"
        )
        db.add(report)
        db.commit()

        response = client.get("/api/v1/pest/reports", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert "reports" in data
        assert "total" in data

    def test_list_pest_reports_with_filter(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test listing pest reports with status filter."""
        # Create test reports
        report1 = PestReport(
            user_id=test_user.id,
            image_url="/uploads/test1.jpg",
            observed_severity="minor",
            ai_response={},
            status="pending"
        )
        report2 = PestReport(
            user_id=test_user.id,
            image_url="/uploads/test2.jpg",
            observed_severity="severe",
            ai_response={},
            status="reviewed"
        )
        db.add_all([report1, report2])
        db.commit()

        # Filter pending reports
        response = client.get("/api/v1/pest/reports?status=pending", headers=auth_headers)

        assert response.status_code == 200
        data = response.json()
        assert all(r["status"] == "pending" for r in data["reports"])

    def test_get_pest_report_by_id(self, client: TestClient, auth_headers: dict, db: Session, test_user):
        """Test getting specific pest report."""
        # Create test report
        report = PestReport(
            user_id=test_user.id,
            image_url="/uploads/test.jpg",
            description="Test pest",
            observed_severity="moderate",
            ai_response={"possible_pest": "Rice Bug"},
            status="pending"
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        response = client.get(
            f"/api/v1/pest/reports/{report.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["description"] == "Test pest"

    def test_get_pest_report_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting non-existent pest report."""
        response = client.get("/api/v1/pest/reports/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_pest_report_no_auth(self, client: TestClient):
        """Test pest report without auth fails."""
        response = client.post(
            "/api/v1/pest/report",
            json={
                "image_url": "/uploads/test.jpg",
                "observed_severity": "minor"
            }
        )
        assert response.status_code == 403
