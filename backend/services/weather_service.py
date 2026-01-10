"""
Weather service for fetching and processing weather data from WeatherAPI.com.

This module provides functions to:
- Fetch current weather data
- Fetch weather forecasts
- Generate weather alerts based on conditions
- Generate agricultural recommendations (static + AI-enhanced)

Learning Notes:
- Uses httpx for async HTTP requests
- Implements error handling for API failures
- Caches API responses to reduce API calls
- Generates mock alerts and recommendations for student project
- Can optionally use AI service for enhanced recommendations

PRD v2 Integration:
- Weather ML model outputs weather conditions (not recommendations)
- AI API (OpenRouter) generates farming recommendations
- Static recommendations serve as fallback when AI unavailable
"""

import httpx
import logging
from typing import List, Optional, Tuple
from datetime import datetime, timedelta
import os
from schemas.weather import (
    WeatherCondition,
    WeatherForecastItem,
    WeatherAlert,
    AgriculturalRecommendation,
    CurrentWeatherResponse,
    WeatherForecastResponse,
    WeatherSummaryResponse,
    LocationInput
)


# ============================================================================
# CONFIGURATION
# ============================================================================

# WeatherAPI.com API configuration
from config import settings

WEATHERAPI_KEY = settings.weatherapi_key
WEATHERAPI_BASE_URL = settings.weatherapi_base_url

# Cache configuration (simple in-memory cache)
_weather_cache = {}
CACHE_DURATION = timedelta(minutes=10)  # Cache for 10 minutes

# Logger
logger = logging.getLogger(__name__)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_cache_key(endpoint: str, lat: float, lon: float) -> str:
    """Generate cache key for weather data."""
    return f"{endpoint}:{lat}:{lon}"


def _get_cached_data(cache_key: str) -> Optional[dict]:
    """Get cached data if still valid."""
    if cache_key in _weather_cache:
        data, timestamp = _weather_cache[cache_key]
        if datetime.now() - timestamp < CACHE_DURATION:
            return data
    return None


def _set_cached_data(cache_key: str, data: dict):
    """Store data in cache with timestamp."""
    _weather_cache[cache_key] = (data, datetime.now())


def _is_api_configured() -> bool:
    """Check if WeatherAPI is properly configured."""
    return bool(WEATHERAPI_KEY and WEATHERAPI_KEY != "your_weatherapi_key_here")


# ============================================================================
# WEATHER DATA FETCHING
# ============================================================================

