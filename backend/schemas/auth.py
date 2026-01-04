"""
Authentication Schemas

Pydantic models for authentication request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    """
    Schema for user registration request.
    
    Validates:
    - Username: 3-50 characters, alphanumeric + underscore
    - Password: minimum 6 characters
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username (3-50 characters)"
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Password (minimum 6 characters)"
    )
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Ensure username contains only alphanumeric characters and underscores."""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v.lower()  # Store usernames in lowercase
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_farmer",
                "password": "securepass123"
            }
        }


class UserLogin(BaseModel):
    """
    Schema for user login request.
    
    Uses OAuth2 password flow format (username + password).
    """
    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_farmer",
                "password": "securepass123"
            }
        }


class Token(BaseModel):
    """
    Schema for JWT token response.
    
    Returns:
    - access_token: JWT token string
    - token_type: Always "bearer"
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type (always 'bearer')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }


class UserResponse(BaseModel):
    """
    Schema for user data response.
    
    Returns user information without sensitive data (no password hash).
    """
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    is_active: bool = Field(..., description="Whether user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")
    
    class Config:
        from_attributes = True  # Allows creation from ORM models
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "john_farmer",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00"
            }
        }
