"""
Tests for sector endpoints.

Tests:
- Create sector
- List sectors (with filtering and pagination)
- Get specific sector
- Update sector
- Delete sector
- Sector statistics
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from models.sector import Sector
from models.user import User


class TestCreateSector:
    """Test sector creation endpoint."""

    def test_create_sector_success(self, client: TestClient, auth_headers: dict):
        """Test successful sector creation with all fields."""
        response = client.post(
            "/api/v1/sector/",
            json={
                "name": "New Sector",
                "location": "East Field",
                "area": "3 acres",
                "area_value": 3.0,
                "area_unit": "acres",
                "crop": "wheat",
                "planted_date": "2025-03-15T00:00:00"
            },
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Sector"
        assert data["location"] == "East Field"
        assert data["area"] == "3 acres"
        assert data["area_value"] == 3.0
        assert data["area_unit"] == "acres"
        assert data["crop"] == "wheat"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_sector_minimal_fields(self, client: TestClient, auth_headers: dict):
        """Test sector creation with only required fields."""
        response = client.post(
            "/api/v1/sector/",
            json={
                "name": "Minimal Sector"
            },
            headers=auth_headers
        )

        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Minimal Sector"
        assert data["location"] is None
        assert data["crop"] is None
        assert data["area_unit"] == "acres"  # Default value

    def test_create_sector_no_auth(self, client: TestClient):
        """Test sector creation without authentication fails."""
        response = client.post(
            "/api/v1/sector/",
            json={
                "name": "Unauthorized Sector"
            }
        )

        assert response.status_code == 403  # HTTPBearer returns 403 when no auth header

    def test_create_sector_invalid_name_empty(self, client: TestClient, auth_headers: dict):
        """Test sector creation with empty name fails."""
        response = client.post(
            "/api/v1/sector/",
            json={
                "name": ""
            },
            headers=auth_headers
        )

        assert response.status_code == 422  # Validation error


class TestListSectors:
    """Test sector listing endpoint."""

    def test_list_sectors(self, client: TestClient, auth_headers: dict, test_sector: Sector):
        """Test listing sectors returns user's sectors."""
        response = client.get(
            "/api/v1/sector/",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        # Check the test sector is in the response
        sector_names = [s["name"] for s in data]
        assert "Test Sector 1" in sector_names

    def test_list_sectors_pagination(self, client: TestClient, auth_headers: dict, db: Session, test_user: User):
        """Test pagination parameters work correctly."""
        # Create multiple sectors
        for i in range(5):
            sector = Sector(
                user_id=test_user.id,
                name=f"Pagination Sector {i}",
                crop="corn"
            )
            db.add(sector)
        db.commit()

        # Test limit
        response = client.get(
            "/api/v1/sector/?limit=2",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Test skip
        response = client.get(
            "/api/v1/sector/?skip=2&limit=2",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    def test_list_sectors_filter_by_crop(self, client: TestClient, auth_headers: dict, db: Session, test_user: User):
        """Test filtering sectors by crop type."""
        # Create sectors with different crops
        sector1 = Sector(user_id=test_user.id, name="Rice Sector", crop="rice")
        sector2 = Sector(user_id=test_user.id, name="Wheat Sector", crop="wheat")
        db.add_all([sector1, sector2])
        db.commit()

        # Filter by rice
        response = client.get(
            "/api/v1/sector/?crop=rice",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert all("rice" in s["crop"].lower() for s in data if s["crop"])

    def test_list_sectors_no_auth(self, client: TestClient):
        """Test listing sectors without authentication fails."""
        response = client.get("/api/v1/sector/")
        assert response.status_code == 403  # HTTPBearer returns 403 when no auth header


class TestGetSector:
    """Test get specific sector endpoint."""

    def test_get_sector_success(self, client: TestClient, auth_headers: dict, test_sector: Sector):
        """Test getting a specific sector by ID."""
        response = client.get(
            f"/api/v1/sector/{test_sector.id}",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_sector.id
        assert data["name"] == "Test Sector 1"
        assert data["location"] == "North Field"
        assert data["crop"] == "rice"

    def test_get_sector_not_found(self, client: TestClient, auth_headers: dict):
        """Test getting a non-existent sector returns 404."""
        response = client.get(
            "/api/v1/sector/99999",
            headers=auth_headers
        )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_sector_no_auth(self, client: TestClient, test_sector: Sector):
        """Test getting sector without authentication fails."""
        response = client.get(f"/api/v1/sector/{test_sector.id}")
        assert response.status_code == 403  # HTTPBearer returns 403 when no auth header


class TestUpdateSector:
    """Test sector update endpoint."""

    def test_update_sector_success(self, client: TestClient, auth_headers: dict, test_sector: Sector):
        """Test successful sector update with all fields."""
        response = client.put(
            f"/api/v1/sector/{test_sector.id}",
            json={
                "name": "Updated Sector Name",
                "location": "South Field",
                "crop": "corn"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Sector Name"
        assert data["location"] == "South Field"
        assert data["crop"] == "corn"
        # Unchanged fields should remain
        assert data["area_value"] == 2.0

    def test_update_sector_partial(self, client: TestClient, auth_headers: dict, test_sector: Sector):
        """Test partial update (only some fields)."""
        original_name = test_sector.name

        response = client.put(
            f"/api/v1/sector/{test_sector.id}",
            json={
                "crop": "soybean"
            },
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["crop"] == "soybean"
        assert data["name"] == original_name  # Unchanged

    def test_update_sector_not_found(self, client: TestClient, auth_headers: dict):
        """Test updating a non-existent sector returns 404."""
        response = client.put(
            "/api/v1/sector/99999",
            json={
                "name": "Ghost Sector"
            },
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_update_sector_no_auth(self, client: TestClient, test_sector: Sector):
        """Test updating sector without authentication fails."""
        response = client.put(
            f"/api/v1/sector/{test_sector.id}",
            json={"name": "Hacked Sector"}
        )
        assert response.status_code == 403  # HTTPBearer returns 403 when no auth header


class TestDeleteSector:
    """Test sector deletion endpoint."""

    def test_delete_sector_success(self, client: TestClient, auth_headers: dict, test_sector: Sector, db: Session):
        """Test successful sector deletion."""
        sector_id = test_sector.id

        response = client.delete(
            f"/api/v1/sector/{sector_id}",
            headers=auth_headers
        )

        assert response.status_code == 204

        # Verify sector no longer exists
        deleted_sector = db.query(Sector).filter(Sector.id == sector_id).first()
        assert deleted_sector is None

    def test_delete_sector_not_found(self, client: TestClient, auth_headers: dict):
        """Test deleting a non-existent sector returns 404."""
        response = client.delete(
            "/api/v1/sector/99999",
            headers=auth_headers
        )

        assert response.status_code == 404

    def test_delete_sector_no_auth(self, client: TestClient, test_sector: Sector):
        """Test deleting sector without authentication fails."""
        response = client.delete(f"/api/v1/sector/{test_sector.id}")
        assert response.status_code == 403  # HTTPBearer returns 403 when no auth header


class TestSectorStatistics:
    """Test sector statistics endpoint."""

    def test_get_sector_stats(self, client: TestClient, auth_headers: dict, db: Session, test_user: User):
        """Test getting sector statistics."""
        # Create some sectors with different crops
        sectors = [
            Sector(user_id=test_user.id, name="Rice Field 1", crop="rice"),
            Sector(user_id=test_user.id, name="Rice Field 2", crop="rice"),
            Sector(user_id=test_user.id, name="Corn Field", crop="corn"),
        ]
        db.add_all(sectors)
        db.commit()

        response = client.get(
            "/api/v1/sector/stats/summary",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert "total_sectors" in data
        assert data["total_sectors"] >= 3
        assert "crops" in data
        assert data["crops"]["rice"] >= 2
        assert data["crops"]["corn"] >= 1
        assert "sector_names" in data
        assert "Rice Field 1" in data["sector_names"]

    def test_get_sector_stats_empty(self, client: TestClient, auth_headers: dict):
        """Test statistics with no sectors returns zero counts."""
        response = client.get(
            "/api/v1/sector/stats/summary",
            headers=auth_headers
        )

        assert response.status_code == 200
        data = response.json()
        assert data["total_sectors"] == 0
        assert data["crops"] == {}
        assert data["sector_names"] == []

    def test_get_sector_stats_no_auth(self, client: TestClient):
        """Test getting statistics without authentication fails."""
        response = client.get("/api/v1/sector/stats/summary")
        assert response.status_code == 403  # HTTPBearer returns 403 when no auth header
