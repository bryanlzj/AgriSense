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
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    image_url: str = Field(..., description="URL to uploaded image")
    recommendations: Optional[str] = Field(None, description="Treatment recommendations")

    @validator('confidence_score')
    def validate_confidence(cls, v):
        """Ensure confidence is between 0 and 1"""
        if not 0.0 <= v <= 1.0:
            raise ValueError('Confidence must be between 0.0 and 1.0')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "pest_type": "Fall Armyworm",
                "confidence_score": 0.87,
                "image_url": "uploads/abc123.jpg",
                "recommendations": "Apply neem oil spray"
            }
        }


class PestDetectionResponse(BaseModel):
    """
    Schema for pest detection response.
    Returns detection results with metadata.
    """
    id: int = Field(..., description="Detection record ID")
    user_id: int = Field(..., description="ID of user who uploaded image")
    pest_type: Optional[str] = Field(None, description="Type of pest detected")
    confidence_score: Optional[float] = Field(None, description="Confidence score (0-1)")
    image_url: str = Field(..., description="URL to access image")
    recommendations: Optional[str] = Field(None, description="Treatment recommendations")
    detected_at: datetime = Field(..., description="Detection timestamp")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "pest_type": "Fall Armyworm",
                "confidence_score": 0.87,
                "image_url": "http://localhost:8000/uploads/abc123.jpg",
                "recommendations": "Apply neem oil spray",
                "detected_at": "2025-01-04T10:30:00"
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


# ============================================================================
# PRD v2: Enhanced Detection Response with Confidence Tiering
# ============================================================================

class DetectionStatus:
    """Detection status constants based on confidence tiering (PRD v2)"""
    DETECTED = "detected"      # >= 70% confidence
    PARTIAL = "partial"        # 50-69% confidence
    UNKNOWN = "unknown"        # < 50% confidence


