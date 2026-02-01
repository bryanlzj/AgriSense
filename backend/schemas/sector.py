"""
Pydantic schemas for sector data.

These schemas define the structure for sector/farm management requests and responses.
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class SectorCreate(BaseModel):
    """
    Schema for creating a new sector.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Sector name"
    )
    location: Optional[str] = Field(
        None,
        max_length=200,
        description="Location description within the farm"
    )
    area: Optional[str] = Field(
        None,
        max_length=50,
        description="Area size as string (e.g., '2 acres')"
    )
    area_value: Optional[float] = Field(
        None,
        ge=0,
        description="Numeric area value"
    )
    area_unit: Optional[str] = Field(
        "acres",
        max_length=20,
        description="Area unit (acres, hectares, sq meters)"
    )
    crop: Optional[str] = Field(
        None,
        max_length=100,
        description="Crop type planted"
    )
    planted_date: Optional[datetime] = Field(
        None,
        description="Date when crop was planted"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sector 1",
                "location": "North Field",
                "area": "2 acres",
                "crop": "Corn",
                "planted_date": "2025-03-12T00:00:00"
            }
        }


class SectorUpdate(BaseModel):
    """
    Schema for updating a sector.
    All fields are optional for partial updates.
    """
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=200)
    area: Optional[str] = Field(None, max_length=50)
    area_value: Optional[float] = Field(None, ge=0)
    area_unit: Optional[str] = Field(None, max_length=20)
    crop: Optional[str] = Field(None, max_length=100)
    planted_date: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sector 1 - Updated",
                "crop": "Wheat"
            }
        }


class SectorResponse(BaseModel):
    """
    Schema for sector responses.
    """
    id: int
    user_id: int
    name: str
    location: Optional[str]
    area: Optional[str]
    area_value: Optional[float]
    area_unit: Optional[str]
    crop: Optional[str]
    planted_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "name": "Sector 1",
                "location": "North Field",
                "area": "2 acres",
                "area_value": 2.0,
                "area_unit": "acres",
                "crop": "Corn",
                "planted_date": "2025-03-12T00:00:00",
                "created_at": "2025-01-15T10:30:00",
                "updated_at": "2025-01-15T10:30:00"
            }
        }


class SectorListResponse(BaseModel):
    """
    Schema for paginated sector list response.
    """
    sectors: List[SectorResponse]
    total: int
    skip: int
    limit: int

    class Config:
        json_schema_extra = {
            "example": {
                "sectors": [
                    {
                        "id": 1,
                        "user_id": 1,
                        "name": "Sector 1",
                        "location": "North Field",
                        "area": "2 acres",
                        "area_value": 2.0,
                        "area_unit": "acres",
                        "crop": "Corn",
                        "planted_date": "2025-03-12T00:00:00",
                        "created_at": "2025-01-15T10:30:00",
                        "updated_at": "2025-01-15T10:30:00"
                    }
                ],
                "total": 1,
                "skip": 0,
                "limit": 50
            }
        }
