"""
Alert Model

This module defines the Alert database model for notifications.

Supports DUAL CORE FEATURES:
- 🌤️ Weather Early Warning System alerts (heavy rain, storms, extreme heat)
- 🐛 Pest Risk Management System alerts (high confidence detections)

Learning Notes:
- Alerts notify users of critical conditions requiring immediate attention
- Alert types are defined by enum for type safety
- Severity levels help prioritize user response
- is_read flag tracks which alerts have been acknowledged
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from enum import Enum

from database import Base


# ============================================================================
# ENUMS
# ============================================================================

class AlertType(str, Enum):
    """
    Types of alerts in the system
    
    Weather Alerts (CORE FEATURE #1):
    - HEAVY_RAIN: Precipitation > 50mm forecast
    - EXTREME_HEAT: Temperature > 35°C
    - STORM_WARNING: Wind speed > 40 km/h
    - LOW_TEMPERATURE: Temperature < 15°C
    
    Pest Alerts (CORE FEATURE #2):
    - PEST_RISK: High confidence pest detection (>80%)
    
    Environmental Alerts:
    - LOW_SOIL_MOISTURE: Soil moisture < 40%
    - HIGH_HUMIDITY: Humidity > 85%
    
    System Alerts:
    - SYSTEM: General system notifications
    """
    # Weather Early Warning System (CORE FEATURE #1)
    HEAVY_RAIN = "heavy_rain"
    EXTREME_HEAT = "extreme_heat"
    STORM_WARNING = "storm_warning"
    LOW_TEMPERATURE = "low_temperature"
    
    # Pest Risk Management System (CORE FEATURE #2)
    PEST_RISK = "pest_risk"
    
    # Environmental Monitoring
    LOW_SOIL_MOISTURE = "low_soil_moisture"
    HIGH_HUMIDITY = "high_humidity"
    
    # System
    SYSTEM = "system"


class AlertSeverity(str, Enum):
    """
    Severity levels for alerts
    
    - LOW: Informational, no immediate action required
    - MEDIUM: Attention needed, plan response
    - HIGH: Urgent, immediate action required
    - CRITICAL: Emergency, act now to prevent damage
    """
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ============================================================================
# ALERT MODEL
# ============================================================================

class Alert(Base):
    """
    Alert Model
    
    Represents notifications for weather warnings, pest risks, and environmental conditions.
    
    Table: alerts
    """
    
    __tablename__ = "alerts"
    
    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique alert identifier"
    )
    
    # Foreign Key to User
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="User who receives this alert"
    )
    
    # Alert Classification
    alert_type = Column(
        SQLEnum(AlertType),
        nullable=False,
        index=True,
        comment="Type of alert (weather, pest, environmental, system)"
    )
    
    severity = Column(
        SQLEnum(AlertSeverity),
        nullable=False,
        default=AlertSeverity.MEDIUM,
        index=True,
        comment="Severity level (low, medium, high, critical)"
    )
    
    # Alert Content
    title = Column(
        String(200),
        nullable=False,
        comment="Short alert title (e.g., 'Heavy Rain Warning')"
    )
    
    message = Column(
        Text,
        nullable=False,
        comment="Detailed alert message with context and recommendations"
    )
    
    # Optional: Actionable recommendations
    recommendations = Column(
        Text,
        nullable=True,
        comment="Specific actions user should take (JSON array or text)"
    )
    
    # Alert Status
    is_read = Column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
        comment="Whether user has acknowledged this alert"
    )
    
    read_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="When the alert was marked as read"
    )
    
    # Optional: Alert expiration
    expires_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="When this alert is no longer relevant (optional)"
    )
    
    # Metadata
    metadata = Column(
        Text,
        nullable=True,
        comment="Additional data (JSON) - e.g., weather values, pest confidence"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="When the alert was generated"
    )
    
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last time alert was updated"
    )
    
    # Relationships
    user = relationship(
        "User",
        back_populates="alerts"
    )
    
    # Indexes for performance
    __table_args__ = (
        # Composite index for common queries
        Index('idx_user_unread_created', 'user_id', 'is_read', 'created_at'),
        Index('idx_user_type_severity', 'user_id', 'alert_type', 'severity'),
        Index('idx_severity_created', 'severity', 'created_at'),
        {'comment': 'Alerts table for weather warnings, pest risks, and notifications'}
    )
    
    def __repr__(self):
        """String representation for debugging"""
        return (
            f"<Alert(id={self.id}, type={self.alert_type.value}, "
            f"severity={self.severity.value}, read={self.is_read})>"
        )
    
    def to_dict(self):
        """
        Convert alert object to dictionary (for API responses)
        """
        return {
            "id": self.id,
            "user_id": self.user_id,
            "alert_type": self.alert_type.value,
            "severity": self.severity.value,
            "title": self.title,
            "message": self.message,
            "recommendations": self.recommendations,
            "is_read": self.is_read,
            "read_at": self.read_at.isoformat() if self.read_at else None,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def mark_as_read(self):
        """
        Mark this alert as read
        
        Usage:
            alert = db.query(Alert).filter(Alert.id == alert_id).first()
            alert.mark_as_read()
            db.commit()
        """
        self.is_read = True
        self.read_at = datetime.utcnow()
    
    def is_expired(self) -> bool:
        """
        Check if alert has expired
        
        Returns:
            bool: True if alert has passed expiration time
        """
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_urgent(self) -> bool:
        """
        Check if alert requires urgent attention
        
        Returns:
            bool: True if severity is HIGH or CRITICAL
        """
        return self.severity in [AlertSeverity.HIGH, AlertSeverity.CRITICAL]
    
    @classmethod
    def get_unread_count(cls, db, user_id: int) -> int:
        """
        Get count of unread alerts for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            int: Number of unread alerts
            
        Usage:
            count = Alert.get_unread_count(db, user_id=1)
        """
        return db.query(cls).filter(
            cls.user_id == user_id,
            cls.is_read == False
        ).count()
    
    @classmethod
    def get_urgent_alerts(cls, db, user_id: int):
        """
        Get all urgent (HIGH/CRITICAL) unread alerts for a user
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of urgent Alert objects
            
        Usage:
            urgent = Alert.get_urgent_alerts(db, user_id=1)
        """
        return db.query(cls).filter(
            cls.user_id == user_id,
            cls.is_read == False,
            cls.severity.in_([AlertSeverity.HIGH, AlertSeverity.CRITICAL])
        ).order_by(cls.created_at.desc()).all()


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def create_weather_alert(
    db,
    user_id: int,
    alert_type: AlertType,
    title: str,
    message: str,
    severity: AlertSeverity = AlertSeverity.MEDIUM,
    recommendations: str = None,
    metadata: str = None,
    expires_at: datetime = None
) -> Alert:
    """
    Helper function to create weather-related alerts
    
    Args:
        db: Database session
        user_id: User ID to receive alert
        alert_type: Type of weather alert (HEAVY_RAIN, EXTREME_HEAT, etc.)
        title: Alert title
        message: Alert message
        severity: Alert severity level
        recommendations: Actionable recommendations (optional)
        metadata: Additional data as JSON string (optional)
        expires_at: When alert expires (optional)
        
    Returns:
        Alert: Created alert object
        
    Usage:
        alert = create_weather_alert(
            db,
            user_id=1,
            alert_type=AlertType.HEAVY_RAIN,
            title="Heavy Rain Warning",
            message="Heavy rain (65mm) expected tomorrow. Prepare drainage.",
            severity=AlertSeverity.HIGH,
            recommendations="Cover crops, prepare drainage, secure equipment"
        )
        db.commit()
    """
    alert = Alert(
        user_id=user_id,
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
        recommendations=recommendations,
        metadata=metadata,
        expires_at=expires_at
    )
    db.add(alert)
    return alert


def create_pest_alert(
    db,
    user_id: int,
    pest_name: str,
    confidence: float,
    severity: AlertSeverity = AlertSeverity.HIGH,
    recommendations: str = None,
    metadata: str = None
) -> Alert:
    """
    Helper function to create pest risk alerts
    
    Args:
        db: Database session
        user_id: User ID to receive alert
        pest_name: Name of detected pest
        confidence: Detection confidence (0-1)
        severity: Alert severity level
        recommendations: Treatment recommendations (optional)
        metadata: Additional data as JSON string (optional)
        
    Returns:
        Alert: Created alert object
        
    Usage:
        alert = create_pest_alert(
            db,
            user_id=1,
            pest_name="Fall Armyworm",
            confidence=0.87,
            severity=AlertSeverity.HIGH,
            recommendations="Apply neem oil spray, remove affected leaves"
        )
        db.commit()
    """
    title = f"Pest Risk Alert: {pest_name}"
    message = (
        f"High confidence ({confidence*100:.1f}%) detection of {pest_name}. "
        f"Immediate action recommended to prevent spread."
    )
    
    alert = Alert(
        user_id=user_id,
        alert_type=AlertType.PEST_RISK,
        severity=severity,
        title=title,
        message=message,
        recommendations=recommendations,
        metadata=metadata
    )
    db.add(alert)
    return alert


def create_environmental_alert(
    db,
    user_id: int,
    alert_type: AlertType,
    title: str,
    message: str,
    severity: AlertSeverity = AlertSeverity.LOW,
    recommendations: str = None,
    metadata: str = None
) -> Alert:
    """
    Helper function to create environmental monitoring alerts
    
    Args:
        db: Database session
        user_id: User ID to receive alert
        alert_type: Type of environmental alert (LOW_SOIL_MOISTURE, HIGH_HUMIDITY)
        title: Alert title
        message: Alert message
        severity: Alert severity level
        recommendations: Actionable recommendations (optional)
        metadata: Additional data as JSON string (optional)
        
    Returns:
        Alert: Created alert object
        
    Usage:
        alert = create_environmental_alert(
            db,
            user_id=1,
            alert_type=AlertType.LOW_SOIL_MOISTURE,
            title="Low Soil Moisture",
            message="Soil moisture at 28%. Irrigation recommended.",
            severity=AlertSeverity.MEDIUM,
            recommendations="Increase irrigation frequency"
        )
        db.commit()
    """
    alert = Alert(
        user_id=user_id,
        alert_type=alert_type,
        severity=severity,
        title=title,
        message=message,
        recommendations=recommendations,
        metadata=metadata
    )
    db.add(alert)
    return alert


# ============================================================================
# LEARNING NOTES
# ============================================================================

"""
📚 Key Concepts Explained:

1. **Alert System Design:**
   - Unified system for BOTH weather AND pest alerts
   - Type-safe enums prevent invalid alert types
   - Severity levels help users prioritize responses
   - Read/unread tracking for user experience

2. **Alert Types (Dual Core Features):**
   
   🌤️ Weather Early Warning System:
   - HEAVY_RAIN: > 50mm precipitation forecast
   - EXTREME_HEAT: Temperature > 35°C
   - STORM_WARNING: Wind speed > 40 km/h
   - LOW_TEMPERATURE: Temperature < 15°C
   
   🐛 Pest Risk Management System:
   - PEST_RISK: High confidence pest detection (>80%)
   
   Environmental Monitoring:
   - LOW_SOIL_MOISTURE: Soil moisture < 40%
   - HIGH_HUMIDITY: Humidity > 85%

3. **Severity Levels:**
   - LOW: Informational (e.g., "Soil moisture slightly low")
   - MEDIUM: Attention needed (e.g., "Increase irrigation")
   - HIGH: Urgent action (e.g., "Heavy rain expected, cover crops")
   - CRITICAL: Emergency (e.g., "Storm approaching, secure equipment")

4. **Alert Lifecycle:**
   - Created: Alert generated by system
   - Unread: User hasn't seen it yet (is_read=False)
   - Read: User acknowledged (is_read=True, read_at set)
   - Expired: Past expires_at time (optional)

5. **Database Indexes:**
   - idx_user_unread_created: Fast queries for "show unread alerts"
   - idx_user_type_severity: Filter by type and severity
   - idx_severity_created: Get all urgent alerts system-wide

6. **Helper Functions:**
   - create_weather_alert(): Standardized weather alert creation
   - create_pest_alert(): Standardized pest alert creation
   - create_environmental_alert(): Standardized environmental alert creation
   - These ensure consistent alert format and reduce code duplication

7. **Metadata Field:**
   - Stores additional data as JSON string
   - Example for weather: {"temperature": 36, "forecast_date": "2025-01-16"}
   - Example for pest: {"confidence": 0.87, "image_url": "/uploads/123.jpg"}
   - Flexible for future enhancements

8. **Cascade Delete:**
   - When user is deleted, all their alerts are deleted
   - Prevents orphaned alerts in database
   - Defined in relationship: ondelete="CASCADE"

Example Usage:

    # Create weather alert
    from models.alert import create_weather_alert, AlertType, AlertSeverity
    
    alert = create_weather_alert(
        db,
        user_id=1,
        alert_type=AlertType.HEAVY_RAIN,
        title="Heavy Rain Warning",
        message="Heavy rain (65mm) expected tomorrow. Prepare drainage.",
        severity=AlertSeverity.HIGH,
        recommendations="Cover crops, prepare drainage, secure equipment"
    )
    db.commit()
    
    # Create pest alert
    from models.alert import create_pest_alert
    
    alert = create_pest_alert(
        db,
        user_id=1,
        pest_name="Fall Armyworm",
        confidence=0.87,
        recommendations="Apply neem oil spray, remove affected leaves"
    )
    db.commit()
    
    # Get unread alerts
    unread = db.query(Alert).filter(
        Alert.user_id == 1,
        Alert.is_read == False
    ).order_by(Alert.created_at.desc()).all()
    
    # Mark alert as read
    alert = db.query(Alert).filter(Alert.id == 1).first()
    alert.mark_as_read()
    db.commit()
    
    # Get unread count
    count = Alert.get_unread_count(db, user_id=1)
    
    # Get urgent alerts
    urgent = Alert.get_urgent_alerts(db, user_id=1)

Next Steps:
- Run Alembic migration to create alerts table
- Implement alert generation service (Task 1.8)
- Create API endpoints for alerts (Task 1.9)
- Integrate with weather and pest detection systems
"""
