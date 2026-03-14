"""
Authentication Schemas

Pydantic models for authentication request/response validation.
"""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional, Literal


# Valid crop types
VALID_CROP_TYPES = Literal["rice", "vegetables", "corn", "oil_palm", "rubber"]

# Malaysian locations with coordinates
MALAYSIAN_LOCATIONS = {
    "Perlis": {"lat": 6.4449, "lng": 100.2048},
    "Kedah": {"lat": 6.1184, "lng": 100.3685},
    "Penang": {"lat": 5.4164, "lng": 100.3327},
    "Perak": {"lat": 4.5921, "lng": 101.0901},
    "Selangor": {"lat": 3.0738, "lng": 101.5183},
    "Negeri Sembilan": {"lat": 2.7258, "lng": 101.9424},
    "Melaka": {"lat": 2.1896, "lng": 102.2501},
    "Johor": {"lat": 1.4854, "lng": 103.7618},
    "Pahang": {"lat": 3.8126, "lng": 103.3256},
    "Terengganu": {"lat": 5.3117, "lng": 103.1324},
    "Kelantan": {"lat": 6.1254, "lng": 102.2381},
    "Sabah": {"lat": 5.9788, "lng": 116.0753},
    "Sarawak": {"lat": 1.5533, "lng": 110.3592},
    "Kuala Lumpur": {"lat": 3.1390, "lng": 101.6869},
}


class UserRegister(BaseModel):
    """
    Schema for user registration request (PRD v2).

    Validates:
    - Username: 3-50 characters, alphanumeric + underscore
    - Password: minimum 6 characters
    - Full name: optional, max 100 characters
    - Farm location: name + coordinates (Malaysian states)
    - Crop type: one of rice, vegetables, corn, oil_palm, rubber
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
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        description="User's full name"
    )
    email: Optional[str] = Field(
        None,
        max_length=255,
        description="User email address (required for new signups)"
    )
    farm_location_name: str = Field(
        default="Kuala Lumpur",
        max_length=100,
        description="Farm location name (Malaysian state)"
    )
    farm_location_lat: float = Field(
        default=3.1390,
        ge=-90,
        le=90,
        description="Farm latitude coordinate"
    )
    farm_location_lng: float = Field(
        default=101.6869,
        ge=-180,
        le=180,
        description="Farm longitude coordinate"
    )
    crop_type: str = Field(
        default="rice",
        description="Primary crop type (rice, vegetables, corn, oil_palm, rubber)"
    )

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Basic email format validation."""
        if v is None or v.strip() == '':
            return None
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Ensure username contains only alphanumeric characters and underscores."""
        if not v.replace('_', '').isalnum():
            raise ValueError('Username must contain only letters, numbers, and underscores')
        return v.lower()  # Store usernames in lowercase

    @field_validator('crop_type')
    @classmethod
    def validate_crop_type(cls, v: str) -> str:
        """Ensure crop type is valid."""
        valid_types = ["rice", "vegetables", "corn", "oil_palm", "rubber"]
        if v.lower() not in valid_types:
            raise ValueError(f'Crop type must be one of: {", ".join(valid_types)}')
        return v.lower()

    class Config:
        json_schema_extra = {
            "example": {
                "username": "ahmad_farmer",
                "password": "SecurePass123",
                "full_name": "Ahmad bin Ibrahim",
                "farm_location_name": "Kedah",
                "farm_location_lat": 6.1184,
                "farm_location_lng": 100.3685,
                "crop_type": "rice"
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


class UserUpdate(BaseModel):
    """Schema for updating user profile. All fields optional."""
    full_name: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    farm_location_name: Optional[str] = Field(None, max_length=100)
    farm_location_lat: Optional[float] = Field(None, ge=-90, le=90)
    farm_location_lng: Optional[float] = Field(None, ge=-180, le=180)
    crop_type: Optional[str] = Field(None)

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v.strip() == '':
            return None
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

    @field_validator('crop_type')
    @classmethod
    def validate_crop_type_update(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        valid_types = ["rice", "vegetables", "corn", "oil_palm", "rubber"]
        if v.lower() not in valid_types:
            raise ValueError(f'Crop type must be one of: {", ".join(valid_types)}')
        return v.lower()


class PasswordChange(BaseModel):
    """Schema for changing password."""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=6, description="New password (min 6 chars)")


class UserResponse(BaseModel):
    """
    Schema for user data response (PRD v2).

    Returns user information without sensitive data (no password hash).
    Includes farm profile fields.
    """
    id: int = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    full_name: Optional[str] = Field(None, description="User's full name")
    email: Optional[str] = Field(None, description="User email address")
    farm_location_name: str = Field(..., description="Farm location name")
    farm_location_lat: float = Field(..., description="Farm latitude")
    farm_location_lng: float = Field(..., description="Farm longitude")
    crop_type: str = Field(..., description="Primary crop type")
    is_active: bool = Field(..., description="Whether user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class Config:
        from_attributes = True  # Allows creation from ORM models
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "ahmad_farmer",
                "full_name": "Ahmad bin Ibrahim",
                "email": "ahmad@example.com",
                "farm_location_name": "Kedah",
                "farm_location_lat": 6.1184,
                "farm_location_lng": 100.3685,
                "crop_type": "rice",
                "is_active": True,
                "created_at": "2024-01-15T10:30:00"
            }
        }
