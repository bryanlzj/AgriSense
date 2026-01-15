"""
SensorReading Model

This model stores simulated IoT sensor data for environmental monitoring.
Part of the Weather Early Warning System (CORE FEATURE #1).

Data Source: Open-Meteo API (acting as simulated sensor data)
Data fields aligned with Open-Meteo parameters for ML processing.

Educational Notes:
- This represents data from virtual sensors (no physical hardware)
- Data is fetched from Open-Meteo API to simulate sensor readings
- In a real system, this would come from ESP32/Arduino devices
- Stores time-series data (readings over time)
"""

from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from database import Base


class SensorReading(Base):
    """
    Stores environmental sensor readings for weather monitoring.

    This is the foundation of the Weather Early Warning System.
    Readings are used to:
    1. Display current conditions on dashboard
    2. Detect weather anomalies (extreme values)
    3. Predict pest risks (based on environmental conditions)
    4. Generate alerts when thresholds are exceeded
    5. ML model training and processing

    Data Source: Open-Meteo API (simulating IoT sensor data)
    Update Frequency: Every 30 seconds (simulated)

    Field mapping to Open-Meteo parameters:
    - temperature -> temperature_2m
    - relative_humidity -> relative_humidity_2m
    - rain -> rain
    - wind_speed -> wind_speed_10m
    - solar_radiation -> shortwave_radiation
    - soil_temperature -> soil_temperature_0_to_7cm
    - soil_moisture -> soil_moisture_0_to_7cm
    - weather_code -> weather_code
    """

    __tablename__ = "sensor_readings"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    # Auto-incrementing ID for each reading

    # Foreign Key to User
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Links reading to a specific user/farm
    # CASCADE: If user is deleted, delete all their readings

    # ===================================
    # Core Sensor Data Fields (Open-Meteo aligned)
    # ===================================

    temperature = Column(Float, nullable=False)
    # Temperature in Celsius (°C)
    # Open-Meteo: temperature_2m
    # Typical range for Malaysia: 25-35°C
    # Alert threshold: >35°C (extreme heat)

    relative_humidity = Column(Float, nullable=False)
    # Relative humidity as percentage (%)
    # Open-Meteo: relative_humidity_2m
    # Typical range: 60-90%
    # Alert threshold: >85% (high humidity, pest risk)

    rain = Column(Float, nullable=False, default=0.0)
    # Rainfall in millimeters (mm)
    # Open-Meteo: rain
    # Range: 0-50+ mm
    # Alert threshold: >10mm (heavy rain)

    wind_speed = Column(Float, nullable=False, default=0.0)
    # Wind speed in kilometers per hour (km/h)
    # Open-Meteo: wind_speed_10m
    # Typical range: 0-60 km/h
    # Alert threshold: >50 km/h (strong winds)

    solar_radiation = Column(Float, nullable=True)
    # Shortwave solar radiation (GHI) in W/m²
    # Open-Meteo: shortwave_radiation
    # Range: 0-1000+ W/m²
    # 0 at night, 800-1000 peak daylight

    soil_temperature = Column(Float, nullable=True)
    # Soil temperature at 0-7cm depth in Celsius (°C)
    # Open-Meteo: soil_temperature_0_to_7cm
    # Typical range: 20-35°C
    # Important for seed germination and root health

    soil_moisture = Column(Float, nullable=False)
    # Volumetric soil moisture at 0-7cm depth (m³/m³)
    # Open-Meteo: soil_moisture_0_to_7cm
    # Range: 0.0-0.5 m³/m³ (typical 0.1-0.4)
    # Alert threshold: <0.2 m³/m³ (dry soil, irrigation needed)

    weather_code = Column(Integer, nullable=True)
    # WMO Weather interpretation code
    # Open-Meteo: weather_code
    # 0 = Clear sky, 1-3 = Partly cloudy, 45/48 = Fog
    # 51-55 = Drizzle, 61-65 = Rain, 80-82 = Showers
    # 95 = Thunderstorm
    # Used for weather condition classification

    # Timestamp
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        index=True
    )
    # When this reading was taken
    # Indexed for fast time-based queries (e.g., "last 24 hours")
    # Uses UTC timezone for consistency

    # Relationships
    user = relationship("User", back_populates="sensor_readings")
    # Access the user who owns this reading: reading.user.username
    # Access all readings for a user: user.sensor_readings

    # Database Indexes for Performance
    __table_args__ = (
        # Composite index for common query: "Get user's recent readings"
        Index('idx_user_timestamp', 'user_id', 'timestamp'),
        # Allows fast queries like: "Get last 100 readings for user X"

        # Index for time-based queries
        Index('idx_timestamp_desc', 'timestamp'),
        # Allows fast queries like: "Get most recent reading across all users"
    )
    
    def to_dict(self):
        """
        Convert model to dictionary for API responses.

        Returns:
            dict: Sensor reading data in JSON-friendly format
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "temperature": round(self.temperature, 2),
            "relative_humidity": round(self.relative_humidity, 2),
            "rain": round(self.rain, 2),
            "wind_speed": round(self.wind_speed, 2),
            "solar_radiation": round(self.solar_radiation, 2) if self.solar_radiation else None,
            "soil_temperature": round(self.soil_temperature, 2) if self.soil_temperature else None,
            "soil_moisture": round(self.soil_moisture, 4),  # 4 decimal places for m³/m³
            "weather_code": self.weather_code,
            "timestamp": self.timestamp.isoformat(),
        }

    def is_anomaly(self):
        """
        Check if this reading contains anomalous values.
        Used for weather early warning system.

        Returns:
            dict: Anomaly status and reasons
        """
        anomalies = []

        # Check temperature (extreme heat)
        if self.temperature > 35:
            anomalies.append(f"Extreme heat: {self.temperature}°C")
        elif self.temperature < 20:
            anomalies.append(f"Unusually cold: {self.temperature}°C")

        # Check humidity (pest risk)
        if self.relative_humidity > 85:
            anomalies.append(f"High humidity: {self.relative_humidity}% (pest risk)")
        elif self.relative_humidity < 40:
            anomalies.append(f"Low humidity: {self.relative_humidity}%")

        # Check soil moisture (irrigation needed) - now in m³/m³
        if self.soil_moisture < 0.2:
            anomalies.append(f"Dry soil: {self.soil_moisture} m³/m³ (irrigation needed)")
        elif self.soil_moisture > 0.45:
            anomalies.append(f"Waterlogged soil: {self.soil_moisture} m³/m³")

        # Check wind speed (strong winds)
        if self.wind_speed > 50:
            anomalies.append(f"Strong winds: {self.wind_speed} km/h")

        # Check rain (heavy rain)
        if self.rain > 10:
            anomalies.append(f"Heavy rain: {self.rain} mm")

        return {
            "is_anomaly": len(anomalies) > 0,
            "anomalies": anomalies
        }

    def __repr__(self):
        """String representation for debugging"""
        return (
            f"<SensorReading(id={self.id}, user_id={self.user_id}, "
            f"temp={self.temperature}°C, humidity={self.relative_humidity}%, "
            f"rain={self.rain}mm, timestamp={self.timestamp})>"
        )


# ============================================================================
# LEARNING NOTES
# ============================================================================

"""
1. TIME-SERIES DATA:
   - Sensor readings are time-series data (values over time)
   - Each reading is a snapshot at a specific moment
   - Queries often involve time ranges: "last 24 hours", "last week"
   - Indexes on timestamp are crucial for performance

