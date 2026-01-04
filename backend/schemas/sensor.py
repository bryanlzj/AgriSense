"""
Pydantic schemas for sensor data.

These schemas define the structure for sensor data requests and responses.
They handle validation and serialization for the API.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional


class SensorDataCreate(BaseModel):
    """
    Schema for creating new sensor data.
    
    Used when farmers or IoT devices submit new sensor readings.
    """
    temperature: float = Field(
        ..., 
        description="Temperature in Celsius",
        ge=-50,  # Greater than or equal to -50°C
        le=60    # Less than or equal to 60°C
    )
    humidity: float = Field(
        ..., 
        description="Relative humidity percentage",
        ge=0,    # Greater than or equal to 0%
        le=100   # Less than or equal to 100%
    )
    soil_moisture: float = Field(
        ...,
        description="Soil moisture percentage",
        ge=0,
        le=100
    )
    light_intensity: float = Field(
        ...,
        description="Light intensity in lux",
        ge=0
    )
    
    @validator('temperature')
    def validate_temperature(cls, v):
        """Validate temperature is within reasonable range."""
        if v < -50 or v > 60:
            raise ValueError('Temperature must be between -50°C and 60°C')
        return v
    
    @validator('humidity')
    def validate_humidity(cls, v):
        """Validate humidity is a valid percentage."""
        if v < 0 or v > 100:
            raise ValueError('Humidity must be between 0% and 100%')
        return v
    
    @validator('soil_moisture')
    def validate_soil_moisture(cls, v):
        """Validate soil moisture is a valid percentage."""
        if v < 0 or v > 100:
            raise ValueError('Soil moisture must be between 0% and 100%')
        return v
    
    @validator('light_intensity')
    def validate_light_intensity(cls, v):
        """Validate light intensity is non-negative."""
        if v < 0:
            raise ValueError('Light intensity cannot be negative')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 28.5,
                "humidity": 75.0,
                "soil_moisture": 65.0,
                "light_intensity": 50000.0
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
    humidity: float
    soil_moisture: float
    light_intensity: float
    timestamp: datetime
    
    class Config:
        from_attributes = True  # Allows creating from ORM models
        json_schema_extra = {
            "example": {
                "id": 1,
                "user_id": 1,
                "temperature": 28.5,
                "humidity": 75.0,
                "soil_moisture": 65.0,
                "light_intensity": 50000.0,
                "timestamp": "2024-01-15T10:30:00"
            }
        }


class SensorDataUpdate(BaseModel):
    """
    Schema for updating sensor data.
    
    All fields are optional to allow partial updates.
    """
    temperature: Optional[float] = Field(None, ge=-50, le=60)
    humidity: Optional[float] = Field(None, ge=0, le=100)
    soil_moisture: Optional[float] = Field(None, ge=0, le=100)
    light_intensity: Optional[float] = Field(None, ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": 29.0,
                "humidity": 78.0,
                "soil_moisture": 70.0
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
    min_temperature: Optional[float] = Field(None, description="Minimum temperature")
    max_temperature: Optional[float] = Field(None, description="Maximum temperature")
    min_humidity: Optional[float] = Field(None, description="Minimum humidity")
    max_humidity: Optional[float] = Field(None, description="Maximum humidity")
    
    class Config:
        json_schema_extra = {
            "example": {
                "start_date": "2024-01-01T00:00:00",
                "end_date": "2024-01-31T23:59:59",
                "min_temperature": 20.0,
                "max_temperature": 35.0
            }
        }
