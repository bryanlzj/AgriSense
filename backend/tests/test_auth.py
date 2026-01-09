"""
Tests for authentication endpoints.

Tests:
- User registration
- User login
- Get current user
- Token validation
- Error handling
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Add parent directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from models.user import User


class TestUserRegistration:
    """Test user registration endpoint."""

    def test_register_new_user(self, client: TestClient, db: Session):
        """Test successful user registration with all fields."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "password": "password123",
                "full_name": "New Test User",
                "farm_location_name": "Kedah",
                "farm_location_lat": 6.1184,
                "farm_location_lng": 100.3685,
                "crop_type": "rice"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert data["full_name"] == "New Test User"
        assert data["farm_location_name"] == "Kedah"
        assert data["crop_type"] == "rice"
        assert "id" in data
        assert "hashed_password" not in data  # Should not expose password

        # Verify user exists in database
        user = db.query(User).filter(User.username == "newuser").first()
        assert user is not None
        assert user.farm_location_lat == 6.1184

    def test_register_new_user_minimal(self, client: TestClient, db: Session):
        """Test registration with only required fields (uses defaults)."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "minimaluser",
                "password": "password123"
            }
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "minimaluser"
        # Defaults should be applied
        assert data["farm_location_name"] == "Kuala Lumpur"
        assert data["crop_type"] == "rice"

    def test_register_duplicate_username(self, client: TestClient, test_user: User):
        """Test registration with existing username fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "testuser",  # Already exists
                "password": "password123"
            }
        )

        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_invalid_crop_type(self, client: TestClient):
        """Test registration with invalid crop type fails."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "badcrop",
                "password": "password123",
                "crop_type": "invalid_crop"
            }
        )
        assert response.status_code == 422

    def test_register_invalid_data(self, client: TestClient):
        """Test registration with invalid data fails."""
        # Missing required fields
        response = client.post(
            "/api/v1/auth/register",
            json={"username": "newuser"}
        )
        assert response.status_code == 422  # Validation error

        # Empty username
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "",
                "password": "password123"
            }
        )
        assert response.status_code == 422

        # Short password
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "shortpass",
                "password": "123"  # Less than 6 chars
            }
        )
        assert response.status_code == 422


class TestUserLogin:
    """Test user login endpoint."""
    
    def test_login_success(self, client: TestClient, test_user: User):
        """Test successful login returns token."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "testpassword123"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert len(data["access_token"]) > 0
    
    def test_login_wrong_password(self, client: TestClient, test_user: User):
        """Test login with wrong password fails."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user fails."""
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        
        assert response.status_code == 401
        assert "incorrect" in response.json()["detail"].lower()
    
    def test_login_invalid_data(self, client: TestClient):
        """Test login with invalid data fails."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": "testuser"}  # Missing password
        )
        assert response.status_code == 422


class TestGetCurrentUser:
    """Test get current user endpoint."""
    
    def test_get_current_user_success(self, client: TestClient, auth_headers: dict, test_user: User):
        """Test getting current user with valid token."""
        response = client.get(
            "/api/v1/auth/me",
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert "id" in data
        assert "hashed_password" not in data
    
    def test_get_current_user_no_token(self, client: TestClient):
        """Test getting current user without token fails."""
        response = client.get("/api/v1/auth/me")
        
        assert response.status_code == 403
        assert "not authenticated" in response.json()["detail"].lower()
    
    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user with invalid token fails."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == 401
    
    def test_get_current_user_malformed_header(self, client: TestClient):
        """Test getting current user with malformed auth header fails."""
        # Missing "Bearer" prefix
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "token123"}
        )
        assert response.status_code == 403


class TestTokenValidation:
    """Test JWT token validation."""
    
    def test_token_contains_username(self, client: TestClient, test_user: User):
        """Test that token contains username in payload."""
        # Login to get token
        login_response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "testuser",
                "password": "testpassword123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Use token to get user info
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"
    
    def test_token_works_across_requests(self, client: TestClient, auth_headers: dict):
        """Test that token can be reused across multiple requests."""
        # First request
        response1 = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response1.status_code == 200
        
        # Second request with same token
        response2 = client.get("/api/v1/auth/me", headers=auth_headers)
        assert response2.status_code == 200
        
        # Both should return same user
        assert response1.json()["id"] == response2.json()["id"]