2. OPEN-METEO API INTEGRATION:
   - Data is fetched from Open-Meteo API (free, no API key required)
   - Acts as simulated IoT sensor data for development
   - Field names aligned with Open-Meteo parameters
   - In production, could be replaced with real sensor data

3. DATA FIELDS (Open-Meteo aligned):
   - temperature: Air temperature at 2m height (°C)
   - relative_humidity: Relative humidity at 2m (%)
   - rain: Rainfall amount (mm)
   - wind_speed: Wind speed at 10m height (km/h)
   - solar_radiation: Shortwave radiation GHI (W/m²)
   - soil_temperature: Soil temp at 0-7cm depth (°C)
   - soil_moisture: Volumetric soil moisture (m³/m³)
   - weather_code: WMO weather interpretation code

4. ALERT THRESHOLDS:
   - is_anomaly() method checks if values are concerning
   - Thresholds based on Malaysian climate and crop needs
   - Used by Alert System to notify farmers
   - Can be customized per crop type in future

5. DATABASE PERFORMANCE:
   - Composite index (user_id, timestamp) speeds up common queries
   - Without index: Database scans all rows (slow)
   - With index: Database jumps directly to relevant rows (fast)
   - Critical for apps with lots of sensor data

6. RELATIONSHIP TO OTHER FEATURES:
   - Dashboard: Displays latest reading
   - Weather Alerts: Checks is_anomaly() every 30 seconds
   - Pest Prediction: Uses temp + humidity to predict pest risk
   - ML Processing: All fields used for model training
   - Historical Charts: Queries readings over time range

7. WMO WEATHER CODES:
   - 0: Clear sky
   - 1-3: Mainly clear, partly cloudy
   - 45, 48: Fog
   - 51-55: Drizzle (light to dense)
   - 61-65: Rain (slight to heavy)
   - 80-82: Rain showers
   - 95: Thunderstorm
"""
