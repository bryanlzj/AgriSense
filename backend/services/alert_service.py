"""
Alert Service

This module provides automated alert generation based on:
- Sensor data thresholds
- Weather conditions
- Pest detections

Learning Notes:
- This service runs as a background task
- It checks sensor data, weather, and pest detections periodically
- It generates alerts when thresholds are exceeded
- Alerts are stored in the database and can be retrieved via API

Alert Generation Rules:
1. Sensor Alerts:
   - High temperature (>32°C) → Warning
   - Low temperature (<18°C) → Warning
   - High humidity (>85%) → Warning
   - Low soil moisture (<30%) → Critical
   
2. Weather Alerts:
   - Heavy rain → Warning
   - Strong wind → Warning
   - Extreme temperature → Critical
   
3. Pest Alerts:
   - High confidence detection (>80%) → Warning
   - Multiple detections in short time → Critical
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from datetime import datetime, timedelta
from typing import List, Optional
import json
import logging

from models.alert import Alert, AlertType, AlertSeverity
from models.sensor_reading import SensorReading
from models.pest_detection import PestDetection

logger = logging.getLogger(__name__)


class AlertService:
    """Service for automated alert generation"""
    
    # Alert thresholds (from config)
    TEMP_HIGH_THRESHOLD = 32.0
    TEMP_LOW_THRESHOLD = 18.0
    HUMIDITY_HIGH_THRESHOLD = 85.0
    SOIL_MOISTURE_LOW_THRESHOLD = 0.2  # Volumetric m³/m³
    WIND_SPEED_HIGH_THRESHOLD = 50.0  # km/h
    RAIN_HEAVY_THRESHOLD = 10.0  # mm
    PEST_CONFIDENCE_THRESHOLD = 0.80
    
    @staticmethod
    def create_alert(
        db: Session,
        user_id: int,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        message: str,
        metadata: Optional[dict] = None
    ) -> Alert:
        """
        Create a new alert.

        Args:
            db: Database session
            user_id: User ID
            alert_type: Type of alert (model AlertType enum)
            severity: Severity level (model AlertSeverity enum)
            title: Alert title
            message: Alert message
            metadata: Additional metadata dict (stored as JSON string)

        Returns:
            Created alert
        """
        alert = Alert(
            user_id=user_id,
            alert_type=alert_type,
            severity=severity,
            title=title,
            message=message,
            alert_metadata=json.dumps(metadata) if metadata else None,
            is_read=False,
            is_acknowledged=False
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)
        return alert
    
    @staticmethod
    def check_sensor_alerts(db: Session, user_id: int) -> List[Alert]:
        """
        Check sensor data and generate alerts if thresholds are exceeded.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of generated alerts
        """
        alerts = []

        # Get latest sensor data (last 5 minutes)
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        recent_data = db.query(SensorReading).filter(
            SensorReading.user_id == user_id,
            SensorReading.timestamp >= five_minutes_ago
        ).order_by(desc(SensorReading.timestamp)).first()

        if not recent_data:
            return alerts

        # Check if we already have recent alerts (prevent duplicates within 1 hour)
        recent_alert_time = datetime.utcnow() - timedelta(hours=1)

        # High temperature alert
        if recent_data.temperature > AlertService.TEMP_HIGH_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.EXTREME_HEAT,
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.EXTREME_HEAT,
                    severity=AlertSeverity.HIGH,
                    title="High Temperature Alert",
                    message=f"Temperature has reached {recent_data.temperature}°C, exceeding the threshold of {AlertService.TEMP_HIGH_THRESHOLD}°C. Consider irrigation or shade protection.",
                    metadata={
                        "temperature": recent_data.temperature,
                        "threshold": AlertService.TEMP_HIGH_THRESHOLD,
                        "sensor_reading_id": recent_data.id,
                    }
                )
                alerts.append(alert)

        # Low temperature alert
        if recent_data.temperature < AlertService.TEMP_LOW_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.LOW_TEMPERATURE,
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.LOW_TEMPERATURE,
                    severity=AlertSeverity.MEDIUM,
                    title="Low Temperature Alert",
                    message=f"Temperature has dropped to {recent_data.temperature}°C, below the threshold of {AlertService.TEMP_LOW_THRESHOLD}°C. Consider frost protection measures.",
                    metadata={
                        "temperature": recent_data.temperature,
                        "threshold": AlertService.TEMP_LOW_THRESHOLD,
                        "sensor_reading_id": recent_data.id,
                    }
                )
                alerts.append(alert)

        # High humidity alert
        if recent_data.relative_humidity > AlertService.HUMIDITY_HIGH_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.HIGH_HUMIDITY,
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.HIGH_HUMIDITY,
                    severity=AlertSeverity.MEDIUM,
                    title="High Humidity Alert",
                    message=f"Humidity has reached {recent_data.relative_humidity}%, exceeding the threshold of {AlertService.HUMIDITY_HIGH_THRESHOLD}%. Increased risk of fungal diseases.",
                    metadata={
                        "relative_humidity": recent_data.relative_humidity,
                        "threshold": AlertService.HUMIDITY_HIGH_THRESHOLD,
                        "sensor_reading_id": recent_data.id,
                    }
                )
                alerts.append(alert)

        # High wind speed alert
        if recent_data.wind_speed and recent_data.wind_speed > AlertService.WIND_SPEED_HIGH_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.STORM_WARNING,
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.STORM_WARNING,
                    severity=AlertSeverity.HIGH,
                    title="Strong Wind Alert",
                    message=f"Wind speed has reached {recent_data.wind_speed} km/h, exceeding the threshold of {AlertService.WIND_SPEED_HIGH_THRESHOLD} km/h. Consider protecting vulnerable crops.",
                    metadata={
                        "wind_speed": recent_data.wind_speed,
                        "threshold": AlertService.WIND_SPEED_HIGH_THRESHOLD,
                        "sensor_reading_id": recent_data.id,
                    }
                )
                alerts.append(alert)

        # Heavy rain alert
        if recent_data.rain and recent_data.rain > AlertService.RAIN_HEAVY_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.HEAVY_RAIN,
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.HEAVY_RAIN,
                    severity=AlertSeverity.HIGH,
                    title="Heavy Rain Alert",
                    message=f"Rainfall has reached {recent_data.rain} mm, exceeding the threshold of {AlertService.RAIN_HEAVY_THRESHOLD} mm. Check drainage and potential flooding.",
                    metadata={
                        "rain": recent_data.rain,
                        "threshold": AlertService.RAIN_HEAVY_THRESHOLD,
                        "sensor_reading_id": recent_data.id,
                    }
                )
                alerts.append(alert)

        # Low soil moisture alert (CRITICAL)
        if recent_data.soil_moisture < AlertService.SOIL_MOISTURE_LOW_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.LOW_SOIL_MOISTURE,
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.LOW_SOIL_MOISTURE,
                    severity=AlertSeverity.CRITICAL,
                    title="Low Soil Moisture Alert",
                    message=f"Soil moisture has dropped to {recent_data.soil_moisture:.3f} m³/m³, below the critical threshold of {AlertService.SOIL_MOISTURE_LOW_THRESHOLD} m³/m³. Immediate irrigation required.",
                    metadata={
                        "soil_moisture": recent_data.soil_moisture,
                        "threshold": AlertService.SOIL_MOISTURE_LOW_THRESHOLD,
                        "sensor_reading_id": recent_data.id,
                    }
                )
                alerts.append(alert)

        return alerts
    
    @staticmethod
    def check_pest_alerts(db: Session, user_id: int) -> List[Alert]:
        """
        Check pest detections and generate alerts for high confidence detections.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            List of generated alerts
        """
        alerts = []

        # Get recent pest detections (last 24 hours)
        one_day_ago = datetime.utcnow() - timedelta(days=1)
        recent_detections = db.query(PestDetection).filter(
            PestDetection.user_id == user_id,
            PestDetection.detected_at >= one_day_ago
        ).order_by(desc(PestDetection.detected_at)).all()

        if not recent_detections:
            return alerts

        recent_alert_time = datetime.utcnow() - timedelta(hours=6)

        for detection in recent_detections:
            # Skip if we already have a recent alert for this pest type
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.PEST_DETECTION,
                Alert.title.like(f"%{detection.pest_type}%"),
                Alert.created_at >= recent_alert_time
            ).first()

            if existing:
                continue

            # High confidence detection
            if detection.confidence >= AlertService.PEST_CONFIDENCE_THRESHOLD:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.PEST_DETECTION,
                    severity=AlertSeverity.HIGH,
                    title=f"Pest Detected: {detection.pest_type}",
                    message=f"High confidence ({detection.confidence*100:.1f}%) detection of {detection.pest_type}. Recommended action: {detection.recommended_action}",
                    metadata={
                        "pest_type": detection.pest_type,
                        "confidence": detection.confidence,
                        "detection_id": detection.id,
                    }
                )
                alerts.append(alert)

        # Check for multiple detections (potential outbreak)
        if len(recent_detections) >= 3:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == AlertType.PEST_RISK,
                Alert.title.like("%Multiple Pest%"),
                Alert.created_at >= recent_alert_time
            ).first()

            if not existing:
                pest_types = list(set([d.pest_type for d in recent_detections]))
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.PEST_RISK,
                    severity=AlertSeverity.CRITICAL,
                    title="Multiple Pest Detections",
                    message=f"Multiple pest detections ({len(recent_detections)}) in the last 24 hours. Pest types: {', '.join(pest_types)}. Consider immediate pest control measures.",
                    metadata={
                        "detection_count": len(recent_detections),
                        "pest_types": pest_types,
                    }
                )
                alerts.append(alert)

        return alerts
    
    @staticmethod
    def check_weather_alerts(db: Session, user_id: int, weather_alerts: List[dict]) -> List[Alert]:
        """
        Generate alerts from weather service alerts.

        Args:
            db: Database session
            user_id: User ID
            weather_alerts: List of weather alerts from weather service

        Returns:
            List of generated alerts
        """
        alerts = []

        if not weather_alerts:
            return alerts

        recent_alert_time = datetime.utcnow() - timedelta(hours=6)

        # Map weather alert titles to specific AlertType
        type_map = {
            "heavy rain": AlertType.HEAVY_RAIN,
            "extreme heat": AlertType.EXTREME_HEAT,
            "storm": AlertType.STORM_WARNING,
            "low temperature": AlertType.LOW_TEMPERATURE,
        }

        # Map weather severity strings to model AlertSeverity
        severity_map = {
            "info": AlertSeverity.LOW,
            "low": AlertSeverity.LOW,
            "warning": AlertSeverity.MEDIUM,
            "medium": AlertSeverity.MEDIUM,
            "high": AlertSeverity.HIGH,
            "critical": AlertSeverity.CRITICAL,
        }

        for weather_alert in weather_alerts:
            title = weather_alert.get("title", "Weather Alert")

            # Determine alert type from title
            alert_type = AlertType.STORM_WARNING  # default
            for keyword, atype in type_map.items():
                if keyword in title.lower():
                    alert_type = atype
                    break

            # Check for duplicates
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.alert_type == alert_type,
                Alert.title == title,
                Alert.created_at >= recent_alert_time
            ).first()

            if existing:
                continue

            severity = severity_map.get(
                weather_alert.get("severity", "medium"),
                AlertSeverity.MEDIUM
            )

            alert = AlertService.create_alert(
                db=db,
                user_id=user_id,
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=weather_alert.get("message", "Weather conditions require attention."),
                metadata=weather_alert
            )
            alerts.append(alert)

        return alerts
    
    @staticmethod
    def run_alert_checks(db: Session, user_id: int, weather_alerts: Optional[List[dict]] = None) -> List[Alert]:
        """
        Run all alert checks and return generated alerts
        
        Args:
            db: Database session
            user_id: User ID
            weather_alerts: Optional weather alerts from weather service
            
        Returns:
            List of all generated alerts
        """
        all_alerts = []
        
        # Check sensor alerts
        sensor_alerts = AlertService.check_sensor_alerts(db, user_id)
        all_alerts.extend(sensor_alerts)
        
        # Check pest alerts
        pest_alerts = AlertService.check_pest_alerts(db, user_id)
        all_alerts.extend(pest_alerts)
        
        # Check weather alerts
        if weather_alerts:
            weather_alert_objs = AlertService.check_weather_alerts(db, user_id, weather_alerts)
            all_alerts.extend(weather_alert_objs)
        
        return all_alerts
