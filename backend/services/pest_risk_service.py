"""
Pest Risk Prediction Service

This service predicts pest outbreak risk based on weather conditions.
Uses pest-weather correlations from database to assess current risk.

Learning Notes:
- Pest risk is predicted based on weather patterns
- Each pest has specific weather conditions that favor outbreaks
- Risk assessment uses stored correlations, NOT AI API (per PRD v2)
- Prevention tips come from database (vetted by agricultural sources)

PRD v2 Integration:
- This is part of CORE FEATURE #2: Pest Risk Management
- Uses stored prevention_tips from pest_weather_correlations table
- Does NOT call AI API (saves cost, ensures consistent advice)
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import JSONB

from models.pest_weather_correlation import PestWeatherCorrelation
from models.alert import Alert
from schemas.alert import AlertType, AlertSeverity

# Logger
logger = logging.getLogger(__name__)


# ============================================================================
# RISK LEVEL DEFINITIONS
# ============================================================================

RISK_LEVELS = {
    "low": {
        "value": 1,
        "label": "Low",
        "color": "green",
        "description": "Minor risk - continue regular monitoring"
    },
    "medium": {
        "value": 2,
        "label": "Medium",
        "color": "yellow",
        "description": "Moderate risk - increase monitoring frequency"
    },
    "high": {
        "value": 3,
        "label": "High",
        "color": "red",
        "description": "High risk - take preventive action immediately"
    }
}


# ============================================================================
# PEST RISK ASSESSMENT
# ============================================================================

def get_correlations_for_crop(
    db: Session,
    crop_type: str
) -> List[PestWeatherCorrelation]:
    """
    Get all pest-weather correlations that affect the given crop type.

    Args:
        db: Database session
        crop_type: User's crop type (rice, vegetables, etc.)

    Returns:
        List of matching correlations
    """
    # Query correlations where affected_crops contains the user's crop
    # PostgreSQL JSONB containment operator: @>
    correlations = db.query(PestWeatherCorrelation).filter(
        PestWeatherCorrelation.affected_crops.contains([crop_type])
    ).all()

    return correlations


def assess_pest_risk(
    correlations: List[PestWeatherCorrelation],
    temperature: float,
    relative_humidity: float,
    recent_rain: bool = False
) -> Dict[str, Any]:
    """
    Assess pest risk based on current weather conditions.

    Args:
        correlations: List of pest-weather correlations to check
        temperature: Current temperature in Celsius
        relative_humidity: Current relative humidity percentage
        recent_rain: Whether there was recent rainfall

    Returns:
        dict: Risk assessment including:
            - overall_risk: Highest risk level found
            - risks: List of matching pest risks
            - conditions_checked: Weather parameters used
    """
    matching_risks = []

    for correlation in correlations:
        if correlation.matches_weather(temperature, relative_humidity, recent_rain):
            risk_info = {
                "pest_name": correlation.pest_name,
                "scientific_name": correlation.scientific_name,
                "risk_level": correlation.risk_level,
                "risk_message": correlation.risk_message,
                "prevention_tips": correlation.prevention_tips,
                "data_source": correlation.data_source
            }
            matching_risks.append(risk_info)

    # Determine overall risk (highest among matching)
    if not matching_risks:
        overall_risk = "none"
    else:
        risk_values = [RISK_LEVELS.get(r["risk_level"], {"value": 0})["value"] for r in matching_risks]
        max_risk_value = max(risk_values)
        for level, info in RISK_LEVELS.items():
            if info["value"] == max_risk_value:
                overall_risk = level
                break

    return {
        "overall_risk": overall_risk,
        "overall_risk_info": RISK_LEVELS.get(overall_risk, {
            "label": "None",
            "color": "green",
            "description": "No significant pest risk detected"
        }),
        "active_risks": matching_risks,
        "total_risks": len(matching_risks),
        "conditions_checked": {
            "temperature": temperature,
            "relative_humidity": relative_humidity,
            "recent_rain": recent_rain
        },
        "assessed_at": datetime.utcnow().isoformat()
    }


async def get_pest_risk_assessment(
    db: Session,
    user_id: int,
    crop_type: str,
    latitude: float,
    longitude: float,
    location_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get complete pest risk assessment for a user's location.

    This is the main entry point for pest risk prediction.
    It fetches current weather and checks against correlations.

    Args:
        db: Database session
        user_id: User ID
        crop_type: User's crop type
        latitude: Farm latitude
        longitude: Farm longitude
        location_name: Optional location name

    Returns:
        dict: Complete pest risk assessment with weather and risks
    """
    from services.weather_service import fetch_current_weather, transform_current_weather

    # Fetch current weather
    try:
        weather_data = await fetch_current_weather(latitude, longitude)
        current_weather = transform_current_weather(weather_data)

        temperature = current_weather.temperature
        relative_humidity = current_weather.relative_humidity
        recent_rain = bool(current_weather.rain and current_weather.rain > 0)

        weather_summary = {
            "temperature": temperature,
            "relative_humidity": relative_humidity,
            "weather_main": current_weather.weather_main,
            "weather_description": current_weather.weather_description,
            "recent_rain": recent_rain,
            "location_name": location_name
        }
    except Exception as e:
        logger.error(f"Failed to fetch weather for pest risk assessment: {e}")
        # Return with error status if weather fetch fails
        return {
            "status": "error",
            "error_message": "Failed to fetch current weather data",
            "overall_risk": "unknown",
            "active_risks": [],
            "assessed_at": datetime.utcnow().isoformat()
        }

    # Get correlations for user's crop type
    correlations = get_correlations_for_crop(db, crop_type)

    if not correlations:
        logger.warning(f"No pest correlations found for crop type: {crop_type}")
        return {
            "status": "success",
            "weather_summary": weather_summary,
            "overall_risk": "none",
            "overall_risk_info": {
                "label": "None",
                "color": "green",
                "description": "No pest correlation data available for this crop"
            },
            "active_risks": [],
            "total_risks": 0,
            "crop_type": crop_type,
            "assessed_at": datetime.utcnow().isoformat()
        }

    # Assess risk
    assessment = assess_pest_risk(
        correlations=correlations,
        temperature=temperature,
        relative_humidity=relative_humidity,
        recent_rain=recent_rain
    )

    return {
        "status": "success",
        "weather_summary": weather_summary,
        "overall_risk": assessment["overall_risk"],
        "overall_risk_info": assessment["overall_risk_info"],
        "active_risks": assessment["active_risks"],
        "total_risks": assessment["total_risks"],
        "crop_type": crop_type,
        "correlations_checked": len(correlations),
        "assessed_at": assessment["assessed_at"]
    }


