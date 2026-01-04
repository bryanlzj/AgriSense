"""
Pest Detection Schemas

Pydantic models for pest detection API requests and responses.
These schemas define the structure of data for pest detection operations.

Learning Notes:
--------------
1. Pest Detection Flow:
   - User uploads image
   - System validates image
   - ML model analyzes image
   - System returns pest detection results
   - Results saved to database
   
2. Confidence Scores:
   - Range from 0.0 to 1.0 (0% to 100%)
   - Higher score = more confident prediction
   - Typically threshold at 0.5 or 0.7 for actionable results
   
3. Pest Types (Common in Agriculture):
   - Fall Armyworm: Major corn/maize pest
   - Aphids: Small sap-sucking insects
   - Whitefly: Small white flying insects
   - Leaf Miner: Creates tunnels in leaves
   - Thrips: Tiny insects that damage plants
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, validator


class PestDetectionCreate(BaseModel):
    """
    Schema for creating a pest detection record.
    Used when saving detection results to database.
    """
    pest_type: str = Field(..., description="Type of pest detected")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    image_path: str = Field(..., description="Path to uploaded image")
    notes: Optional[str] = Field(None, description="Additional notes or observations")
    
    @validator('confidence')
    def validate_confidence(cls, v):
        """Ensure confidence is between 0 and 1"""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "pest_type": "Fall Armyworm",
                "confidence": 0.87,
                "image_path": "uploads/abc123.jpg",
                "notes": "Detected on corn leaves"
            }
        }


class PestDetectionResponse(BaseModel):
    """
    Schema for pest detection response.
    Returns detection results with metadata.
    """
    id: int = Field(..., description="Detection record ID")
    user_id: int = Field(..., description="ID of user who uploaded image")
    pest_type: str = Field(..., description="Type of pest detected")
    confidence: float = Field(..., description="Confidence score (0-1)")
    image_path: str = Field(..., description="Path to uploaded image")
    image_url: str = Field(..., description="URL to access image")
    notes: Optional[str] = Field(None, description="Additional notes")
    created_at: datetime = Field(..., description="Detection timestamp")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "pest_type": "Fall Armyworm",
                "confidence": 0.87,
                "image_path": "uploads/abc123.jpg",
                "image_url": "http://localhost:8000/uploads/abc123.jpg",
                "notes": "Detected on corn leaves",
                "created_at": "2025-01-04T10:30:00"
            }
        }


class ImageUploadResponse(BaseModel):
    """
    Schema for image upload response.
    Returns upload confirmation and file details.
    """
    filename: str = Field(..., description="Unique filename")
    file_path: str = Field(..., description="Server file path")
    file_url: str = Field(..., description="URL to access file")
    file_size: int = Field(..., description="File size in bytes")
    width: int = Field(..., description="Image width in pixels")
    height: int = Field(..., description="Image height in pixels")
    message: str = Field(..., description="Success message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "filename": "a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
                "file_path": "/uploads/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
                "file_url": "http://localhost:8000/uploads/a1b2c3d4-e5f6-7890-abcd-ef1234567890.jpg",
                "file_size": 245760,
                "width": 1024,
                "height": 768,
                "message": "Image uploaded successfully"
            }
        }


class PestDetectionResult(BaseModel):
    """
    Schema for ML model detection result.
    Represents a single pest detection prediction.
    """
    pest_type: str = Field(..., description="Type of pest detected")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    description: Optional[str] = Field(None, description="Pest description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pest_type": "Fall Armyworm",
                "confidence": 0.87,
                "description": "A major pest of corn and other crops"
            }
        }


class PestDetectionAnalysisResponse(BaseModel):
    """
    Schema for complete pest detection analysis response.
    Includes image info, detection results, and saved record.
    """
    detection_id: int = Field(..., description="Saved detection record ID")
    image_url: str = Field(..., description="URL to uploaded image")
    detections: List[PestDetectionResult] = Field(..., description="List of detected pests")
    primary_detection: PestDetectionResult = Field(..., description="Most confident detection")
    analysis_timestamp: datetime = Field(..., description="When analysis was performed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detection_id": 1,
                "image_url": "http://localhost:8000/uploads/abc123.jpg",
                "detections": [
                    {
                        "pest_type": "Fall Armyworm",
                        "confidence": 0.87,
                        "description": "A major pest of corn and other crops"
                    },
                    {
                        "pest_type": "Aphids",
                        "confidence": 0.12,
                        "description": "Small sap-sucking insects"
                    }
                ],
                "primary_detection": {
                    "pest_type": "Fall Armyworm",
                    "confidence": 0.87,
                    "description": "A major pest of corn and other crops"
                },
                "analysis_timestamp": "2025-01-04T10:30:00"
            }
        }


class PestDetectionFilter(BaseModel):
    """
    Schema for filtering pest detection records.
    Used in list/search endpoints.
    """
    pest_type: Optional[str] = Field(None, description="Filter by pest type")
    min_confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum confidence")
    start_date: Optional[datetime] = Field(None, description="Filter from date")
    end_date: Optional[datetime] = Field(None, description="Filter to date")
    
    class Config:
        json_schema_extra = {
            "example": {
                "pest_type": "Fall Armyworm",
                "min_confidence": 0.7,
                "start_date": "2025-01-01T00:00:00",
                "end_date": "2025-01-31T23:59:59"
            }
        }


class PestStatistics(BaseModel):
    """
    Schema for pest detection statistics.
    Provides summary of detections over time.
    """
    total_detections: int = Field(..., description="Total number of detections")
    unique_pests: int = Field(..., description="Number of unique pest types")
    most_common_pest: Optional[str] = Field(None, description="Most frequently detected pest")
    average_confidence: float = Field(..., description="Average confidence score")
    detections_by_pest: dict = Field(..., description="Count of detections per pest type")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_detections": 25,
                "unique_pests": 3,
                "most_common_pest": "Fall Armyworm",
                "average_confidence": 0.82,
                "detections_by_pest": {
                    "Fall Armyworm": 15,
                    "Aphids": 7,
                    "Whitefly": 3
                }
            }
        }
