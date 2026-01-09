"""
Pest-Weather Correlation Model

This module defines the reference data table for pest-weather correlations.
Used to predict pest risk based on weather conditions.

Learning Notes:
- This is reference data (not user-specific)
- JSONB columns store flexible structured data
- Used to check weather against risk conditions
- Correlations are filtered by user's crop type
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from database import Base


class PestWeatherCorrelation(Base):
    """
    Pest-Weather Correlation Model

    Stores reference data linking weather conditions to pest outbreak risk.
    Used for pest risk early warning system (PRD v2 Section 5.4).

    Table: pest_weather_correlations
    """

    __tablename__ = "pest_weather_correlations"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique correlation identifier"
    )

    # Pest Information
    pest_name = Column(
        String(100),
        nullable=False,
        index=True,
        comment="Common name of the pest (e.g., Rice Stem Borer)"
    )

    scientific_name = Column(
        String(150),
        nullable=True,
        comment="Scientific name of the pest (e.g., Scirpophaga incertulas)"
    )

    # Affected Crops (JSONB array)
    # Example: ["rice", "vegetables"]
    affected_crops = Column(
        JSONB,
        nullable=False,
        comment="Array of crop types affected by this pest"
    )

    # Risk Conditions (JSONB object)
    # Example: {"temp_min": 25, "temp_max": 35, "humidity_min": 70, "trigger": "after_rain"}
    risk_conditions = Column(
        JSONB,
        nullable=False,
        comment="Weather conditions that increase risk (temp, humidity, triggers)"
    )

    # Risk Level
    risk_level = Column(
        String(20),
        nullable=False,
        comment="Risk severity: low, medium, high"
    )

    # Risk Message (shown to user in alerts)
    risk_message = Column(
        Text,
        nullable=False,
        comment="Descriptive message explaining the risk and pest behavior"
    )

    # Prevention Tips (JSONB array)
    # Example: ["Monitor fields daily", "Apply neem spray", "Remove infected plants"]
    prevention_tips = Column(
        JSONB,
        nullable=False,
        comment="Array of prevention/treatment recommendations"
    )

    # Data Source
    data_source = Column(
        String(200),
        nullable=True,
        comment="Source of correlation data (e.g., MARDI Guidelines, IRRI)"
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="When this correlation was added"
    )

    # Indexes for common queries
    __table_args__ = (
        Index('idx_correlations_risk_level', 'risk_level'),
        {'comment': 'Reference data for pest-weather correlations used in risk prediction'}
    )

    def __repr__(self):
        """String representation for debugging"""
        return f"<PestWeatherCorrelation(id={self.id}, pest='{self.pest_name}', risk='{self.risk_level}')>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "pest_name": self.pest_name,
            "scientific_name": self.scientific_name,
            "affected_crops": self.affected_crops,
            "risk_conditions": self.risk_conditions,
            "risk_level": self.risk_level,
            "risk_message": self.risk_message,
            "prevention_tips": self.prevention_tips,
            "data_source": self.data_source,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def matches_weather(self, temperature: float, humidity: float, recent_rain: bool = False) -> bool:
        """
        Check if current weather conditions match this pest's risk conditions.

        Args:
            temperature: Current temperature in Celsius
            humidity: Current humidity percentage
            recent_rain: Whether there was recent rainfall

        Returns:
            True if conditions match risk profile, False otherwise
        """
        conditions = self.risk_conditions or {}

        # Check temperature range
        temp_min = conditions.get("temp_min")
        temp_max = conditions.get("temp_max")
        if temp_min and temperature < temp_min:
            return False
        if temp_max and temperature > temp_max:
            return False

        # Check humidity range
        humidity_min = conditions.get("humidity_min")
        humidity_max = conditions.get("humidity_max")
        if humidity_min and humidity < humidity_min:
            return False
        if humidity_max and humidity > humidity_max:
            return False

        # Check trigger conditions
        trigger = conditions.get("trigger")
        if trigger == "after_rain" and not recent_rain:
            return False
        if trigger == "after_heavy_rain" and not recent_rain:
            return False

        return True


# ============================================================================
# LEARNING NOTES: Pest-Weather Correlations
# ============================================================================

"""
1. What is Pest Risk Prediction?
   - Uses weather data to predict pest outbreak probability
   - Farmers get warned BEFORE pests appear
   - Based on scientific research (MARDI, IRRI)
   - Each pest has specific weather preferences

2. How Risk Conditions Work:
   - temp_min/temp_max: Temperature range favoring pest
   - humidity_min/humidity_max: Humidity range
   - trigger: Special conditions (after_rain, dry_period, flooding)
   - condition: Weather type (cloudy, etc.)
   - stage: Crop growth stage (grain_filling, etc.)

3. Risk Levels:
   - LOW: Minor concern, monitor situation
   - MEDIUM: Increased vigilance needed
   - HIGH: Take immediate preventive action

4. How the System Uses This:
   1. Background job runs every 30 minutes
   2. Fetches current weather for user's location
   3. Queries correlations matching user's crop type
   4. Checks each correlation against current weather
   5. If conditions match, generates pest risk alert

5. Why JSONB Columns?
   - Flexible structure (different pests need different conditions)
   - Easy to query with PostgreSQL operators
   - Can add new condition types without schema changes
   - Supports arrays (affected_crops, prevention_tips)

6. Data Sources:
   - MARDI (Malaysian Agricultural Research and Development Institute)
   - IRRI (International Rice Research Institute)
   - PhilRice (Philippine Rice Research Institute)

Example Usage:
    # Check if weather matches pest risk
    correlation = db.query(PestWeatherCorrelation).filter(
        PestWeatherCorrelation.affected_crops.contains(["rice"])
    ).all()

    for c in correlations:
        if c.matches_weather(temperature=28, humidity=85, recent_rain=True):
            # Generate alert!
            create_pest_risk_alert(c, user)
"""