# ============================================================================
# PEST RISK ALERTS
# ============================================================================

def create_pest_risk_alert(
    db: Session,
    user_id: int,
    correlation: PestWeatherCorrelation,
    weather_conditions: Dict[str, Any]
) -> Alert:
    """
    Create a pest risk warning alert.

    Uses stored prevention_tips as recommendations (NOT AI-generated).

    Args:
        db: Database session
        user_id: User ID
        correlation: Matching pest-weather correlation
        weather_conditions: Current weather data

    Returns:
        Created Alert object
    """
    # Map risk level to alert severity
    severity_map = {
        "low": AlertSeverity.INFO,
        "medium": AlertSeverity.WARNING,
        "high": AlertSeverity.CRITICAL
    }
    severity = severity_map.get(correlation.risk_level, AlertSeverity.INFO)

    # Build alert metadata
    metadata = {
        "pest_name": correlation.pest_name,
        "scientific_name": correlation.scientific_name,
        "risk_level": correlation.risk_level,
        "risk_conditions": correlation.risk_conditions,
        "weather_at_assessment": weather_conditions,
        "prevention_tips": correlation.prevention_tips,
        "data_source": correlation.data_source
    }

    # Create alert
    alert = Alert(
        user_id=user_id,
        type=AlertType.PEST_RISK_WARNING.value,
        severity=severity.value,
        title=f"Pest Risk Alert: {correlation.pest_name}",
        message=correlation.risk_message,
        source_id=correlation.id,
        source_type="pest_weather_correlation",
        metadata=metadata,
        is_read=False,
        is_acknowledged=False
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    logger.info(f"Created pest risk alert for user {user_id}: {correlation.pest_name}")
    return alert


async def check_and_generate_pest_risk_alerts(
    db: Session,
    user_id: int,
    crop_type: str,
    latitude: float,
    longitude: float
) -> List[Alert]:
    """
    Check pest risk and generate alerts for any matching conditions.

    This function is called by background jobs to proactively warn users.

    Args:
        db: Database session
        user_id: User ID
        crop_type: User's crop type
        latitude: Farm latitude
        longitude: Farm longitude

    Returns:
        List of created alerts
    """
    from services.weather_service import fetch_current_weather, transform_current_weather
    from datetime import timedelta

    created_alerts = []

    try:
        # Fetch current weather
        weather_data = await fetch_current_weather(latitude, longitude)
        current_weather = transform_current_weather(weather_data)

        temperature = current_weather.temperature
        relative_humidity = current_weather.relative_humidity
        recent_rain = bool(current_weather.rain and current_weather.rain > 0)

        weather_conditions = {
            "temperature": temperature,
            "relative_humidity": relative_humidity,
            "recent_rain": recent_rain,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to fetch weather for pest risk alerts: {e}")
        return []

    # Get correlations for user's crop type
    correlations = get_correlations_for_crop(db, crop_type)

    # Check each correlation and create alerts
    for correlation in correlations:
        if correlation.matches_weather(temperature, relative_humidity, recent_rain):
            # Check if we already have a recent alert for this pest
            six_hours_ago = datetime.utcnow() - timedelta(hours=6)
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.PEST_RISK_WARNING.value,
                Alert.source_id == correlation.id,
                Alert.source_type == "pest_weather_correlation",
                Alert.created_at >= six_hours_ago
            ).first()

            if not existing:
                alert = create_pest_risk_alert(
                    db=db,
                    user_id=user_id,
                    correlation=correlation,
                    weather_conditions=weather_conditions
                )
                created_alerts.append(alert)

    return created_alerts


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_risk_summary_for_display(
    risks: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Generate a user-friendly risk summary for display.

    Args:
        risks: List of active risk dictionaries

    Returns:
        dict: Summary suitable for UI display
    """
    if not risks:
        return {
            "status": "safe",
            "headline": "No Active Pest Risks",
            "description": "Current weather conditions do not favor any known pest outbreaks for your crop.",
            "action_required": False
        }

    # Count by risk level
    high_count = sum(1 for r in risks if r["risk_level"] == "high")
    medium_count = sum(1 for r in risks if r["risk_level"] == "medium")
    low_count = sum(1 for r in risks if r["risk_level"] == "low")

    if high_count > 0:
        return {
            "status": "critical",
            "headline": f"{high_count} High Risk Alert{'s' if high_count > 1 else ''}",
            "description": f"Weather conditions favor {high_count} high-risk pest{'s' if high_count > 1 else ''}. Take immediate preventive action.",
            "action_required": True,
            "top_risk": risks[0] if risks else None
        }
    elif medium_count > 0:
        return {
            "status": "warning",
            "headline": f"{medium_count} Pest Risk Warning{'s' if medium_count > 1 else ''}",
            "description": f"Weather conditions favor {medium_count} pest{'s' if medium_count > 1 else ''}. Increase monitoring frequency.",
            "action_required": True,
            "top_risk": risks[0] if risks else None
        }
    else:
        return {
            "status": "caution",
            "headline": f"{low_count} Low Risk Notice{'s' if low_count > 1 else ''}",
            "description": f"Minor pest risk detected. Continue regular monitoring.",
            "action_required": False,
            "top_risk": risks[0] if risks else None
        }


# ============================================================================
# LEARNING NOTES: Pest Risk Prediction
# ============================================================================

"""
1. How Pest Risk Prediction Works:
   - Fetch current weather conditions
   - Query pest-weather correlations for user's crop
   - Check each correlation against current weather
   - Return matching risks with prevention tips

2. Why NOT Use AI API for Risk Predictions:
   - Prevention tips are pre-vetted (from MARDI, IRRI)
   - Consistent advice every time (no AI variation)
   - Faster response (no API call latency)
   - Cost savings (API calls cost money)
   - Works offline if needed

3. Risk Conditions in Database:
   - temp_min, temp_max: Temperature range
   - humidity_min, humidity_max: Humidity range
   - trigger: Special conditions (after_rain, dry_period)
   - These are based on scientific research

4. Alert Generation:
   - Only one alert per pest per 6 hours
   - Includes prevention_tips in metadata
   - Maps risk_level to alert severity

5. Integration Points:
   - GET /pests/risk: User checks current risk
   - Background job: Periodic checks for all users
   - Dashboard: Shows risk status summary
"""
