"""
Weather service for fetching and processing weather data from OpenWeatherMap API.

This module provides functions to:
- Fetch current weather data
- Fetch weather forecasts
- Generate weather alerts based on conditions
- Generate agricultural recommendations

Learning Notes:
- Uses httpx for async HTTP requests
- Implements error handling for API failures
- Caches API responses to reduce API calls
- Generates mock alerts and recommendations for student project
"""

import httpx
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

# OpenWeatherMap API configuration
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"

# Cache configuration (simple in-memory cache)
_weather_cache = {}
CACHE_DURATION = timedelta(minutes=10)  # Cache for 10 minutes


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


# ============================================================================
# WEATHER DATA FETCHING
# ============================================================================

async def fetch_current_weather(latitude: float, longitude: float) -> dict:
    """
    Fetch current weather data from OpenWeatherMap API.
    
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
    
    url = f"{OPENWEATHER_BASE_URL}/weather"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Celsius
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        _set_cached_data(cache_key, data)
        return data


async def fetch_weather_forecast(latitude: float, longitude: float) -> dict:
    """
    Fetch 5-day weather forecast from OpenWeatherMap API.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        dict: Raw forecast data from API (3-hour intervals)
        
    Raises:
        httpx.HTTPError: If API request fails
    """
    cache_key = _get_cache_key("forecast", latitude, longitude)
    cached = _get_cached_data(cache_key)
    if cached:
        return cached
    
    url = f"{OPENWEATHER_BASE_URL}/forecast"
    params = {
        "lat": latitude,
        "lon": longitude,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"  # Celsius
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        _set_cached_data(cache_key, data)
        return data


# ============================================================================
# DATA TRANSFORMATION
# ============================================================================

def transform_current_weather(data: dict) -> WeatherCondition:
    """
    Transform OpenWeatherMap current weather data to WeatherCondition schema.
    
    Args:
        data: Raw API response
        
    Returns:
        WeatherCondition: Transformed weather data
    """
    main = data["main"]
    wind = data["wind"]
    clouds = data["clouds"]
    weather = data["weather"][0]
    rain = data.get("rain", {})
    
    return WeatherCondition(
        temperature=main["temp"],
        feels_like=main["feels_like"],
        humidity=main["humidity"],
        pressure=main["pressure"],
        wind_speed=wind["speed"],
        wind_direction=wind.get("deg", 0),
        clouds=clouds["all"],
        visibility=data.get("visibility", 10000),
        weather_main=weather["main"],
        weather_description=weather["description"],
        rain_1h=rain.get("1h"),
        rain_3h=rain.get("3h")
    )


def transform_forecast_data(data: dict) -> List[WeatherForecastItem]:
    """
    Transform OpenWeatherMap forecast data to list of WeatherForecastItem.
    
    Args:
        data: Raw API response
        
    Returns:
        List[WeatherForecastItem]: List of forecast items
    """
    forecast_list = []
    
    for item in data["list"]:
        main = item["main"]
        wind = item["wind"]
        clouds = item["clouds"]
        weather = item["weather"][0]
        rain = item.get("rain", {})
        
        forecast_item = WeatherForecastItem(
            forecast_time=datetime.fromtimestamp(item["dt"]),
            temperature=main["temp"],
            feels_like=main["feels_like"],
            humidity=main["humidity"],
            pressure=main["pressure"],
            wind_speed=wind["speed"],
            clouds=clouds["all"],
            weather_main=weather["main"],
            weather_description=weather["description"],
            rain_probability=item.get("pop", 0),  # Probability of precipitation
            rain_volume=rain.get("3h")
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
    elif current.rain_probability > 0.5 and forecast:
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
    if current.weather_main == "Clear" and current.humidity < 70:
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
