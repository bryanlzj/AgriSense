"""
Pest Report Schemas

Pydantic models for manual pest report API requests and responses.
Used when AI detection fails to identify a pest after multiple attempts.

Learning Notes:
--------------
1. Pest Report Flow:
   - User uploads image for detection
   - Detection fails 3 times (confidence < 50%)
   - System offers manual report option
   - User submits description and severity
   - AI provides best-guess analysis
   - Report saved for future model improvement

2. Observed Severity (User's Assessment):
   - minor: Few pests visible, limited damage
   - moderate: Noticeable presence, some damage
   - severe: Heavy infestation, significant damage

3. AI Response Structure:
   - possible_identification: Best guess based on description
   - general_advice: List of actionable recommendations
   - when_to_seek_help: When to consult experts
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class ObservedSeverityEnum(str, Enum):
    """Severity as observed by the farmer"""
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"


class ReportStatusEnum(str, Enum):
    """Status of the pest report"""
    PENDING = "pending"
    REVIEWED = "reviewed"


class PestReportCreate(BaseModel):
    """
    Schema for creating a manual pest report.
    Used when submitting a report for unidentified pests.
    """
    image_url: str = Field(
        ...,
        description="URL/path to the uploaded image (from failed detection)"
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="User's description of what they observed"
    )
    observed_severity: ObservedSeverityEnum = Field(
        ...,
        description="Severity as observed by farmer: minor, moderate, severe"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "/uploads/pest_images/abc123.jpg",
                "description": "Small green insects on rice leaves, causing yellowing",
                "observed_severity": "moderate"
            }
        }


class AIResponseSchema(BaseModel):
    """
    Schema for AI-generated response in pest reports.
    """
    possible_identification: Optional[str] = Field(
        None,
        description="AI's best-guess identification based on description/image"
    )
    general_advice: List[str] = Field(
        default_factory=list,
        description="List of general pest management recommendations"
    )
    when_to_seek_help: Optional[str] = Field(
        None,
        description="Guidance on when to consult agricultural experts"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "possible_identification": "Based on description, this could be Green Leafhopper or Rice Aphids",
                "general_advice": [
                    "Monitor the affected area daily for changes",
                    "Remove heavily infested leaves carefully",
                    "Consider applying neem oil spray as organic treatment",
                    "Maintain proper field drainage",
                    "Consult local agricultural extension office for confirmation"
                ],
                "when_to_seek_help": "If infestation spreads to more than 20% of plants or damage becomes severe within a week"
            }
        }


class PestReportResponse(BaseModel):
    """
    Schema for pest report response.
    Returns report details with AI analysis.
    """
    id: int = Field(..., description="Report ID")
    user_id: int = Field(..., description="User who submitted the report")
    image_url: str = Field(..., description="Path to uploaded image")
    description: Optional[str] = Field(None, description="User's description")
    observed_severity: str = Field(..., description="Severity observed by farmer")
    ai_response: Optional[AIResponseSchema] = Field(
        None,
        description="AI-generated analysis and recommendations"
    )
    status: str = Field(..., description="Report status: pending, reviewed")
    reported_at: datetime = Field(..., description="When report was submitted")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 15,
                "user_id": 1,
                "image_url": "/uploads/pest_images/abc123.jpg",
                "description": "Small green insects on rice leaves",
                "observed_severity": "moderate",
                "ai_response": {
                    "possible_identification": "Based on description, this could be Green Leafhopper or Rice Aphids",
                    "general_advice": [
                        "Monitor the affected area daily",
                        "Remove heavily infested leaves",
                        "Consider applying neem oil spray",
                        "Consult local agricultural extension office"
                    ],
                    "when_to_seek_help": "If infestation spreads to more than 20% of plants"
                },
                "status": "pending",
                "reported_at": "2025-01-15T14:35:00"
            }
        }


class PestReportListResponse(BaseModel):
    """
    Schema for list of pest reports with pagination.
    """
    total: int = Field(..., description="Total number of reports")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Items per page")
    reports: List[PestReportResponse] = Field(..., description="List of reports")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 5,
                "page": 1,
                "limit": 20,
                "reports": [
                    {
                        "id": 15,
                        "user_id": 1,
                        "image_url": "/uploads/pest_images/abc123.jpg",
                        "description": "Small green insects",
                        "observed_severity": "moderate",
                        "ai_response": {
                            "possible_identification": "Could be Green Leafhopper",
                            "general_advice": ["Monitor daily", "Apply neem spray"],
                            "when_to_seek_help": "If damage increases"
                        },
                        "status": "pending",
                        "reported_at": "2025-01-15T14:35:00"
                    }
                ]
            }
        }


class PestReportSubmitResponse(BaseModel):
    """
    Schema for successful report submission response.
    """
    report_id: int = Field(..., description="Created report ID")
    status: str = Field(default="submitted", description="Submission status")
    message: str = Field(..., description="Success message")
    ai_response: AIResponseSchema = Field(
        ...,
        description="AI-generated best-guess analysis"
    )
    reported_at: datetime = Field(..., description="Submission timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "report_id": 15,
                "status": "submitted",
                "message": "Report submitted successfully. AI has provided general guidance below.",
                "ai_response": {
                    "possible_identification": "Based on description, this could be Green Leafhopper or Rice Aphids",
                    "general_advice": [
                        "Monitor the affected area daily",
                        "Remove heavily infested leaves",
                        "Consider applying neem oil spray",
                        "Consult local agricultural extension office for confirmation"
                    ],
                    "when_to_seek_help": "If infestation spreads to more than 20% of plants"
                },
                "reported_at": "2025-01-15T14:35:00"
            }
        }


# ============================================================================
# LEARNING NOTES: Manual Pest Reports
# ============================================================================

"""
1. Why Manual Reports?
   - AI pest detection isn't 100% accurate
   - Rare or new pests may not be in training data
   - Farmers still need guidance even without positive ID
   - Reports can be used to improve future models

2. AI Response Generation:
   - Uses OpenRouter API to generate best-guess analysis
   - Context includes: image description, severity, crop type
   - Response is general advice, not specific treatment
   - Always recommends consulting experts for severe cases

3. Report Status Flow:
   - PENDING: Just submitted, awaiting any follow-up
   - REVIEWED: Acknowledged or processed

4. Integration Points:
   - POST /pests/report: Submit new report
   - GET /pests/reports: List user's reports
   - Called after 3 failed detection attempts (offer_report=True)

5. Future Improvements:
   - Admin review interface
   - Community identification
   - Feedback loop to improve ML model
"""
