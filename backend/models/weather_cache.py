"""
Weather Cache Model

This module defines the database cache for weather data.
Replaces in-memory caching with persistent database storage.

Learning Notes:
- Caching reduces external API calls (OpenWeatherMap)
- Database cache persists across server restarts
- 30-minute cache duration per PRD v2
- Shared across users by location (not user-specific)
"""

from sqlalchemy import Column, Integer, String, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from datetime import datetime, timedelta

from database import Base


class WeatherCache(Base):
    """
    Weather Cache Model

    Stores cached weather data from OpenWeatherMap API.
    Shared across users - keyed by location coordinates.

    Table: weather_cache
    """

    __tablename__ = "weather_cache"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique cache entry identifier"
    )

    # Location Key (unique identifier for cache lookup)
    # Format: "lat_lng" e.g., "3.1390_101.6869"
    location_key = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Unique location key (lat_lng format) for cache lookup"
    )

    # Location Name (human-readable)
    location_name = Column(
        String(100),
        nullable=False,
        comment="Human-readable location name (e.g., Kuala Lumpur)"
    )

    # Current Weather Conditions (JSONB)
    # Example: {"temp": 28.5, "humidity": 75, "weather": "cloudy", "wind_speed": 12.5}
    current_conditions = Column(
        JSONB,
        nullable=False,
        comment="Current weather data from API"
    )

    # 7-Day Forecast Data (JSONB)
    # Example: [{"date": "2025-01-15", "temp_min": 24, "temp_max": 32, ...}, ...]
    forecast_data = Column(
        JSONB,
        nullable=False,
        comment="7-day forecast data from API"
    )

    # ML Predictions (JSONB, optional)
    # Example: {"anomaly_detected": false, "predictions": [...], "confidence": 0.85}
    ml_predictions = Column(
        JSONB,
        nullable=True,
        comment="Output from weather ML model (anomalies, predictions)"
    )

    # Timestamp when data was fetched
    fetched_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="When the weather data was fetched from API"
    )

    # Indexes for common queries
    __table_args__ = (
        Index('idx_weather_cache_fetched', 'fetched_at'),
        {'comment': 'Cache for weather API data, shared across users by location'}
    )

    def __repr__(self):
        """String representation for debugging"""
        return f"<WeatherCache(id={self.id}, location='{self.location_name}', fetched_at={self.fetched_at})>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "location_key": self.location_key,
            "location_name": self.location_name,
            "current_conditions": self.current_conditions,
            "forecast_data": self.forecast_data,
            "ml_predictions": self.ml_predictions,
            "fetched_at": self.fetched_at.isoformat() if self.fetched_at else None
        }

    def is_expired(self, cache_duration_seconds: int = 1800) -> bool:
        """
        Check if cache entry has expired.

        Args:
            cache_duration_seconds: Cache TTL in seconds (default: 1800 = 30 minutes)

        Returns:
            True if cache has expired, False if still valid
        """
        if not self.fetched_at:
            return True

        expiry_time = self.fetched_at + timedelta(seconds=cache_duration_seconds)
        return datetime.now(self.fetched_at.tzinfo) > expiry_time

    @staticmethod
    def generate_location_key(lat: float, lng: float) -> str:
        """
        Generate a location key from coordinates.

        Args:
            lat: Latitude coordinate
            lng: Longitude coordinate

        Returns:
            Location key string (e.g., "3.1390_101.6869")
        """
        # Round to 4 decimal places for consistency
        return f"{round(lat, 4)}_{round(lng, 4)}"


# ============================================================================
# LEARNING NOTES: Weather Caching Strategy
# ============================================================================

"""
1. Why Cache Weather Data?
   - OpenWeatherMap API has rate limits (1000 calls/day for free tier)
   - Weather doesn't change frequently (30-minute updates sufficient)
   - Reduces latency for users
   - Saves bandwidth and API costs

2. Cache Strategy:
   - Key: Location coordinates (lat_lng format)
   - TTL: 30 minutes (configurable)
   - Shared: All users at same location share cache
   - Persistent: Survives server restarts (database-backed)

3. Cache Flow:
   1. User requests weather for their location
   2. Generate location_key from coordinates
   3. Check database for existing cache entry
   4. If found AND not expired → return cached data
   5. If not found OR expired → fetch from API, store in cache
   6. Return fresh data

4. Why Database Cache vs In-Memory?
   In-Memory (Redis, dict):
   ✅ Faster reads
   ❌ Lost on server restart
   ❌ Not shared across multiple server instances

   Database Cache:
   ✅ Persistent across restarts
   ✅ Shared across all server instances
   ✅ Easy to query and debug
   ❌ Slightly slower than in-memory

   For this project, database cache is simpler and sufficient.

5. JSONB Columns:
   - Store flexible weather data structure
   - Easy to query with PostgreSQL operators
   - Can add new fields without schema changes
   - Better than TEXT for structured data

6. Location Key Format:
   - "3.1390_101.6869" (lat_lng with 4 decimal places)
   - Unique per location
   - Rounding ensures nearby coordinates hit same cache
   - 4 decimal places ≈ 11 meter accuracy (sufficient for weather)

Example Usage:
    from models.weather_cache import WeatherCache

    # Generate cache key
    key = WeatherCache.generate_location_key(3.1390, 101.6869)

    # Check cache
    cached = db.query(WeatherCache).filter(
        WeatherCache.location_key == key
    ).first()

    if cached and not cached.is_expired():
        # Use cached data
        return cached.current_conditions

    # Fetch fresh data from API
    weather_data = fetch_from_openweathermap(lat, lng)

    # Update or create cache entry
    if cached:
        cached.current_conditions = weather_data["current"]
        cached.forecast_data = weather_data["forecast"]
        cached.fetched_at = datetime.now()
    else:
        cached = WeatherCache(
            location_key=key,
            location_name="Kuala Lumpur",
            current_conditions=weather_data["current"],
            forecast_data=weather_data["forecast"]
        )
        db.add(cached)

    db.commit()
    return weather_data["current"]
"""
