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
from models import User, PestDetection
from dependencies.auth import get_current_user
from schemas.pest import (
    PestDetectionResponse,
    ImageUploadResponse,
    PestDetectionAnalysisResponse,
    PestDetectionResult,
    PestDetectionFilter,
    PestStatistics
)
from utils.image_validator import validate_image_or_raise, get_image_dimensions
from utils.file_storage import save_upload_file, generate_file_url

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
    
    # Save primary detection to database
    pest_detection = PestDetection(
        user_id=current_user.id,
        pest_type=primary_detection.pest_type,
        confidence=primary_detection.confidence,
        image_path=f"uploads/{filename}",
        notes=notes
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
