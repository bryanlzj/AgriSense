"""
Pydantic schemas for sensor data.

These schemas define the structure for sensor data requests and responses.
They handle validation and serialization for the API.

Fields aligned with Open-Meteo API parameters for ML processing.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class SensorDataCreate(BaseModel):
    """
    Schema for creating new sensor data.

    Used when farmers or IoT devices submit new sensor readings.
    Fields aligned with Open-Meteo API parameters.
    """
    temperature: float = Field(
        ...,
        description="Temperature in Celsius (Open-Meteo: temperature_2m)",
        ge=-50,
        le=60
    )
    relative_humidity: float = Field(
        ...,
        description="Relative humidity percentage (Open-Meteo: relative_humidity_2m)",
        ge=0,
        le=100
    )
    rain: float = Field(
        default=0.0,
        description="Rainfall in millimeters (Open-Meteo: rain)",
        ge=0
    )
    wind_speed: float = Field(
        default=0.0,
        description="Wind speed in km/h (Open-Meteo: wind_speed_10m)",
        ge=0
    )
    solar_radiation: Optional[float] = Field(
        None,
        description="Shortwave solar radiation (GHI) in W/m² (Open-Meteo: shortwave_radiation)",
        ge=0
    )
    soil_temperature: Optional[float] = Field(
        None,
        description="Soil temperature at 0-7cm depth in Celsius (Open-Meteo: soil_temperature_0_to_7cm)",
        ge=-20,
        le=60
    )
    soil_moisture: float = Field(
        ...,
        description="Volumetric soil moisture in m³/m³ (Open-Meteo: soil_moisture_0_to_7cm)",
        ge=0,
        le=1.0
    )
    weather_code: Optional[int] = Field(
        None,
        description="WMO weather interpretation code (Open-Meteo: weather_code)"
    )

    @validator('temperature')
    def validate_temperature(cls, v):
        """Validate temperature is within reasonable range."""
        if v < -50 or v > 60:
            raise ValueError('Temperature must be between -50°C and 60°C')
        return v

    @validator('relative_humidity')
    def validate_relative_humidity(cls, v):
        """Validate relative humidity is a valid percentage."""
        if v < 0 or v > 100:
            raise ValueError('Relative humidity must be between 0% and 100%')
        return v

    @validator('soil_moisture')
    def validate_soil_moisture(cls, v):
        """Validate soil moisture is a valid volumetric value."""
        if v < 0 or v > 1.0:
            raise ValueError('Soil moisture must be between 0 and 1.0 m³/m³')
        return v

    @validator('weather_code')
    def validate_weather_code(cls, v):
        """Validate weather code is a valid WMO code."""
        if v is not None and (v < 0 or v > 99):
            raise ValueError('Weather code must be between 0 and 99')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 28.5,
                "relative_humidity": 75.0,
                "rain": 0.0,
                "wind_speed": 12.5,
                "solar_radiation": 650.0,
                "soil_temperature": 26.0,
                "soil_moisture": 0.35,
                "weather_code": 1
            }
        }


class SensorDataResponse(BaseModel):
    """
    Schema for sensor data responses.

    Returned when retrieving sensor data from the API.
    """
    id: int
    user_id: int
    temperature: float
    relative_humidity: float
    rain: float
    wind_speed: float
    solar_radiation: Optional[float]
    soil_temperature: Optional[float]
    soil_moisture: float
    weather_code: Optional[int]
    weather_condition: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "temperature": 28.5,
                "relative_humidity": 75.0,
                "rain": 0.0,
                "wind_speed": 12.5,
                "solar_radiation": 650.0,
                "soil_temperature": 26.0,
                "soil_moisture": 0.35,
                "weather_code": 1,
                "timestamp": "2025-01-15T10:30:00"
            }
        }


class SensorDataUpdate(BaseModel):
    """
    Schema for updating sensor data.

    All fields are optional to allow partial updates.
    """
    temperature: Optional[float] = Field(None, ge=-50, le=60)
    relative_humidity: Optional[float] = Field(None, ge=0, le=100)
    rain: Optional[float] = Field(None, ge=0)
    wind_speed: Optional[float] = Field(None, ge=0)
    solar_radiation: Optional[float] = Field(None, ge=0)
    soil_temperature: Optional[float] = Field(None, ge=-20, le=60)
    soil_moisture: Optional[float] = Field(None, ge=0, le=1.0)
    weather_code: Optional[int] = Field(None, ge=0, le=99)

    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 29.0,
                "relative_humidity": 78.0,
                "soil_moisture": 0.40
            }
        }


class SensorDataFilter(BaseModel):
    """
    Schema for filtering sensor data queries.

    Used to filter sensor data by date range and other criteria.
    """
    start_date: Optional[datetime] = Field(
        None,
        description="Start date for filtering (inclusive)"
    )
    end_date: Optional[datetime] = Field(
        None,
        description="End date for filtering (inclusive)"
    )
    min_temperature: Optional[float] = Field(None, description="Minimum temperature (°C)")
    max_temperature: Optional[float] = Field(None, description="Maximum temperature (°C)")
    min_humidity: Optional[float] = Field(None, description="Minimum relative humidity (%)")
    max_humidity: Optional[float] = Field(None, description="Maximum relative humidity (%)")
    min_rain: Optional[float] = Field(None, description="Minimum rainfall (mm)")
    max_rain: Optional[float] = Field(None, description="Maximum rainfall (mm)")
    min_wind_speed: Optional[float] = Field(None, description="Minimum wind speed (km/h)")
    max_wind_speed: Optional[float] = Field(None, description="Maximum wind speed (km/h)")
    weather_code: Optional[int] = Field(None, description="Filter by specific WMO weather code")

    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2025-01-01T00:00:00",
                "end_date": "2025-01-31T23:59:59",
                "min_temperature": 20.0,
                "max_temperature": 35.0
            }
        }
