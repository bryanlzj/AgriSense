"""
Weather service for fetching and processing weather data from Open-Meteo API.

This module provides functions to:
- Fetch current weather data
- Fetch weather forecasts
- Generate weather alerts based on conditions
- Generate agricultural recommendations (static + AI-enhanced)

Learning Notes:
- Uses httpx for async HTTP requests
- Open-Meteo is free, no API key required
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

# Open-Meteo API configuration (free, no API key required)
from config import settings

OPENMETEO_BASE_URL = settings.openmeteo_base_url

# Cache configuration (simple in-memory cache)
_weather_cache = {}
CACHE_DURATION = timedelta(minutes=10)  # Cache for 10 minutes

# Logger
logger = logging.getLogger(__name__)

# WMO Weather Code descriptions (simplified for Malaysian agriculture)
WMO_WEATHER_CODES = {
    0: ("Clear sky", "clear"),
    1: ("Mainly clear", "clear"),
    2: ("Partly cloudy", "cloudy"),
    3: ("Overcast", "cloudy"),
    51: ("Light drizzle", "drizzle"),
    53: ("Moderate drizzle", "drizzle"),
    55: ("Dense drizzle", "drizzle"),
    61: ("Slight rain", "rain"),
    63: ("Moderate rain", "rain"),
    65: ("Heavy rain", "rain"),
}


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


def _get_weather_description(code: int) -> Tuple[str, str]:
    """Get weather description and category from WMO code."""
    return WMO_WEATHER_CODES.get(code, ("Unknown", "unknown"))


# ============================================================================
# WEATHER DATA FETCHING
# ============================================================================

async def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather data from Open-Meteo API.

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

    url = f"{OPENMETEO_BASE_URL}/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "rain",
            "weather_code",
            "surface_pressure",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover"
        ],
        "timezone": "auto"
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            _set_cached_data(cache_key, data)
            return data
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch current weather from Open-Meteo: {e}")
        return _get_mock_current_weather(latitude, longitude)


async def fetch_weather_forecast(latitude: float, longitude: float, days: int = 7) -> dict:
    """
    Fetch weather forecast from Open-Meteo API.

    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        days: Number of days to forecast (1-16)

    Returns:
        dict: Raw forecast data from API

    Raises:
        httpx.HTTPError: If API request fails
    """
    cache_key = _get_cache_key("forecast", latitude, longitude)
    cached = _get_cached_data(cache_key)
    if cached:
        return cached

    url = f"{OPENMETEO_BASE_URL}/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "rain",
            "weather_code",
            "surface_pressure",
            "wind_speed_10m",
            "cloud_cover"
        ],
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "wind_speed_10m_max"
        ],
        "timezone": "auto",
        "forecast_days": min(days, 16)
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            _set_cached_data(cache_key, data)
            return data
    except httpx.HTTPError as e:
        logger.error(f"Failed to fetch weather forecast from Open-Meteo: {e}")
        return _get_mock_forecast(latitude, longitude)


# ============================================================================
# MOCK DATA (When API not available)
# ============================================================================

def _get_mock_current_weather(latitude: float, longitude: float) -> dict:
    """Generate mock current weather data for testing."""
    return {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": "Asia/Kuala_Lumpur",
        "current": {
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M"),
            "temperature_2m": 30.0,
            "relative_humidity_2m": 75,
            "apparent_temperature": 34.0,
            "precipitation": 0.0,
            "rain": 0.0,
            "weather_code": 2,
            "surface_pressure": 1010.0,
            "wind_speed_10m": 15.0,
            "wind_direction_10m": 180,
            "cloud_cover": 50
        }
    }


def _get_mock_forecast(latitude: float, longitude: float) -> dict:
    """Generate mock forecast data for testing."""
    base_data = _get_mock_current_weather(latitude, longitude)

    # Generate hourly data for 3 days
    hourly_times = []
    hourly_temp = []
    hourly_humidity = []
    hourly_apparent = []
    hourly_precip_prob = []
    hourly_precip = []
    hourly_rain = []
    hourly_weather_code = []
    hourly_pressure = []
    hourly_wind = []
    hourly_cloud = []

    for i in range(72):  # 3 days * 24 hours
        time = datetime.now() + timedelta(hours=i)
        hourly_times.append(time.strftime("%Y-%m-%dT%H:00"))
        hourly_temp.append(28.0 + (i % 8) - 4)
        hourly_humidity.append(70 + (i % 20))
        hourly_apparent.append(30.0 + (i % 8) - 4)
        hourly_precip_prob.append(20 if i % 6 == 0 else 10)
        hourly_precip.append(0.0 if i % 6 != 0 else 2.0)
        hourly_rain.append(0.0 if i % 6 != 0 else 2.0)
        hourly_weather_code.append(61 if i % 6 == 0 else 2)
        hourly_pressure.append(1010.0)
        hourly_wind.append(10.0 + (i % 10))
        hourly_cloud.append(40 + (i % 40))

    base_data["hourly"] = {
        "time": hourly_times,
        "temperature_2m": hourly_temp,
        "relative_humidity_2m": hourly_humidity,
        "apparent_temperature": hourly_apparent,
        "precipitation_probability": hourly_precip_prob,
        "precipitation": hourly_precip,
        "rain": hourly_rain,
        "weather_code": hourly_weather_code,
        "surface_pressure": hourly_pressure,
        "wind_speed_10m": hourly_wind,
        "cloud_cover": hourly_cloud
    }

    # Generate daily data
    daily_times = []
    daily_weather_code = []
    daily_temp_max = []
    daily_temp_min = []
    daily_precip_sum = []
    daily_precip_prob = []
    daily_wind_max = []

    for i in range(3):
        date = datetime.now() + timedelta(days=i)
        daily_times.append(date.strftime("%Y-%m-%d"))
        daily_weather_code.append(2)
        daily_temp_max.append(34.0)
        daily_temp_min.append(26.0)
        daily_precip_sum.append(5.0)
        daily_precip_prob.append(40)
        daily_wind_max.append(20.0)

    base_data["daily"] = {
        "time": daily_times,
        "weather_code": daily_weather_code,
        "temperature_2m_max": daily_temp_max,
        "temperature_2m_min": daily_temp_min,
        "precipitation_sum": daily_precip_sum,
        "precipitation_probability_max": daily_precip_prob,
        "wind_speed_10m_max": daily_wind_max
    }

    return base_data


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_current_weather(data: dict) -> WeatherCondition:
    """
    Transform Open-Meteo current weather data to WeatherCondition schema.

    Args:
        data: Raw API response

    Returns:
        WeatherCondition: Transformed weather data
    """
    current = data.get("current", {})

    # Get weather description from code
    weather_code = current.get("weather_code", 0)
    weather_desc, weather_main = _get_weather_description(weather_code)

    # Convert wind from km/h to m/s (1 km/h = 0.277778 m/s)
    wind_speed_ms = current.get("wind_speed_10m", 0) * 0.277778

    return WeatherCondition(
        temperature=current.get("temperature_2m", 25.0),
        feels_like=current.get("apparent_temperature", 25.0),
        relative_humidity=current.get("relative_humidity_2m", 70),
        pressure=current.get("surface_pressure", 1010.0),
        wind_speed=wind_speed_ms,
        wind_direction=current.get("wind_direction_10m", 0),
        clouds=current.get("cloud_cover", 0),
        visibility=10000,  # Open-Meteo doesn't provide visibility in current
        weather_main=weather_main.title(),
        weather_description=weather_desc,
        rain=current.get("rain", 0.0),
        rain_1h=current.get("rain", 0.0),
        rain_3h=None
    )


def transform_forecast_data(data: dict) -> List[WeatherForecastItem]:
    """
    Transform Open-Meteo forecast data to list of WeatherForecastItem.

    Args:
        data: Raw API response

    Returns:
        List[WeatherForecastItem]: List of forecast items
    """
    forecast_list = []

    hourly = data.get("hourly", {})
    if not hourly:
        return forecast_list

    times = hourly.get("time", [])
    temps = hourly.get("temperature_2m", [])
    feels_like = hourly.get("apparent_temperature", [])
    humidity = hourly.get("relative_humidity_2m", [])
    pressure = hourly.get("surface_pressure", [])
    wind_speed = hourly.get("wind_speed_10m", [])
    clouds = hourly.get("cloud_cover", [])
    weather_codes = hourly.get("weather_code", [])
    precip_prob = hourly.get("precipitation_probability", [])
    rain = hourly.get("rain", [])

    for i in range(len(times)):
        # Convert wind from km/h to m/s
        wind_ms = wind_speed[i] * 0.277778 if i < len(wind_speed) else 0

        # Get weather description
        code = weather_codes[i] if i < len(weather_codes) else 0
        weather_desc, weather_main = _get_weather_description(code)

        forecast_item = WeatherForecastItem(
            forecast_time=datetime.fromisoformat(times[i]),
            temperature=temps[i] if i < len(temps) else 25.0,
            feels_like=feels_like[i] if i < len(feels_like) else 25.0,
            humidity=humidity[i] if i < len(humidity) else 70,
            pressure=pressure[i] if i < len(pressure) else 1010.0,
            wind_speed=wind_ms,
            clouds=clouds[i] if i < len(clouds) else 0,
            weather_main=weather_main.title(),
            weather_description=weather_desc,
            rain_probability=(precip_prob[i] / 100) if i < len(precip_prob) else 0,
            rain_volume=rain[i] if i < len(rain) else 0
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
    rain_amount = current.rain_1h or current.rain or 0
    if rain_amount > 10:
        alerts.append(WeatherAlert(
            alert_type="Heavy Rain",
            severity="high",
            title="Heavy Rain Warning",
            description=f"Heavy rainfall detected ({rain_amount:.1f}mm). Risk of waterlogging.",
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
    heavy_rain_forecast = [f for f in forecast[:24] if f.rain_probability > 0.7]  # Next 24 hours
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
    rain_amount = current.rain_1h or current.rain or 0
    if rain_amount > 5:
        recommendations.append(AgriculturalRecommendation(
            category="irrigation",
            priority="high",
            title="Suspend Irrigation",
            description="Recent rainfall provides sufficient water. Suspend irrigation to avoid waterlogging.",
            reason=f"Recent rainfall: {rain_amount:.1f}mm",
            actions=[
                "Turn off irrigation systems",
                "Check soil moisture levels",
                "Resume irrigation only when soil dries"
            ]
        ))
    elif current.temperature > 30 and current.relative_humidity < 50:
        recommendations.append(AgriculturalRecommendation(
            category="irrigation",
            priority="high",
            title="Increase Irrigation",
            description="Hot and dry conditions increase water demand. Increase irrigation frequency.",
            reason=f"Temperature: {current.temperature:.1f}°C, Humidity: {current.relative_humidity}%",
            actions=[
                "Water early morning or late evening",
                "Increase irrigation frequency",
                "Check soil moisture regularly",
                "Apply mulch to retain moisture"
            ]
        ))

    # Pest control recommendations
    if current.relative_humidity > 80 and current.temperature > 25:
        recommendations.append(AgriculturalRecommendation(
            category="pest_control",
            priority="medium",
            title="Monitor for Fungal Diseases",
            description="High humidity and warm temperature favor fungal disease development.",
            reason=f"Humidity: {current.relative_humidity}%, Temperature: {current.temperature:.1f}°C",
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
    if current.weather_main.lower() in ["clear", "sunny"] or "clear" in current.weather_description.lower():
        if current.relative_humidity < 70:
            recommendations.append(AgriculturalRecommendation(
                category="harvesting",
                priority="medium",
                title="Good Harvesting Conditions",
                description="Clear weather and low humidity are ideal for harvesting.",
                reason=f"Weather: {current.weather_main}, Humidity: {current.relative_humidity}%",
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
            relative_humidity=forecast[0].humidity,
            pressure=forecast[0].pressure,
            wind_speed=forecast[0].wind_speed,
            wind_direction=0,
            clouds=forecast[0].clouds,
            visibility=10000,
            weather_main=forecast[0].weather_main,
            weather_description=forecast[0].weather_description,
            rain=forecast[0].rain_volume,
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
    """Check if weather API is properly configured (Open-Meteo is always available)."""
    return True  # Open-Meteo requires no API key


async def test_weather_api_connection() -> dict:
    """Test connection to Open-Meteo API."""
    try:
        # Test with default location (Kuala Lumpur)
        data = await fetch_current_weather(3.1390, 101.6869)
        if "current" in data:
            return {
                "status": "ok",
                "message": "Open-Meteo API is working",
                "sample_data": {
                    "temperature": data["current"].get("temperature_2m"),
                    "humidity": data["current"].get("relative_humidity_2m"),
                    "weather_code": data["current"].get("weather_code")
                }
            }
        else:
            return {
                "status": "error",
                "message": "Unexpected response format from Open-Meteo"
            }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
