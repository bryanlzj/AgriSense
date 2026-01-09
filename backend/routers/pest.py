"""
Pest Detection Router

API endpoints for pest detection and image upload.
This is one of the TWO CORE FEATURES of AgriSense.

Learning Notes:
--------------
1. File Upload in FastAPI:
   - Use UploadFile type for file uploads
   - Supports multipart/form-data
   - Async file operations for better performance
   
2. Image Processing Flow:
   - Validate image (type, size, dimensions)
   - Save to disk with unique filename
   - Process with ML model (mock for now)
   - Save detection results to database
   - Return results to user
   
3. CORE FEATURE Status:
   - This is CORE FEATURE #2: Pest Risk Management
   - Equal priority to Weather Early Warning
   - Critical for MVP and demo
"""

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query, Request
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from database import get_db
from models import User, PestDetection, PestReport
from dependencies.auth import get_current_user
from schemas.pest import (
    PestDetectionResponse,
    ImageUploadResponse,
    PestDetectionAnalysisResponse,
    PestDetectionResult,
    PestDetectionFilter,
    PestStatistics,
    EnhancedPestDetectionResponse,
    DetectionStatus,
    DangerLevel,
    RETRY_TIPS,
    PestRiskAssessmentResponse,
    PestRiskSummaryResponse,
    WeatherSummarySchema,
    RiskLevelInfoSchema,
    ActiveRiskSchema
)
from schemas.pest_report import (
    PestReportCreate,
    PestReportResponse,
    PestReportListResponse,
    PestReportSubmitResponse,
    AIResponseSchema
)
from models.pest_detection import SeverityLevel
from utils.image_validator import validate_image_or_raise, get_image_dimensions
from utils.file_storage import save_upload_file, generate_file_url
from services.ai_service import (
    get_pest_recommendations,
    get_pest_report_analysis,
    is_ai_available
)
from services.pest_risk_service import (
    get_pest_risk_assessment,
    get_risk_summary_for_display
)

router = APIRouter(prefix="/pest", tags=["Pest Detection 🐛"])