async def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather data from WeatherAPI.com.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate

    Returns:
        dict: Raw weather data from API

    Raises:
        httpx.HTTPError: If API request fails
    """
    cache_key = _get_cache_key("current", latitude, longitude)
    cached = _get_cached_data(cache_key)
    if cached:
        return cached

    if not _is_api_configured():
        logger.warning("WeatherAPI key not configured, returning mock data")
        return _get_mock_current_weather(latitude, longitude)

    url = f"{WEATHERAPI_BASE_URL}/current.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": f"{latitude},{longitude}",
        "aqi": "no"  # Air quality index not needed
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        _set_cached_data(cache_key, data)
        return data


async def fetch_weather_forecast(latitude: float, longitude: float, days: int = 7) -> dict:
    """
    Fetch weather forecast from WeatherAPI.com.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        days: Number of days to forecast (1-10)

    Returns:
        dict: Raw forecast data from API

    Raises:
        httpx.HTTPError: If API request fails
    """
    cache_key = _get_cache_key("forecast", latitude, longitude)
    cached = _get_cached_data(cache_key)
    if cached:
        return cached

    if not _is_api_configured():
        logger.warning("WeatherAPI key not configured, returning mock data")
        return _get_mock_forecast(latitude, longitude)

    url = f"{WEATHERAPI_BASE_URL}/forecast.json"
    params = {
        "key": WEATHERAPI_KEY,
        "q": f"{latitude},{longitude}",
        "days": min(days, 10),  # WeatherAPI free tier supports up to 3 days
        "aqi": "no",
        "alerts": "no"
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        _set_cached_data(cache_key, data)
        return data


# ============================================================================
# MOCK DATA (When API not configured)
# ============================================================================

def _get_mock_current_weather(latitude: float, longitude: float) -> dict:
    """Generate mock current weather data for testing."""
    return {
        "location": {
            "name": "Mock Location",
            "region": "Test Region",
            "country": "Malaysia",
            "lat": latitude,
            "lon": longitude,
            "localtime": datetime.now().strftime("%Y-%m-%d %H:%M")
        },
        "current": {
            "temp_c": 30.0,
            "feelslike_c": 34.0,
            "humidity": 75,
            "pressure_mb": 1010.0,
            "wind_kph": 15.0,
            "wind_degree": 180,
            "wind_dir": "S",
            "cloud": 50,
            "vis_km": 10.0,
            "precip_mm": 0.0,
            "condition": {
                "text": "Partly cloudy",
                "code": 1003
            }
        }
    }


def _get_mock_forecast(latitude: float, longitude: float) -> dict:
    """Generate mock forecast data for testing."""
    base_data = _get_mock_current_weather(latitude, longitude)

    forecast_days = []
    for i in range(3):
        date = datetime.now() + timedelta(days=i)
        hours = []
        for h in range(24):
            hour_time = date.replace(hour=h, minute=0, second=0)
            hours.append({
                "time_epoch": int(hour_time.timestamp()),
                "time": hour_time.strftime("%Y-%m-%d %H:%M"),
                "temp_c": 28.0 + (h % 8) - 4,
                "feelslike_c": 30.0 + (h % 8) - 4,
                "humidity": 70 + (h % 20),
                "wind_kph": 10.0 + (h % 10),
                "wind_dir": "S",
                "pressure_mb": 1010.0,
                "precip_mm": 0.0 if h % 6 != 0 else 2.0,
                "cloud": 40 + (h % 40),
                "chance_of_rain": 20 if h % 6 == 0 else 10,
                "condition": {
                    "text": "Partly cloudy",
                    "code": 1003
                }
            })

        forecast_days.append({
            "date": date.strftime("%Y-%m-%d"),
            "date_epoch": int(date.timestamp()),
            "day": {
                "maxtemp_c": 34.0,
                "mintemp_c": 26.0,
                "avgtemp_c": 30.0,
                "maxwind_kph": 20.0,
                "totalprecip_mm": 5.0,
                "avghumidity": 75,
                "daily_chance_of_rain": 40,
                "condition": {
                    "text": "Partly cloudy",
                    "code": 1003
                }
            },
            "hour": hours
        })

    base_data["forecast"] = {"forecastday": forecast_days}
    return base_data


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_current_weather(data: dict) -> WeatherCondition:
    """
    Transform WeatherAPI.com current weather data to WeatherCondition schema.

    Args:
        data: Raw API response

    Returns:
        WeatherCondition: Transformed weather data
    """
    current = data["current"]

    # Convert wind from kph to m/s (1 kph = 0.277778 m/s)
    wind_speed_ms = current.get("wind_kph", 0) * 0.277778

    return WeatherCondition(
        temperature=current["temp_c"],
        feels_like=current["feelslike_c"],
        humidity=current["humidity"],
        pressure=current["pressure_mb"],
        wind_speed=wind_speed_ms,
        wind_direction=current.get("wind_degree", 0),
        clouds=current.get("cloud", 0),
        visibility=current.get("vis_km", 10) * 1000,  # Convert km to meters
        weather_main=current["condition"]["text"],
        weather_description=current["condition"]["text"],
        rain_1h=current.get("precip_mm"),
        rain_3h=None  # WeatherAPI doesn't provide 3h rain data in current
    )


def transform_forecast_data(data: dict) -> List[WeatherForecastItem]:
    """
    Transform WeatherAPI.com forecast data to list of WeatherForecastItem.

    Args:
        data: Raw API response

    Returns:
        List[WeatherForecastItem]: List of forecast items
    """
    forecast_list = []

    if "forecast" not in data or "forecastday" not in data["forecast"]:
        return forecast_list

    for day in data["forecast"]["forecastday"]:
        # Get hourly data for more granular forecasts
        for hour in day.get("hour", []):
            # Convert wind from kph to m/s
            wind_speed_ms = hour.get("wind_kph", 0) * 0.277778

            forecast_item = WeatherForecastItem(
                forecast_time=datetime.fromtimestamp(hour["time_epoch"]),
                temperature=hour["temp_c"],
                feels_like=hour["feelslike_c"],
                humidity=hour["humidity"],
                pressure=hour["pressure_mb"],
                wind_speed=wind_speed_ms,
                clouds=hour.get("cloud", 0),
                weather_main=hour["condition"]["text"],
                weather_description=hour["condition"]["text"],
                rain_probability=hour.get("chance_of_rain", 0) / 100,  # Convert % to 0-1
                rain_volume=hour.get("precip_mm")
            )
            forecast_list.append(forecast_item)

    return forecast_list


# ============================================================================
# ALERT GENERATION
# ============================================================================

def generate_weather_alerts(
    current: WeatherCondition,
    forecast: List[WeatherForecastItem]
) -> List[WeatherAlert]:
    """
    Generate weather alerts based on current conditions and forecast.

    This is a simplified alert system for the student project.
    In production, you would use official weather alert APIs.

    Args:
        current: Current weather conditions
        forecast: Weather forecast data

    Returns:
        List[WeatherAlert]: List of generated alerts
    """
    alerts = []
    now = datetime.now()

    # Heavy rain alert
    if current.rain_1h and current.rain_1h > 10:
        alerts.append(WeatherAlert(
            alert_type="Heavy Rain",
            severity="high",
            title="Heavy Rain Warning",
            description=f"Heavy rainfall detected ({current.rain_1h:.1f}mm in last hour). Risk of waterlogging.",
            start_time=now,
            end_time=now + timedelta(hours=3),
            recommendations=[
                "Ensure proper drainage in fields",
                "Delay irrigation activities",
                "Protect sensitive crops with covers",
                "Monitor for signs of waterlogging"
            ]
        ))

    # Strong wind alert
    if current.wind_speed > 10:  # > 10 m/s (36 km/h)
        alerts.append(WeatherAlert(
            alert_type="Strong Wind",
            severity="medium",
            title="Strong Wind Advisory",
            description=f"Strong winds detected ({current.wind_speed:.1f} m/s). Risk of crop damage.",
            start_time=now,
            end_time=now + timedelta(hours=6),
            recommendations=[
                "Secure loose equipment and materials",
                "Check support structures for tall crops",
                "Delay pesticide spraying",
                "Monitor for physical crop damage"
            ]
        ))

    # High temperature alert
    if current.temperature > 35:
        alerts.append(WeatherAlert(
            alert_type="High Temperature",
            severity="medium",
            title="Heat Stress Warning",
            description=f"High temperature detected ({current.temperature:.1f}°C). Risk of heat stress.",
            start_time=now,
            end_time=now + timedelta(hours=12),
            recommendations=[
                "Increase irrigation frequency",
                "Apply mulch to retain soil moisture",
                "Provide shade for sensitive crops",
                "Monitor plants for wilting signs"
            ]
        ))

    # Forecast-based: Heavy rain expected
    heavy_rain_forecast = [f for f in forecast[:8] if f.rain_probability > 0.7]  # Next 24 hours
    if heavy_rain_forecast:
        alerts.append(WeatherAlert(
            alert_type="Heavy Rain Forecast",
            severity="medium",
            title="Heavy Rain Expected",
            description=f"High probability of rain in next 24 hours ({len(heavy_rain_forecast)} periods).",
            start_time=heavy_rain_forecast[0].forecast_time,
            end_time=heavy_rain_forecast[-1].forecast_time,
            recommendations=[
                "Complete urgent field work before rain",
                "Prepare drainage systems",
                "Delay fertilizer application",
                "Harvest mature crops if possible"
            ]
        ))

    return alerts


# ============================================================================
# RECOMMENDATION GENERATION
# ============================================================================

def generate_agricultural_recommendations(
    current: WeatherCondition,
    forecast: List[WeatherForecastItem],
    alerts: List[WeatherAlert]
) -> List[AgriculturalRecommendation]:
    """
    Generate agricultural recommendations based on weather conditions.

    Args:
        current: Current weather conditions
        forecast: Weather forecast data
        alerts: Active weather alerts

    Returns:
        List[AgriculturalRecommendation]: List of recommendations
    """
    recommendations = []

    # Irrigation recommendations
    if current.rain_1h and current.rain_1h > 5:
        recommendations.append(AgriculturalRecommendation(
            category="irrigation",
            priority="high",
            title="Suspend Irrigation",
            description="Recent rainfall provides sufficient water. Suspend irrigation to avoid waterlogging.",
            reason=f"Recent rainfall: {current.rain_1h:.1f}mm in last hour",
            actions=[
                "Turn off irrigation systems",
                "Check soil moisture levels",
                "Resume irrigation only when soil dries"
            ]
        ))
    elif current.temperature > 30 and current.humidity < 50:
        recommendations.append(AgriculturalRecommendation(
            category="irrigation",
            priority="high",
            title="Increase Irrigation",
            description="Hot and dry conditions increase water demand. Increase irrigation frequency.",
            reason=f"Temperature: {current.temperature:.1f}°C, Humidity: {current.humidity}%",
            actions=[
                "Water early morning or late evening",
                "Increase irrigation frequency",
                "Check soil moisture regularly",
                "Apply mulch to retain moisture"
            ]
        ))

    # Pest control recommendations
    if current.humidity > 80 and current.temperature > 25:
        recommendations.append(AgriculturalRecommendation(
            category="pest_control",
            priority="medium",
            title="Monitor for Fungal Diseases",
            description="High humidity and warm temperature favor fungal disease development.",
            reason=f"Humidity: {current.humidity}%, Temperature: {current.temperature:.1f}°C",
            actions=[
                "Inspect plants for disease symptoms",
                "Improve air circulation",
                "Apply preventive fungicides if needed",
                "Remove infected plant material"
            ]
        ))

    # Spraying recommendations
    if current.wind_speed > 5:
        recommendations.append(AgriculturalRecommendation(
            category="spraying",
            priority="high",
            title="Avoid Pesticide Spraying",
            description="Wind speed too high for effective pesticide application.",
            reason=f"Wind speed: {current.wind_speed:.1f} m/s",
            actions=[
                "Postpone spraying activities",
                "Wait for wind speed below 5 m/s",
                "Check weather forecast for calm periods"
            ]
        ))
    elif forecast:
        next_rain = next((f for f in forecast if f.rain_probability > 0.5), None)
        if next_rain:
            hours_until_rain = (next_rain.forecast_time - datetime.now()).total_seconds() / 3600
            if hours_until_rain < 6:
                recommendations.append(AgriculturalRecommendation(
                    category="spraying",
                    priority="high",
                    title="Avoid Pesticide Spraying",
                    description=f"Rain expected in {hours_until_rain:.1f} hours. Pesticides may wash off.",
                    reason=f"Rain probability: {next_rain.rain_probability*100:.0f}%",
                    actions=[
                        "Postpone spraying until after rain",
                        "Wait for dry conditions",
                        "Check forecast before spraying"
                    ]
                ))

    # Harvesting recommendations
    if current.weather_main == "Clear" or "sunny" in current.weather_main.lower():
        if current.humidity < 70:
            recommendations.append(AgriculturalRecommendation(
                category="harvesting",
                priority="medium",
                title="Good Harvesting Conditions",
                description="Clear weather and low humidity are ideal for harvesting.",
                reason=f"Weather: {current.weather_main}, Humidity: {current.humidity}%",
                actions=[
                    "Harvest mature crops",
                    "Ensure proper drying conditions",
                    "Store harvested crops in dry place"
                ]
            ))

    return recommendations


# ============================================================================
# MAIN SERVICE FUNCTIONS
# ============================================================================

async def get_current_weather(
    latitude: float,
    longitude: float,
    location_name: Optional[str] = None
) -> CurrentWeatherResponse:
    """
    Get current weather with alerts and recommendations.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location_name: Optional location name

    Returns:
        CurrentWeatherResponse: Complete current weather data
    """
    # Fetch data
    weather_data = await fetch_current_weather(latitude, longitude)

    # Transform data
    current = transform_current_weather(weather_data)

    # Generate alerts and recommendations
    alerts = generate_weather_alerts(current, [])
    recommendations = generate_agricultural_recommendations(current, [], alerts)

    # Build response
    location = LocationInput(
        latitude=latitude,
        longitude=longitude,
        location_name=location_name
    )

    return CurrentWeatherResponse(
        location=location,
        current=current,
        alerts=alerts,
        recommendations=recommendations,
        updated_at=datetime.now()
    )


async def get_weather_forecast(
    latitude: float,
    longitude: float,
    location_name: Optional[str] = None
) -> WeatherForecastResponse:
    """
    Get weather forecast with alerts and recommendations.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location_name: Optional location name

    Returns:
        WeatherForecastResponse: Complete forecast data
    """
    # Fetch data
    forecast_data = await fetch_weather_forecast(latitude, longitude)

    # Transform data
    forecast = transform_forecast_data(forecast_data)

    # Generate alerts and recommendations (using first forecast item as "current")
    if forecast:
        mock_current = WeatherCondition(
            temperature=forecast[0].temperature,
            feels_like=forecast[0].feels_like,
            humidity=forecast[0].humidity,
            pressure=forecast[0].pressure,
            wind_speed=forecast[0].wind_speed,
            wind_direction=0,
            clouds=forecast[0].clouds,
            visibility=10000,
            weather_main=forecast[0].weather_main,
            weather_description=forecast[0].weather_description,
            rain_1h=forecast[0].rain_volume,
            rain_3h=None
        )
        alerts = generate_weather_alerts(mock_current, forecast)
        recommendations = generate_agricultural_recommendations(mock_current, forecast, alerts)
    else:
        alerts = []
        recommendations = []

    # Build response
    location = LocationInput(
        latitude=latitude,
        longitude=longitude,
        location_name=location_name
    )

    return WeatherForecastResponse(
        location=location,
        forecast=forecast,
        alerts=alerts,
        recommendations=recommendations,
        updated_at=datetime.now()
    )


async def get_weather_summary(
    latitude: float,
    longitude: float,
    location_name: Optional[str] = None
) -> WeatherSummaryResponse:
    """
    Get complete weather summary (current + forecast + alerts + recommendations).

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location_name: Optional location name

    Returns:
        WeatherSummaryResponse: Complete weather summary
    """
    # Fetch both current and forecast data
    weather_data = await fetch_current_weather(latitude, longitude)
    forecast_data = await fetch_weather_forecast(latitude, longitude)

    # Transform data
    current = transform_current_weather(weather_data)
    forecast = transform_forecast_data(forecast_data)

    # Generate alerts and recommendations
    alerts = generate_weather_alerts(current, forecast)
    recommendations = generate_agricultural_recommendations(current, forecast, alerts)

    # Build response
    location = LocationInput(
        latitude=latitude,
        longitude=longitude,
        location_name=location_name
    )

    return WeatherSummaryResponse(
        location=location,
        current=current,
        forecast=forecast,
        alerts=alerts,
        recommendations=recommendations,
        updated_at=datetime.now()
    )


# ============================================================================
# AI-ENHANCED RECOMMENDATIONS (PRD v2)
# ============================================================================

async def get_ai_enhanced_weather_recommendations(
    alerts: List[WeatherAlert],
    crop_type: str,
    location_name: Optional[str] = None
) -> List[dict]:
    """
    Enhance weather alerts with AI-generated recommendations.

    This function takes weather alerts and calls the AI service to generate
    context-aware farming recommendations for each alert type.

    Args:
        alerts: List of weather alerts from generate_weather_alerts()
        crop_type: User's crop type (rice, vegetables, etc.)
        location_name: Farm location name

    Returns:
        List[dict]: Enhanced alerts with AI recommendations
    """
    from services.ai_service import get_weather_recommendations, is_ai_available

    enhanced_alerts = []

    for alert in alerts:
        # Prepare conditions dict for AI
        conditions = {
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "description": alert.description
        }

        # Determine alert type category
        alert_type_lower = alert.alert_type.lower()
        if "rain" in alert_type_lower:
            ai_alert_type = "heavy_rain"
        elif "wind" in alert_type_lower:
            ai_alert_type = "strong_wind"
        elif "temperature" in alert_type_lower or "heat" in alert_type_lower:
            ai_alert_type = "high_temperature"
        else:
            ai_alert_type = alert_type_lower.replace(" ", "_")

        # Get AI recommendations if available
        if is_ai_available():
            try:
                ai_recs = await get_weather_recommendations(
                    alert_type=ai_alert_type,
                    conditions=conditions,
                    crop_type=crop_type,
                    location=location_name
                )
                # Combine static and AI recommendations
                combined_recommendations = list(alert.recommendations) if alert.recommendations else []
                if ai_recs.get("immediate_actions"):
                    combined_recommendations.extend(ai_recs["immediate_actions"])
                if ai_recs.get("crop_protection"):
                    combined_recommendations.extend(ai_recs["crop_protection"])

                # Deduplicate recommendations
                seen = set()
                unique_recs = []
                for rec in combined_recommendations:
                    if rec.lower() not in seen:
                        seen.add(rec.lower())
                        unique_recs.append(rec)

                enhanced_alert = {
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "title": alert.title,
                    "description": alert.description,
                    "start_time": alert.start_time.isoformat() if alert.start_time else None,
                    "end_time": alert.end_time.isoformat() if alert.end_time else None,
                    "recommendations": unique_recs[:8],  # Limit to 8 recommendations
                    "ai_enhanced": True
                }
            except Exception as e:
                logger.warning(f"Failed to get AI recommendations for {alert.alert_type}: {e}")
                enhanced_alert = {
                    "alert_type": alert.alert_type,
                    "severity": alert.severity,
                    "title": alert.title,
                    "description": alert.description,
                    "start_time": alert.start_time.isoformat() if alert.start_time else None,
                    "end_time": alert.end_time.isoformat() if alert.end_time else None,
                    "recommendations": alert.recommendations,
                    "ai_enhanced": False
                }
        else:
            # Use static recommendations
            enhanced_alert = {
                "alert_type": alert.alert_type,
                "severity": alert.severity,
                "title": alert.title,
                "description": alert.description,
                "start_time": alert.start_time.isoformat() if alert.start_time else None,
                "end_time": alert.end_time.isoformat() if alert.end_time else None,
                "recommendations": alert.recommendations,
                "ai_enhanced": False
            }

        enhanced_alerts.append(enhanced_alert)

    return enhanced_alerts


async def get_weather_summary_with_ai(
    latitude: float,
    longitude: float,
    location_name: Optional[str] = None,
    crop_type: str = "rice"
) -> WeatherSummaryResponse:
    """
    Get complete weather summary with AI-enhanced recommendations.

    This is an enhanced version of get_weather_summary that includes
    AI-generated recommendations when the AI service is available.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        location_name: Optional location name
        crop_type: User's crop type for context-aware recommendations

    Returns:
        WeatherSummaryResponse: Complete weather summary with AI recommendations
    """
    # Get base weather summary
    summary = await get_weather_summary(latitude, longitude, location_name)

    # Enhance alerts with AI recommendations
    if summary.alerts:
        enhanced_alerts = await get_ai_enhanced_weather_recommendations(
            alerts=summary.alerts,
            crop_type=crop_type,
            location_name=location_name
        )

        # Update the alerts with enhanced versions (convert back to WeatherAlert)
        enhanced_weather_alerts = []
        for alert_dict in enhanced_alerts:
            enhanced_weather_alerts.append(WeatherAlert(
                alert_type=alert_dict["alert_type"],
                severity=alert_dict["severity"],
                title=alert_dict["title"],
                description=alert_dict["description"],
                start_time=datetime.fromisoformat(alert_dict["start_time"]) if alert_dict["start_time"] else None,
                end_time=datetime.fromisoformat(alert_dict["end_time"]) if alert_dict["end_time"] else None,
                recommendations=alert_dict["recommendations"]
            ))

        # Return updated summary with enhanced alerts
        return WeatherSummaryResponse(
            location=summary.location,
            current=summary.current,
            forecast=summary.forecast,
            alerts=enhanced_weather_alerts,
            recommendations=summary.recommendations,
            updated_at=summary.updated_at
        )

    return summary


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def is_weather_api_configured() -> bool:
    """Check if weather API is properly configured."""
    return _is_api_configured()


async def test_weather_api_connection() -> dict:
    """Test connection to WeatherAPI.com."""
    if not _is_api_configured():
        return {
            "status": "not_configured",
            "message": "WeatherAPI key not configured",
            "using_mock": True
        }

    try:
        # Test with default location (Kuala Lumpur)
        data = await fetch_current_weather(3.1390, 101.6869)
        if "current" in data:
            return {
                "status": "connected",
                "message": "WeatherAPI.com is working",
                "using_mock": False,
                "location": data.get("location", {}).get("name", "Unknown")
            }
        else:
            return {
                "status": "error",
                "message": "Unexpected response format",
                "using_mock": True
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "using_mock": True
        }