class DangerLevel:
    """Danger level constants for pest severity"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# Retry tips for failed detections (PRD v2 Section 5.3)
RETRY_TIPS = {
    1: "Image unclear. Please try again with better lighting and focus on the pest.",
    2: "Still having trouble. Tips: Get closer, ensure pest is centered, avoid shadows.",
    3: "Unable to identify. Would you like to report this pest for assistance?"
}


class EnhancedPestDetectionResponse(BaseModel):
    """
    Enhanced pest detection response with confidence tiering (PRD v2).

    Confidence Tiering:
    - >= 70%: Successful detection (status="detected")
    - 50-69%: Partial match (status="partial")
    - < 50%: Unknown (status="unknown")
    """
    # Detection identifiers
    detection_id: Optional[int] = Field(None, description="Saved detection record ID (only if detected)")
    image_url: str = Field(..., description="URL to uploaded image")

    # Status and confidence
    status: str = Field(..., description="Detection status: detected, partial, unknown")
    confidence: float = Field(..., description="Confidence score (0-1)")
    confidence_percent: int = Field(..., description="Confidence as percentage (0-100)")

    # Pest information (if detected or partial)
    pest_name: Optional[str] = Field(None, description="Name of detected pest")
    scientific_name: Optional[str] = Field(None, description="Scientific name of pest")
    description: Optional[str] = Field(None, description="Pest description")
    danger_level: Optional[str] = Field(None, description="Danger level: low, medium, high")

    # AI Recommendations (only for >= 70% confidence)
    recommendations: Optional[List[str]] = Field(None, description="AI-generated treatment recommendations")

    # Retry information
    can_retry: bool = Field(..., description="Whether user can retry detection")
    retry_tip: Optional[str] = Field(None, description="Tip for improving next detection attempt")
    offer_report: bool = Field(False, description="Whether to offer manual report option")

    # Analysis metadata
    analysis_timestamp: datetime = Field(..., description="When analysis was performed")
    all_detections: Optional[List[PestDetectionResult]] = Field(None, description="All detected pests (for debugging)")

    class Config:
        json_schema_extra = {
            "example": {
                "detection_id": 1,
                "image_url": "http://localhost:8000/uploads/abc123.jpg",
                "status": "detected",
                "confidence": 0.87,
                "confidence_percent": 87,
                "pest_name": "Rice Stem Borer",
                "scientific_name": "Scirpophaga incertulas",
                "description": "A major pest of rice that bores into stems",
                "danger_level": "high",
                "recommendations": [
                    "Monitor rice stems for entry holes and frass",
                    "Apply Trichogramma biological control",
                    "Remove and destroy infected stems"
                ],
                "can_retry": False,
                "retry_tip": None,
                "offer_report": False,
                "analysis_timestamp": "2025-01-04T10:30:00",
                "all_detections": None
            }
        }


class PartialDetectionResponse(BaseModel):
    """
    Response for partial detection (50-69% confidence).
    Suggests possible pest but recommends retry or report.
    """
    image_url: str
    status: str = "partial"
    confidence: float
    confidence_percent: int
    possible_pest: str
    message: str = "Detection confidence is low. This might be the pest, but we're not certain."
    can_retry: bool = True
    retry_tip: str
    offer_report: bool = False
    analysis_timestamp: datetime


class UnknownDetectionResponse(BaseModel):
    """
    Response for unknown detection (< 50% confidence).
    Prompts retry with tips, offers manual report after 3 attempts.
    """
    image_url: str
    status: str = "unknown"
    confidence: float
    confidence_percent: int
    message: str = "Unable to identify pest in image."
    can_retry: bool = True
    retry_tip: str
    offer_report: bool  # True after 3 attempts
    analysis_timestamp: datetime


# ============================================================================
# PRD v2: Pest Risk Prediction Schemas (Section 5.4)
# ============================================================================

class WeatherSummarySchema(BaseModel):
    """Current weather conditions used for risk assessment (aligned with Open-Meteo)."""
    temperature: float = Field(..., description="Current temperature in Celsius")
    relative_humidity: float = Field(..., description="Current relative humidity percentage")
    weather_main: str = Field(..., description="Main weather condition")
    weather_description: str = Field(..., description="Detailed weather description")
    recent_rain: bool = Field(False, description="Whether there was recent rainfall")
    location_name: Optional[str] = Field(None, description="Location name")

    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 28.5,
                "relative_humidity": 85,
                "weather_main": "Clouds",
                "weather_description": "scattered clouds",
                "recent_rain": True,
                "location_name": "Kedah"
            }
        }


class RiskLevelInfoSchema(BaseModel):
    """Risk level information for display."""
    label: str = Field(..., description="Human-readable risk label")
    color: str = Field(..., description="Color code for UI display")
    description: str = Field(..., description="Description of risk level")

    class Config:
        json_schema_extra = {
            "example": {
                "label": "Medium",
                "color": "yellow",
                "description": "Moderate risk - increase monitoring frequency"
            }
        }


class ActiveRiskSchema(BaseModel):
    """Individual pest risk that matches current conditions."""
    pest_name: str = Field(..., description="Common name of the pest")
    scientific_name: Optional[str] = Field(None, description="Scientific name")
    risk_level: str = Field(..., description="Risk level: low, medium, high")
    risk_message: str = Field(..., description="Description of risk and pest behavior")
    prevention_tips: List[str] = Field(..., description="Prevention recommendations")
    data_source: Optional[str] = Field(None, description="Source of correlation data")

    class Config:
        json_schema_extra = {
            "example": {
                "pest_name": "Brown Planthopper",
                "scientific_name": "Nilaparvata lugens",
                "risk_level": "high",
                "risk_message": "High humidity and warm temperatures favor Brown Planthopper population explosion.",
                "prevention_tips": [
                    "Avoid excessive nitrogen fertilizer",
                    "Maintain proper plant spacing",
                    "Drain fields periodically",
                    "Use resistant rice varieties"
                ],
                "data_source": "MARDI Rice Pest Guidelines"
            }
        }


class PestRiskAssessmentResponse(BaseModel):
    """
    Complete pest risk assessment response.

    Returns risk assessment based on current weather conditions
    checked against pest-weather correlations for user's crop type.
    """
    status: str = Field(..., description="Assessment status: success or error")
    weather_summary: Optional[WeatherSummarySchema] = Field(None, description="Current weather conditions")
    overall_risk: str = Field(..., description="Overall risk level: none, low, medium, high")
    overall_risk_info: RiskLevelInfoSchema = Field(..., description="Risk level details for display")
    active_risks: List[ActiveRiskSchema] = Field(default_factory=list, description="List of active pest risks")
    total_risks: int = Field(0, description="Total number of active risks")
    crop_type: str = Field(..., description="User's crop type")
    correlations_checked: int = Field(0, description="Number of correlations checked")
    assessed_at: str = Field(..., description="ISO timestamp of assessment")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "weather_summary": {
                    "temperature": 28.5,
                    "humidity": 85,
                    "weather_main": "Clouds",
                    "weather_description": "scattered clouds",
                    "recent_rain": True,
                    "location_name": "Kedah"
                },
                "overall_risk": "high",
                "overall_risk_info": {
                    "label": "High",
                    "color": "red",
                    "description": "High risk - take preventive action immediately"
                },
                "active_risks": [
                    {
                        "pest_name": "Brown Planthopper",
                        "scientific_name": "Nilaparvata lugens",
                        "risk_level": "high",
                        "risk_message": "High humidity favors BPH population explosion.",
                        "prevention_tips": ["Avoid excessive nitrogen", "Drain fields"],
                        "data_source": "MARDI Rice Pest Guidelines"
                    }
                ],
                "total_risks": 1,
                "crop_type": "rice",
                "correlations_checked": 8,
                "assessed_at": "2025-01-09T10:30:00"
            }
        }


class PestRiskSummaryResponse(BaseModel):
    """
    Simplified pest risk summary for dashboard display.
    """
    status: str = Field(..., description="Risk status: safe, caution, warning, critical")
    headline: str = Field(..., description="Short headline for display")
    description: str = Field(..., description="Longer description of current risk")
    action_required: bool = Field(False, description="Whether immediate action is needed")
    top_risk: Optional[ActiveRiskSchema] = Field(None, description="Top risk for quick view")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "warning",
                "headline": "2 Pest Risk Warnings",
                "description": "Weather conditions favor 2 pests. Increase monitoring frequency.",
                "action_required": True,
                "top_risk": {
                    "pest_name": "Brown Planthopper",
                    "risk_level": "high",
                    "risk_message": "High humidity favors population growth.",
                    "prevention_tips": ["Drain fields", "Use resistant varieties"]
                }
            }
        }