@router.post("/upload", response_model=ImageUploadResponse, status_code=201)
async def upload_pest_image(
    request: Request,
    file: UploadFile = File(..., description="Image file (JPEG/PNG, max 5MB, min 224x224)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload an image for pest detection.
    
    **CORE FEATURE #2: Pest Risk Management** 🐛
    
    This endpoint handles image upload for pest detection analysis.
    The image is validated, saved to disk, and prepared for ML analysis.
    
    **Validations:**
    - File type: JPEG or PNG only
    - File size: Maximum 5MB
    - Image dimensions: Minimum 224x224 pixels (required for ML model)
    
    **Returns:**
    - Unique filename and file path
    - Image URL for access
    - Image dimensions and file size
    
    **Next Step:**
    - Use the returned filename with `/pest/analyze` endpoint
    - Or use `/pest/detect` to upload and analyze in one step
    
    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/pest/upload" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -F "file=@pest_image.jpg"
    ```
    """
    # Validate image
    await validate_image_or_raise(file)
    
    # Get image dimensions
    width, height = await get_image_dimensions(file)
    
    # Save file to disk
    filename, file_path = await save_upload_file(file)
    
    # Generate URL for accessing the file
    base_url = str(request.base_url).rstrip('/')
    file_url = generate_file_url(filename, base_url)
    
    return ImageUploadResponse(
        filename=filename,
        file_path=f"/uploads/{filename}",
        file_url=file_url,
        file_size=file.size,
        width=width,
        height=height,
        message="Image uploaded successfully. Use /pest/analyze to detect pests."
    )


@router.post("/detect", response_model=PestDetectionAnalysisResponse, status_code=201)
async def detect_pest(
    request: Request,
    file: UploadFile = File(..., description="Image file (JPEG/PNG, max 5MB, min 224x224)"),
    notes: Optional[str] = Query(None, description="Optional notes about the image"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload image and detect pests in one step.
    
    **CORE FEATURE #2: Pest Risk Management** 🐛
    
    This endpoint combines image upload and pest detection analysis.
    It validates the image, saves it, runs ML analysis, and saves results to database.
    
    **Process:**
    1. Validate and save image
    2. Run ML model for pest detection (mock for now)
    3. Save detection results to database
    4. Return analysis results
    
    **Mock ML Results:**
    - Currently returns mock predictions
    - Real ML model will be integrated in Phase 2
    - Mock results include common pests: Fall Armyworm, Aphids, Whitefly
    
    **Returns:**
    - Detection ID (saved in database)
    - Image URL
    - List of detected pests with confidence scores
    - Primary detection (highest confidence)
    
    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/pest/detect" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -F "file=@pest_image.jpg" \\
      -F "notes=Found on corn leaves"
    ```
    """
    # Validate and save image
    await validate_image_or_raise(file)
    filename, file_path = await save_upload_file(file)
    
    # Generate URL
    base_url = str(request.base_url).rstrip('/')
    file_url = generate_file_url(filename, base_url)
    
    # Mock ML detection (will be replaced with real ML in Phase 2)
    # For now, return mock results
    import random
    
    pest_types = [
        ("Fall Armyworm", "A major pest of corn and other crops"),
        ("Aphids", "Small sap-sucking insects that damage plants"),
        ("Whitefly", "Small white flying insects that spread diseases"),
        ("Leaf Miner", "Creates tunnels in leaves"),
        ("Thrips", "Tiny insects that damage flowers and leaves")
    ]
    
    # Generate mock detections
    detections = []
    for pest_name, description in pest_types[:3]:  # Return top 3
        confidence = random.uniform(0.1, 0.95)
        detections.append(PestDetectionResult(
            pest_type=pest_name,
            confidence=round(confidence, 2),
            description=description
        ))
    
    # Sort by confidence (highest first)
    detections.sort(key=lambda x: x.confidence, reverse=True)
    primary_detection = detections[0]
    
    # Save primary detection to database (use correct model field names)
    pest_detection = PestDetection(
        user_id=current_user.id,
        pest_type=primary_detection.pest_type,
        confidence_score=primary_detection.confidence,
        image_url=f"uploads/{filename}",
        recommendations=notes
    )
    db.add(pest_detection)
    db.commit()
    db.refresh(pest_detection)
    
    return PestDetectionAnalysisResponse(
        detection_id=pest_detection.id,
        image_url=file_url,
        detections=detections,
        primary_detection=primary_detection,
        analysis_timestamp=pest_detection.created_at
    )


# ============================================================================
# PRD v2: Enhanced Detection with Confidence Tiering
# ============================================================================

# Mock pest database with detailed info (will be replaced with real ML model)
# Maps pest names to their info including severity (using SeverityLevel enum for database)
PEST_DATABASE = {
    "Rice Stem Borer": {
        "scientific_name": "Scirpophaga incertulas",
        "description": "A major pest of rice that bores into stems, causing deadhearts and whiteheads.",
        "danger_level": DangerLevel.HIGH,
        "severity_enum": SeverityLevel.HIGH,
        "recommendations": [
            "Monitor rice stems for entry holes and frass",
            "Apply Trichogramma biological control",
            "Remove and destroy infected stems",
            "Avoid excessive nitrogen fertilizer"
        ]
    },
    "Rice Leaf Folder": {
        "scientific_name": "Cnaphalocrocis medinalis",
        "description": "Larvae fold rice leaves and feed inside, reducing photosynthesis.",
        "danger_level": DangerLevel.MEDIUM,
        "severity_enum": SeverityLevel.MEDIUM,
        "recommendations": [
            "Scout for folded leaves with larvae inside",
            "Maintain field hygiene",
            "Avoid dense planting",
            "Apply neem-based spray if >10% damage"
        ]
    },
    "Brown Planthopper": {
        "scientific_name": "Nilaparvata lugens",
        "description": "Sap-sucking pest that causes hopper burn in rice fields.",
        "danger_level": DangerLevel.HIGH,
        "severity_enum": SeverityLevel.HIGH,
        "recommendations": [
            "Avoid excessive nitrogen application",
            "Maintain proper plant spacing",
            "Drain fields periodically",
            "Use resistant varieties if available"
        ]
    },
    "Rice Bug": {
        "scientific_name": "Leptocorisa oratorius",
        "description": "Attacks rice during grain filling, causing empty or discolored grains.",
        "danger_level": DangerLevel.MEDIUM,
        "severity_enum": SeverityLevel.MEDIUM,
        "recommendations": [
            "Monitor during flowering and grain filling",
            "Remove weeds around field",
            "Early morning collection when bugs are sluggish",
            "Apply insecticide if >5 bugs per hill"
        ]
    },
    "Green Leafhopper": {
        "scientific_name": "Nephotettix virescens",
        "description": "Vector for tungro virus disease, common in warm humid conditions.",
        "danger_level": DangerLevel.MEDIUM,
        "severity_enum": SeverityLevel.MEDIUM,
        "recommendations": [
            "Monitor for hopper populations",
            "Remove infected plants immediately",
            "Synchronize planting in area",
            "Use resistant varieties"
        ]
    }
}


@router.post("/detect/enhanced", response_model=EnhancedPestDetectionResponse, status_code=201)
async def detect_pest_enhanced(
    request: Request,
    file: UploadFile = File(..., description="Image file (JPEG/PNG, max 5MB, min 224x224)"),
    retry_count: int = Query(0, ge=0, le=3, description="Number of previous retry attempts"),
    notes: Optional[str] = Query(None, description="Optional notes about the image"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Enhanced pest detection with confidence tiering (PRD v2).

    **CORE FEATURE #2: Pest Risk Management** 🐛

    This endpoint implements the PRD v2 confidence tiering system:

    **Confidence Tiering:**
    | Confidence | Status | Response |
    |------------|--------|----------|
    | >= 70% | detected | Full pest info + AI recommendations |
    | 50-69% | partial | Possible pest + retry suggestion |
    | < 50% | unknown | Retry tips, manual report after 3 attempts |

    **Retry System:**
    - Pass `retry_count` to track attempts (0-3)
    - After 3 failed attempts, `offer_report=true` suggests manual reporting

    **Parameters:**
    - `file`: Image file (JPEG/PNG)
    - `retry_count`: Number of previous attempts (default: 0)
    - `notes`: Optional description

    **Example:**
    ```bash
    # First attempt
    curl -X POST "http://localhost:8000/api/v1/pest/detect/enhanced" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -F "file=@pest_image.jpg"

    # Retry after failed attempt
    curl -X POST "http://localhost:8000/api/v1/pest/detect/enhanced?retry_count=1" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -F "file=@pest_image.jpg"
    ```
    """
    # Validate and save image
    await validate_image_or_raise(file)
    filename, file_path = await save_upload_file(file)

    # Generate URL
    base_url = str(request.base_url).rstrip('/')
    file_url = generate_file_url(filename, base_url)

    # Mock ML detection (will be replaced with real ML model)
    import random

    pest_names = list(PEST_DATABASE.keys())

    # Generate mock confidence (biased towards different ranges for testing)
    # In production, this comes from the ML model
    confidence = random.uniform(0.3, 0.95)

    # Select a pest (in production, ML model determines this)
    selected_pest = random.choice(pest_names)
    pest_info = PEST_DATABASE[selected_pest]

    # Determine status based on confidence tiering (PRD v2)
    confidence_percent = int(confidence * 100)

    if confidence >= 0.70:
        # DETECTED: >= 70% confidence
        status = DetectionStatus.DETECTED

        # Get AI-generated recommendations
        ai_recommendations = await get_pest_recommendations(
            pest_name=selected_pest,
            confidence=confidence,
            crop_type=current_user.crop_type,
            location=current_user.farm_location_name
        )

        # Use AI recommendations if available, otherwise fall back to static
        recommendations = ai_recommendations.get(
            "recommendations",
            pest_info["recommendations"]
        )

        # Save detection to database (use correct model field names)
        pest_detection = PestDetection(
            user_id=current_user.id,
            pest_type=selected_pest,
            confidence_score=confidence,
            image_url=f"uploads/{filename}",
            recommendations=notes,
            severity_level=pest_info["severity_enum"]
        )
        db.add(pest_detection)
        db.commit()
        db.refresh(pest_detection)

        return EnhancedPestDetectionResponse(
            detection_id=pest_detection.id,
            image_url=file_url,
            status=status,
            confidence=round(confidence, 2),
            confidence_percent=confidence_percent,
            pest_name=selected_pest,
            scientific_name=pest_info["scientific_name"],
            description=pest_info["description"],
            danger_level=pest_info["danger_level"],
            recommendations=recommendations,
            can_retry=False,
            retry_tip=None,
            offer_report=False,
            analysis_timestamp=datetime.utcnow()
        )

    elif confidence >= 0.50:
        # PARTIAL: 50-69% confidence
        status = DetectionStatus.PARTIAL
        retry_tip = RETRY_TIPS.get(retry_count + 1, RETRY_TIPS[1])

        return EnhancedPestDetectionResponse(
            detection_id=None,  # Not saved to database
            image_url=file_url,
            status=status,
            confidence=round(confidence, 2),
            confidence_percent=confidence_percent,
            pest_name=selected_pest,
            scientific_name=pest_info["scientific_name"],
            description=f"Possible match: {pest_info['description']}",
            danger_level=pest_info["danger_level"],
            recommendations=None,  # No recommendations for partial match
            can_retry=True,
            retry_tip=retry_tip,
            offer_report=retry_count >= 2,
            analysis_timestamp=datetime.utcnow()
        )

    else:
        # UNKNOWN: < 50% confidence
        status = DetectionStatus.UNKNOWN
        offer_report = retry_count >= 2
        retry_tip = RETRY_TIPS.get(retry_count + 1, RETRY_TIPS[3])

        return EnhancedPestDetectionResponse(
            detection_id=None,
            image_url=file_url,
            status=status,
            confidence=round(confidence, 2),
            confidence_percent=confidence_percent,
            pest_name=None,
            scientific_name=None,
            description="Unable to identify pest in image.",
            danger_level=None,
            recommendations=None,
            can_retry=True,
            retry_tip=retry_tip,
            offer_report=offer_report,
            analysis_timestamp=datetime.utcnow()
        )


@router.get("/", response_model=List[PestDetectionResponse])
def get_pest_detections(
    request: Request,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    pest_type: Optional[str] = Query(None, description="Filter by pest type"),
    min_confidence: Optional[float] = Query(None, ge=0.0, le=1.0, description="Minimum confidence score"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of pest detections for current user.
    
    Supports filtering by pest type and minimum confidence score.
    Results are ordered by detection date (newest first).
    
    **Query Parameters:**
    - `skip`: Number of records to skip (for pagination)
    - `limit`: Maximum records to return (default 100, max 1000)
    - `pest_type`: Filter by specific pest type
    - `min_confidence`: Filter by minimum confidence score
    
    **Example:**
    ```bash
    # Get all detections
    curl "http://localhost:8000/api/v1/pest/" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    
    # Get Fall Armyworm detections with confidence > 0.7
    curl "http://localhost:8000/api/v1/pest/?pest_type=Fall%20Armyworm&min_confidence=0.7" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Build query
    query = db.query(PestDetection).filter(PestDetection.user_id == current_user.id)
    
    # Apply filters
    if pest_type:
        query = query.filter(PestDetection.pest_type == pest_type)
    
    if min_confidence is not None:
        query = query.filter(PestDetection.confidence >= min_confidence)
    
    # Order by newest first
    query = query.order_by(desc(PestDetection.created_at))
    
    # Apply pagination
    detections = query.offset(skip).limit(limit).all()
    
    # Generate URLs for each detection
    base_url = str(request.base_url).rstrip('/')
    results = []
    for detection in detections:
        # Extract filename from image_path
        filename = detection.image_path.split('/')[-1]
        image_url = generate_file_url(filename, base_url)
        
        results.append(PestDetectionResponse(
            id=detection.id,
            user_id=detection.user_id,
            pest_type=detection.pest_type,
            confidence=detection.confidence,
            image_path=detection.image_path,
            image_url=image_url,
            notes=detection.notes,
            created_at=detection.created_at
        ))
    
    return results


@router.get("/{detection_id}", response_model=PestDetectionResponse)
def get_pest_detection(
    detection_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific pest detection by ID.
    
    Users can only access their own detections.
    
    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/pest/1" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    detection = db.query(PestDetection).filter(
        PestDetection.id == detection_id,
        PestDetection.user_id == current_user.id
    ).first()
    
    if not detection:
        raise HTTPException(status_code=404, detail="Pest detection not found")
    
    # Generate image URL
    base_url = str(request.base_url).rstrip('/')
    filename = detection.image_path.split('/')[-1]
    image_url = generate_file_url(filename, base_url)
    
    return PestDetectionResponse(
        id=detection.id,
        user_id=detection.user_id,
        pest_type=detection.pest_type,
        confidence=detection.confidence,
        image_path=detection.image_path,
        image_url=image_url,
        notes=detection.notes,
        created_at=detection.created_at
    )


@router.delete("/{detection_id}", status_code=204)
def delete_pest_detection(
    detection_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a pest detection record.
    
    Users can only delete their own detections.
    Note: This does not delete the image file from disk.
    
    **Example:**
    ```bash
    curl -X DELETE "http://localhost:8000/api/v1/pest/1" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    detection = db.query(PestDetection).filter(
        PestDetection.id == detection_id,
        PestDetection.user_id == current_user.id
    ).first()
    
    if not detection:
        raise HTTPException(status_code=404, detail="Pest detection not found")
    
    db.delete(detection)
    db.commit()
    
    return None


@router.get("/stats/summary", response_model=PestStatistics)
def get_pest_statistics(
    days: int = Query(30, ge=1, le=365, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get pest detection statistics for current user.
    
    Provides summary of detections over specified time period.
    
    **Statistics Include:**
    - Total number of detections
    - Number of unique pest types detected
    - Most common pest
    - Average confidence score
    - Count of detections per pest type
    
    **Example:**
    ```bash
    # Get stats for last 30 days
    curl "http://localhost:8000/api/v1/pest/stats/summary?days=30" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Calculate date range
    from datetime import timedelta
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Get detections in date range
    detections = db.query(PestDetection).filter(
        PestDetection.user_id == current_user.id,
        PestDetection.created_at >= start_date
    ).all()
    
    if not detections:
        return PestStatistics(
            total_detections=0,
            unique_pests=0,
            most_common_pest=None,
            average_confidence=0.0,
            detections_by_pest={}
        )
    
    # Calculate statistics
    total_detections = len(detections)
    
    # Count detections by pest type
    detections_by_pest = {}
    total_confidence = 0.0
    
    for detection in detections:
        pest_type = detection.pest_type
        detections_by_pest[pest_type] = detections_by_pest.get(pest_type, 0) + 1
        total_confidence += detection.confidence
    
    unique_pests = len(detections_by_pest)
    most_common_pest = max(detections_by_pest, key=detections_by_pest.get) if detections_by_pest else None
    average_confidence = round(total_confidence / total_detections, 2)
    
    return PestStatistics(
        total_detections=total_detections,
        unique_pests=unique_pests,
        most_common_pest=most_common_pest,
        average_confidence=average_confidence,
        detections_by_pest=detections_by_pest
    )


# ============================================================================
# PRD v2: Pest Risk Prediction (Section 5.4)
# ============================================================================

@router.get("/risk", response_model=PestRiskAssessmentResponse)
async def get_pest_risk(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current pest risk assessment based on weather conditions.

    **CORE FEATURE #2: Pest Risk Management** 🐛

    This endpoint predicts pest outbreak risk by checking current weather
    conditions against known pest-weather correlations for the user's crop.

    **How it Works:**
    1. Fetches current weather for user's farm location
    2. Queries pest-weather correlations for user's crop type
    3. Checks each correlation against current conditions
    4. Returns matching risks with prevention tips

    **Risk Levels:**
    | Level | Action Required |
    |-------|----------------|
    | none | No significant risk |
    | low | Monitor situation |
    | medium | Increase monitoring |
    | high | Take preventive action |

    **Response Includes:**
    - Weather summary (current conditions)
    - Overall risk level
    - List of active pest risks
    - Prevention tips from agricultural sources (MARDI, IRRI)

    **Note:** Prevention tips come from database (not AI-generated) to ensure
    consistent, vetted agricultural advice.

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/pest/risk" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Get pest risk assessment using user's location and crop type
    assessment = await get_pest_risk_assessment(
        db=db,
        user_id=current_user.id,
        crop_type=current_user.crop_type,
        latitude=current_user.farm_location_lat,
        longitude=current_user.farm_location_lng,
        location_name=current_user.farm_location_name
    )

    # Handle error case
    if assessment.get("status") == "error":
        raise HTTPException(
            status_code=503,
            detail=assessment.get("error_message", "Failed to assess pest risk")
        )

    # Build response with proper schema types
    weather_summary = None
    if assessment.get("weather_summary"):
        ws = assessment["weather_summary"]
        weather_summary = WeatherSummarySchema(
            temperature=ws["temperature"],
            humidity=ws["humidity"],
            weather_main=ws["weather_main"],
            weather_description=ws["weather_description"],
            recent_rain=ws.get("recent_rain", False),
            location_name=ws.get("location_name")
        )

    risk_info = assessment.get("overall_risk_info", {})
    overall_risk_info = RiskLevelInfoSchema(
        label=risk_info.get("label", "None"),
        color=risk_info.get("color", "green"),
        description=risk_info.get("description", "No significant risk")
    )

    active_risks = []
    for risk in assessment.get("active_risks", []):
        active_risks.append(ActiveRiskSchema(
            pest_name=risk["pest_name"],
            scientific_name=risk.get("scientific_name"),
            risk_level=risk["risk_level"],
            risk_message=risk["risk_message"],
            prevention_tips=risk["prevention_tips"],
            data_source=risk.get("data_source")
        ))

    return PestRiskAssessmentResponse(
        status="success",
        weather_summary=weather_summary,
        overall_risk=assessment.get("overall_risk", "none"),
        overall_risk_info=overall_risk_info,
        active_risks=active_risks,
        total_risks=assessment.get("total_risks", 0),
        crop_type=assessment.get("crop_type", current_user.crop_type),
        correlations_checked=assessment.get("correlations_checked", 0),
        assessed_at=assessment.get("assessed_at", datetime.utcnow().isoformat())
    )


@router.get("/risk/summary", response_model=PestRiskSummaryResponse)
async def get_pest_risk_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get simplified pest risk summary for dashboard display.

    Returns a concise summary suitable for displaying on a dashboard card.

    **Response Includes:**
    - Status: safe, caution, warning, critical
    - Headline: Short text for display
    - Description: Longer explanation
    - Action required: Boolean indicator
    - Top risk: Most urgent risk (if any)

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/pest/risk/summary" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Get full assessment
    assessment = await get_pest_risk_assessment(
        db=db,
        user_id=current_user.id,
        crop_type=current_user.crop_type,
        latitude=current_user.farm_location_lat,
        longitude=current_user.farm_location_lng,
        location_name=current_user.farm_location_name
    )

    # Handle error case
    if assessment.get("status") == "error":
        return PestRiskSummaryResponse(
            status="unknown",
            headline="Unable to Assess Risk",
            description="Could not fetch weather data to assess pest risk.",
            action_required=False,
            top_risk=None
        )

    # Get summary for display
    summary = get_risk_summary_for_display(assessment.get("active_risks", []))

    # Convert top_risk to schema if present
    top_risk = None
    if summary.get("top_risk"):
        tr = summary["top_risk"]
        top_risk = ActiveRiskSchema(
            pest_name=tr["pest_name"],
            scientific_name=tr.get("scientific_name"),
            risk_level=tr["risk_level"],
            risk_message=tr["risk_message"],
            prevention_tips=tr["prevention_tips"],
            data_source=tr.get("data_source")
        )

    return PestRiskSummaryResponse(
        status=summary["status"],
        headline=summary["headline"],
        description=summary["description"],
        action_required=summary.get("action_required", False),
        top_risk=top_risk
    )


# ============================================================================
# PRD v2: Manual Pest Reports (Section 5.5)
# ============================================================================

@router.post("/report", response_model=PestReportSubmitResponse, status_code=201)
async def submit_pest_report(
    report_data: PestReportCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Submit a manual pest report when AI detection fails.

    **FALLBACK FEATURE: Manual Pest Reporting** 📝

    This endpoint is used when pest detection fails after multiple attempts.
    The farmer can submit a manual report with description and observed severity,
    and receive AI-generated best-guess analysis and general advice.

    **When to Use:**
    - After 3 failed detection attempts (offer_report=true)
    - When farmer wants to report pest manually

    **Request Body:**
    - `image_url`: Path to the uploaded image (from failed detection)
    - `description`: Optional description of what was observed
    - `observed_severity`: Farmer's assessment (minor, moderate, severe)

    **Response:**
    - AI-generated possible identification
    - General pest management advice
    - Guidance on when to seek expert help

    **Example:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/pest/report" \\
      -H "Authorization: Bearer YOUR_TOKEN" \\
      -H "Content-Type: application/json" \\
      -d '{
        "image_url": "/uploads/pest_images/abc123.jpg",
        "description": "Small green insects on rice leaves",
        "observed_severity": "moderate"
      }'
    ```
    """
    # Get AI-generated analysis for the pest report
    # Uses OpenRouter API if configured, falls back to mock responses
    ai_response = await get_pest_report_analysis(
        description=report_data.description,
        observed_severity=report_data.observed_severity,
        crop_type=current_user.crop_type,
        location=current_user.farm_location_name
    )

    # Create pest report record
    pest_report = PestReport(
        user_id=current_user.id,
        image_url=report_data.image_url,
        description=report_data.description,
        observed_severity=report_data.observed_severity,
        ai_response=ai_response,
        status="pending"
    )
    db.add(pest_report)
    db.commit()
    db.refresh(pest_report)

    return PestReportSubmitResponse(
        report_id=pest_report.id,
        status="submitted",
        message="Report submitted successfully. AI has provided general guidance below.",
        ai_response=AIResponseSchema(**ai_response),
        reported_at=pest_report.reported_at
    )


@router.get("/reports", response_model=PestReportListResponse)
def get_pest_reports(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    status: Optional[str] = Query(None, description="Filter by status (pending, reviewed)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get list of manual pest reports for current user.

    **Query Parameters:**
    - `page`: Page number (default: 1)
    - `limit`: Items per page (default: 20, max: 100)
    - `status`: Filter by status (pending, reviewed)

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/pest/reports" \\
      -H "Authorization: Bearer YOUR_TOKEN"

    # Filter by pending reports
    curl "http://localhost:8000/api/v1/pest/reports?status=pending" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Build query
    query = db.query(PestReport).filter(PestReport.user_id == current_user.id)

    # Apply status filter
    if status:
        query = query.filter(PestReport.status == status)

    # Get total count
    total = query.count()

    # Apply pagination
    skip = (page - 1) * limit
    reports = query.order_by(desc(PestReport.reported_at)).offset(skip).limit(limit).all()

    # Convert to response format
    report_responses = []
    for report in reports:
        ai_resp = None
        if report.ai_response:
            ai_resp = AIResponseSchema(**report.ai_response)

        report_responses.append(PestReportResponse(
            id=report.id,
            user_id=report.user_id,
            image_url=report.image_url,
            description=report.description,
            observed_severity=report.observed_severity,
            ai_response=ai_resp,
            status=report.status,
            reported_at=report.reported_at
        ))

    return PestReportListResponse(
        total=total,
        page=page,
        limit=limit,
        reports=report_responses
    )


@router.get("/reports/{report_id}", response_model=PestReportResponse)
def get_pest_report(
    report_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific pest report by ID.

    Users can only access their own reports.

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/pest/reports/15" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    report = db.query(PestReport).filter(
        PestReport.id == report_id,
        PestReport.user_id == current_user.id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Pest report not found")

    ai_resp = None
    if report.ai_response:
        ai_resp = AIResponseSchema(**report.ai_response)

    return PestReportResponse(
        id=report.id,
        user_id=report.user_id,
        image_url=report.image_url,
        description=report.description,
        observed_severity=report.observed_severity,
        ai_response=ai_resp,
        status=report.status,
        reported_at=report.reported_at
    )


# ============================================================================
# AI Service Integration Notes
# ============================================================================
# The pest report and detection endpoints now use the AI service from
# services/ai_service.py which:
# 1. Calls OpenRouter API when configured (OPENROUTER_API_KEY set)
# 2. Falls back to mock responses when API not configured
# 3. Handles rate limiting and errors gracefully
#
# Key functions used:
# - get_pest_recommendations(): For detected pests (≥70% confidence)
# - get_pest_report_analysis(): For manual pest reports
#
# See services/ai_service.py for implementation details.
