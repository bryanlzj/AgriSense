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
from models.alert import Alert
from models.sensor_data import SensorData
from models.pest_detection import PestDetection
from schemas.alert import AlertType, AlertSeverity


class AlertService:
    """Service for automated alert generation"""
    
    # Alert thresholds (from config)
    TEMP_HIGH_THRESHOLD = 32.0
    TEMP_LOW_THRESHOLD = 18.0
    HUMIDITY_HIGH_THRESHOLD = 85.0
    SOIL_MOISTURE_LOW_THRESHOLD = 30.0
    PEST_CONFIDENCE_THRESHOLD = 0.80
    
    @staticmethod
    def create_alert(
        db: Session,
        user_id: int,
        alert_type: AlertType,
        severity: AlertSeverity,
        title: str,
        message: str,
        source_id: Optional[int] = None,
        source_type: Optional[str] = None,
        metadata: Optional[dict] = None
    ) -> Alert:
        """
        Create a new alert
        
        Args:
            db: Database session
            user_id: User ID
            alert_type: Type of alert
            severity: Severity level
            title: Alert title
            message: Alert message
            source_id: ID of source entity
            source_type: Type of source entity
            metadata: Additional metadata
            
        Returns:
            Created alert
        """
        alert = Alert(
            user_id=user_id,
            type=alert_type.value,
            severity=severity.value,
            title=title,
            message=message,
            source_id=source_id,
            source_type=source_type,
            metadata=metadata or {},
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
        Check sensor data and generate alerts if thresholds are exceeded
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of generated alerts
        """
        alerts = []
        
        # Get latest sensor data (last 5 minutes)
        five_minutes_ago = datetime.utcnow() - timedelta(minutes=5)
        recent_data = db.query(SensorData).filter(
            SensorData.user_id == user_id,
            SensorData.timestamp >= five_minutes_ago
        ).order_by(desc(SensorData.timestamp)).first()
        
        if not recent_data:
            return alerts
        
        # Check if we already have recent alerts for this sensor data
        recent_alert_time = datetime.utcnow() - timedelta(hours=1)
        
        # High temperature alert
        if recent_data.temperature > AlertService.TEMP_HIGH_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.SENSOR.value,
                Alert.title.like("%High Temperature%"),
                Alert.created_at >= recent_alert_time
            ).first()
            
            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.SENSOR,
                    severity=AlertSeverity.WARNING,
                    title="High Temperature Alert",
                    message=f"Temperature has reached {recent_data.temperature}°C, exceeding the threshold of {AlertService.TEMP_HIGH_THRESHOLD}°C. Consider irrigation or shade protection.",
                    source_id=recent_data.id,
                    source_type="sensor_data",
                    metadata={
                        "temperature": recent_data.temperature,
                        "threshold": AlertService.TEMP_HIGH_THRESHOLD,
                        "timestamp": recent_data.timestamp.isoformat()
                    }
                )
                alerts.append(alert)
        
        # Low temperature alert
        if recent_data.temperature < AlertService.TEMP_LOW_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.SENSOR.value,
                Alert.title.like("%Low Temperature%"),
                Alert.created_at >= recent_alert_time
            ).first()
            
            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.SENSOR,
                    severity=AlertSeverity.WARNING,
                    title="Low Temperature Alert",
                    message=f"Temperature has dropped to {recent_data.temperature}°C, below the threshold of {AlertService.TEMP_LOW_THRESHOLD}°C. Consider frost protection measures.",
                    source_id=recent_data.id,
                    source_type="sensor_data",
                    metadata={
                        "temperature": recent_data.temperature,
                        "threshold": AlertService.TEMP_LOW_THRESHOLD,
                        "timestamp": recent_data.timestamp.isoformat()
                    }
                )
                alerts.append(alert)
        
        # High humidity alert
        if recent_data.humidity > AlertService.HUMIDITY_HIGH_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.SENSOR.value,
                Alert.title.like("%High Humidity%"),
                Alert.created_at >= recent_alert_time
            ).first()
            
            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.SENSOR,
                    severity=AlertSeverity.WARNING,
                    title="High Humidity Alert",
                    message=f"Humidity has reached {recent_data.humidity}%, exceeding the threshold of {AlertService.HUMIDITY_HIGH_THRESHOLD}%. Increased risk of fungal diseases.",
                    source_id=recent_data.id,
                    source_type="sensor_data",
                    metadata={
                        "humidity": recent_data.humidity,
                        "threshold": AlertService.HUMIDITY_HIGH_THRESHOLD,
                        "timestamp": recent_data.timestamp.isoformat()
                    }
                )
                alerts.append(alert)
        
        # Low soil moisture alert (CRITICAL)
        if recent_data.soil_moisture < AlertService.SOIL_MOISTURE_LOW_THRESHOLD:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.SENSOR.value,
                Alert.title.like("%Low Soil Moisture%"),
                Alert.created_at >= recent_alert_time
            ).first()
            
            if not existing:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.SENSOR,
                    severity=AlertSeverity.CRITICAL,
                    title="Low Soil Moisture Alert",
                    message=f"Soil moisture has dropped to {recent_data.soil_moisture}%, below the critical threshold of {AlertService.SOIL_MOISTURE_LOW_THRESHOLD}%. Immediate irrigation required.",
                    source_id=recent_data.id,
                    source_type="sensor_data",
                    metadata={
                        "soil_moisture": recent_data.soil_moisture,
                        "threshold": AlertService.SOIL_MOISTURE_LOW_THRESHOLD,
                        "timestamp": recent_data.timestamp.isoformat()
                    }
                )
                alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def check_pest_alerts(db: Session, user_id: int) -> List[Alert]:
        """
        Check pest detections and generate alerts for high confidence detections
        
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
            PestDetection.created_at >= one_day_ago
        ).order_by(desc(PestDetection.created_at)).all()
        
        if not recent_detections:
            return alerts
        
        # Check for high confidence detections
        recent_alert_time = datetime.utcnow() - timedelta(hours=6)
        
        for detection in recent_detections:
            # Skip if we already have an alert for this detection
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.PEST.value,
                Alert.source_id == detection.id,
                Alert.source_type == "pest_detection"
            ).first()
            
            if existing:
                continue
            
            # High confidence detection
            if detection.confidence >= AlertService.PEST_CONFIDENCE_THRESHOLD:
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.PEST,
                    severity=AlertSeverity.WARNING,
                    title=f"Pest Detected: {detection.pest_type}",
                    message=f"High confidence ({detection.confidence*100:.1f}%) detection of {detection.pest_type}. Recommended action: {detection.recommended_action}",
                    source_id=detection.id,
                    source_type="pest_detection",
                    metadata={
                        "pest_type": detection.pest_type,
                        "confidence": detection.confidence,
                        "severity": detection.severity,
                        "recommended_action": detection.recommended_action,
                        "timestamp": detection.created_at.isoformat()
                    }
                )
                alerts.append(alert)
        
        # Check for multiple detections (potential outbreak)
        if len(recent_detections) >= 3:
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.PEST.value,
                Alert.title.like("%Multiple Pest%"),
                Alert.created_at >= recent_alert_time
            ).first()
            
            if not existing:
                pest_types = list(set([d.pest_type for d in recent_detections]))
                alert = AlertService.create_alert(
                    db=db,
                    user_id=user_id,
                    alert_type=AlertType.PEST,
                    severity=AlertSeverity.CRITICAL,
                    title="Multiple Pest Detections",
                    message=f"Multiple pest detections ({len(recent_detections)}) in the last 24 hours. Pest types: {', '.join(pest_types)}. Consider immediate pest control measures.",
                    source_id=None,
                    source_type="pest_detection_summary",
                    metadata={
                        "detection_count": len(recent_detections),
                        "pest_types": pest_types,
                        "time_period": "24 hours"
                    }
                )
                alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def check_weather_alerts(db: Session, user_id: int, weather_alerts: List[dict]) -> List[Alert]:
        """
        Generate alerts from weather service alerts
        
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
        
        for weather_alert in weather_alerts:
            # Check if we already have a similar alert
            existing = db.query(Alert).filter(
                Alert.user_id == user_id,
                Alert.type == AlertType.WEATHER.value,
                Alert.title == weather_alert.get("title"),
                Alert.created_at >= recent_alert_time
            ).first()
            
            if existing:
                continue
            
            # Map weather severity to alert severity
            severity_map = {
                "info": AlertSeverity.INFO,
                "warning": AlertSeverity.WARNING,
                "critical": AlertSeverity.CRITICAL
            }
            severity = severity_map.get(weather_alert.get("severity", "info"), AlertSeverity.INFO)
            
            alert = AlertService.create_alert(
                db=db,
                user_id=user_id,
                alert_type=AlertType.WEATHER,
                severity=severity,
                title=weather_alert.get("title", "Weather Alert"),
                message=weather_alert.get("message", "Weather conditions require attention."),
                source_id=None,
                source_type="weather_service",
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
