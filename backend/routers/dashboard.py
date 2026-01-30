"""
Dashboard Router

API endpoint for unified dashboard data.
Aggregates weather, alerts, detections, and pest risk into single response.

Learning Notes:
- Single endpoint reduces mobile app API calls
- Aggregates data from multiple services
- Returns everything needed for home screen
"""

from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc

from database import get_db
from models import User, Alert, PestDetection
from dependencies.auth import get_current_user
from schemas.alert import AlertResponse
from services.weather_service import fetch_current_weather, transform_current_weather
from services.pest_risk_service import get_pest_risk_assessment, get_risk_summary_for_display

router = APIRouter(prefix="/dashboard", tags=["Dashboard 📊"])


@router.get("")
async def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get unified dashboard data for home screen.

    **Dashboard Endpoint** 📊

    Returns all data needed for the mobile app home screen in a single request:
    - Weather summary (current conditions)
    - Alert count and recent alerts (top 3)
    - Recent pest detections (top 3)
    - Pest risk status

    This reduces the number of API calls needed to render the home screen.

    **Response Includes:**
    - `weather`: Current weather conditions
    - `alerts`: Count and recent alerts
    - `detections`: Recent pest detections
    - `pest_risk`: Current pest risk status

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/dashboard" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Initialize response data
    response_data = {
        "user": {
            "username": current_user.username,
            "full_name": current_user.full_name,
            "crop_type": current_user.crop_type,
            "farm_location": current_user.farm_location_name
        },
        "weather": None,
        "alerts": {
            "total_unread": 0,
            "recent": []
        },
        "detections": {
            "total_recent": 0,
            "recent": []
        },
        "pest_risk": None,
        "generated_at": datetime.utcnow().isoformat()
    }

    # 1. Get weather summary
    try:
        weather_data = await fetch_current_weather(
            current_user.farm_location_lat,
            current_user.farm_location_lng
        )
        current_weather = transform_current_weather(weather_data)

        response_data["weather"] = {
            "temperature": round(current_weather.temperature, 1),
            "humidity": current_weather.relative_humidity,
            "weather_main": current_weather.weather_main,
            "weather_description": current_weather.weather_description,
            "feels_like": round(current_weather.feels_like, 1),
            "wind_speed": round(current_weather.wind_speed, 1),
            "location": current_user.farm_location_name
        }
    except Exception as e:
        response_data["weather"] = {
            "error": "Failed to fetch weather data",
            "location": current_user.farm_location_name
        }

    # 2. Get alerts summary
    try:
        # Count unread alerts
        unread_count = db.query(Alert).filter(
            Alert.user_id == current_user.id,
            Alert.is_read == False
        ).count()

        # Get recent alerts (top 3)
        recent_alerts = db.query(Alert).filter(
            Alert.user_id == current_user.id
        ).order_by(desc(Alert.created_at)).limit(3).all()

        response_data["alerts"] = {
            "total_unread": unread_count,
            "recent": [
                {
                    "id": alert.id,
                    "type": alert.alert_type.value if alert.alert_type else None,
                    "severity": alert.severity.value if alert.severity else None,
                    "title": alert.title,
                    "message": alert.message[:100] + "..." if len(alert.message) > 100 else alert.message,
                    "is_read": alert.is_read,
                    "created_at": alert.created_at.isoformat() if alert.created_at else None
                }
                for alert in recent_alerts
            ]
        }
    except Exception as e:
        response_data["alerts"] = {
            "total_unread": 0,
            "recent": [],
            "error": str(e)
        }

    # 3. Get recent detections
    try:
        # Get detections from last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)

        recent_detections = db.query(PestDetection).filter(
            PestDetection.user_id == current_user.id,
            PestDetection.detected_at >= seven_days_ago
        ).order_by(desc(PestDetection.detected_at)).limit(3).all()

        total_recent = db.query(PestDetection).filter(
            PestDetection.user_id == current_user.id,
            PestDetection.detected_at >= seven_days_ago
        ).count()

        response_data["detections"] = {
            "total_recent": total_recent,
            "recent": [
                {
                    "id": detection.id,
                    "pest_type": detection.pest_type,
                    "confidence": round(detection.confidence_score, 2) if detection.confidence_score else None,
                    "image_url": detection.image_url,
                    "detected_at": detection.detected_at.isoformat() if detection.detected_at else None
                }
                for detection in recent_detections
            ]
        }
    except Exception as e:
        response_data["detections"] = {
            "total_recent": 0,
            "recent": [],
            "error": str(e)
        }

    # 4. Get pest risk status
    try:
        risk_assessment = await get_pest_risk_assessment(
            db=db,
            user_id=current_user.id,
            crop_type=current_user.crop_type,
            latitude=current_user.farm_location_lat,
            longitude=current_user.farm_location_lng,
            location_name=current_user.farm_location_name
        )

        if risk_assessment.get("status") == "success":
            summary = get_risk_summary_for_display(risk_assessment.get("active_risks", []))

            response_data["pest_risk"] = {
                "status": summary["status"],
                "headline": summary["headline"],
                "description": summary["description"],
                "action_required": summary.get("action_required", False),
                "overall_risk": risk_assessment.get("overall_risk", "none"),
                "total_risks": risk_assessment.get("total_risks", 0)
            }
        else:
            response_data["pest_risk"] = {
                "status": "unknown",
                "headline": "Unable to Assess",
                "description": "Could not assess pest risk at this time.",
                "action_required": False,
                "overall_risk": "unknown",
                "total_risks": 0
            }
    except Exception as e:
        response_data["pest_risk"] = {
            "status": "error",
            "headline": "Error",
            "description": str(e),
            "action_required": False,
            "overall_risk": "unknown",
            "total_risks": 0
        }

    return response_data


@router.get("/quick")
async def get_quick_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get minimal dashboard data for quick loading.

    Returns only essential counts without detailed data.
    Use this for quick status checks or loading indicators.

    **Example:**
    ```bash
    curl "http://localhost:8000/api/v1/dashboard/quick" \\
      -H "Authorization: Bearer YOUR_TOKEN"
    ```
    """
    # Count unread alerts
    unread_alerts = db.query(Alert).filter(
        Alert.user_id == current_user.id,
        Alert.is_read == False
    ).count()

    # Count recent detections (7 days)
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_detections = db.query(PestDetection).filter(
        PestDetection.user_id == current_user.id,
        PestDetection.detected_at >= seven_days_ago
    ).count()

    return {
        "user": current_user.username,
        "crop_type": current_user.crop_type,
        "location": current_user.farm_location_name,
        "unread_alerts": unread_alerts,
        "recent_detections": recent_detections,
        "generated_at": datetime.utcnow().isoformat()
    }


# ============================================================================
# LEARNING NOTES: Dashboard Endpoint
# ============================================================================

"""
1. Why a Dashboard Endpoint?
   - Mobile apps need multiple data sources for home screen
   - Single request is faster than multiple parallel requests
   - Reduces network overhead
   - Better user experience (less loading)

2. What's Included:
   - User profile summary
   - Current weather conditions
   - Alert count and recent alerts
   - Recent pest detections
   - Pest risk status

3. Error Handling:
   - Each section has its own try/except
   - Partial failures don't break entire response
   - Error info included in response for debugging

4. Performance Tips:
   - Use /dashboard/quick for loading states
   - Cache weather data (already cached in weather service)
   - Consider caching entire dashboard response
"""
