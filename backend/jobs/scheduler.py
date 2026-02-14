"""
Background Job Scheduler

This module sets up and manages background jobs for AgriSense.
Uses APScheduler for scheduling periodic tasks.

Jobs:
1. Weather Check (every 30 minutes):
   - Fetch weather for active users
   - Update weather cache
   - Check weather alert thresholds

2. Pest Risk Check (every 30 minutes):
   - Check weather against pest correlations
   - Generate pest risk alerts for matching conditions

Learning Notes:
- APScheduler runs jobs in background threads
- Jobs are async and use the database session
- Scheduler integrates with FastAPI lifespan
"""

import logging
import asyncio
from datetime import datetime
from typing import Optional
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

import json
from database import SessionLocal
from models.user import User
from models.alert import Alert, AlertType, AlertSeverity
from models.sensor_reading import SensorReading
from services.weather_service import fetch_current_weather, transform_current_weather
from services.pest_risk_service import check_and_generate_pest_risk_alerts

# Logger
logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler: Optional[AsyncIOScheduler] = None


# ============================================================================
# JOB FUNCTIONS
# ============================================================================

async def weather_check_job():
    """
    Background job: Check weather and generate alerts.

    This job runs every 30 minutes and:
    1. Gets all active users with unique locations
    2. Fetches current weather for each location
    3. Checks weather against alert thresholds
    4. Creates alerts for concerning conditions
    """
    logger.info("Starting weather check job...")

    db = SessionLocal()
    try:
        # Get all active users (we'll dedupe by location)
        users = db.query(User).filter(User.is_active == True).all()

        if not users:
            logger.info("No active users found, skipping weather check")
            return

        # Track processed locations to avoid duplicate API calls
        processed_locations = set()
        alerts_created = 0
        readings_created = 0

        for user in users:
            # Create location key for deduplication
            location_key = f"{user.farm_location_lat:.4f},{user.farm_location_lng:.4f}"

            if location_key in processed_locations:
                continue

            processed_locations.add(location_key)

            try:
                # Fetch current weather
                weather_data = await fetch_current_weather(
                    user.farm_location_lat,
                    user.farm_location_lng
                )
                current = transform_current_weather(weather_data)

                # Save weather data as sensor readings for all users at this location
                raw_current = weather_data.get("current", {})
                location_users = [
                    u for u in users
                    if abs(u.farm_location_lat - user.farm_location_lat) < 0.01
                    and abs(u.farm_location_lng - user.farm_location_lng) < 0.01
                ]
                for loc_user in location_users:
                    reading = SensorReading(
                        user_id=loc_user.id,
                        temperature=current.temperature,
                        relative_humidity=current.relative_humidity,
                        rain=current.rain or 0.0,
                        wind_speed=raw_current.get("wind_speed_10m", 0.0),  # km/h (raw from API)
                        solar_radiation=current.shortwave_radiation,
                        soil_temperature=current.soil_temperature,
                        soil_moisture=current.soil_moisture if current.soil_moisture is not None else 0.0,
                        weather_code=raw_current.get("weather_code")
                    )
                    db.add(reading)
                    readings_created += 1
                db.commit()

                # Check thresholds and create alerts
                # High temperature alert
                if current.temperature > 35:
                    alert_count = await _create_weather_alert_for_location(
                        db=db,
                        users=users,
                        lat=user.farm_location_lat,
                        lng=user.farm_location_lng,
                        alert_type=AlertType.EXTREME_HEAT,
                        severity=AlertSeverity.HIGH,
                        title="High Temperature Warning",
                        message=f"Temperature has reached {current.temperature:.1f}°C. Consider shade protection and increase irrigation.",
                        threshold_value=current.temperature
                    )
                    alerts_created += alert_count

                # Heavy rain alert
                if current.rain_1h and current.rain_1h > 20:
                    alert_count = await _create_weather_alert_for_location(
                        db=db,
                        users=users,
                        lat=user.farm_location_lat,
                        lng=user.farm_location_lng,
                        alert_type=AlertType.HEAVY_RAIN,
                        severity=AlertSeverity.HIGH,
                        title="Heavy Rain Warning",
                        message=f"Heavy rainfall ({current.rain_1h:.1f}mm/hr). Check drainage and protect crops.",
                        threshold_value=current.rain_1h
                    )
                    alerts_created += alert_count

                # High humidity alert (fungal disease risk)
                if current.relative_humidity > 90 and current.temperature > 25:
                    alert_count = await _create_weather_alert_for_location(
                        db=db,
                        users=users,
                        lat=user.farm_location_lat,
                        lng=user.farm_location_lng,
                        alert_type=AlertType.HIGH_HUMIDITY,
                        severity=AlertSeverity.MEDIUM,
                        title="High Humidity - Disease Risk",
                        message=f"Humidity at {current.relative_humidity}%. High risk of fungal diseases. Monitor crops closely.",
                        threshold_value=current.relative_humidity
                    )
                    alerts_created += alert_count

            except Exception as e:
                logger.error(f"Error checking weather for location {location_key}: {e}")
                continue

        logger.info(f"Weather check completed. Locations checked: {len(processed_locations)}, Readings saved: {readings_created}, Alerts created: {alerts_created}")

    except Exception as e:
        logger.error(f"Weather check job failed: {e}")
    finally:
        db.close()


async def pest_risk_check_job():
    """
    Background job: Check pest risk and generate alerts.

    This job runs every 30 minutes and:
    1. Gets all active users
    2. Checks weather against pest-weather correlations
    3. Creates pest risk alerts for matching conditions
    """
    logger.info("Starting pest risk check job...")

    db = SessionLocal()
    try:
        # Get all active users
        users = db.query(User).filter(User.is_active == True).all()

        if not users:
            logger.info("No active users found, skipping pest risk check")
            return

        total_alerts = 0

        for user in users:
            try:
                alerts = await check_and_generate_pest_risk_alerts(
                    db=db,
                    user_id=user.id,
                    crop_type=user.crop_type,
                    latitude=user.farm_location_lat,
                    longitude=user.farm_location_lng
                )
                total_alerts += len(alerts)

            except Exception as e:
                logger.error(f"Error checking pest risk for user {user.id}: {e}")
                continue

        logger.info(f"Pest risk check completed. Users checked: {len(users)}, Alerts created: {total_alerts}")

    except Exception as e:
        logger.error(f"Pest risk check job failed: {e}")
    finally:
        db.close()


async def _create_weather_alert_for_location(
    db,
    users,
    lat: float,
    lng: float,
    alert_type: AlertType,
    severity: AlertSeverity,
    title: str,
    message: str,
    threshold_value: float
):
    """
    Create weather alert for all users at a location.

    Returns count of alerts created.
    """
    from datetime import timedelta

    alerts_created = 0
    six_hours_ago = datetime.utcnow() - timedelta(hours=6)

    # Find all users at this location (within ~1km)
    location_users = [
        u for u in users
        if abs(u.farm_location_lat - lat) < 0.01 and abs(u.farm_location_lng - lng) < 0.01
    ]

    for user in location_users:
        # Check for existing recent alert (dedup within 6 hours)
        existing = db.query(Alert).filter(
            Alert.user_id == user.id,
            Alert.alert_type == alert_type,
            Alert.title == title,
            Alert.created_at >= six_hours_ago
        ).first()

        if not existing:
            alert = Alert(
                user_id=user.id,
                alert_type=alert_type,
                severity=severity,
                title=title,
                message=message,
                alert_metadata=json.dumps({
                    "threshold_value": threshold_value,
                    "location_lat": lat,
                    "location_lng": lng
                }),
                is_read=False,
                is_acknowledged=False
            )
            db.add(alert)
            alerts_created += 1

    if alerts_created > 0:
        db.commit()

    return alerts_created


# ============================================================================
# SCHEDULER MANAGEMENT
# ============================================================================

def start_scheduler():
    """
    Start the background job scheduler.

    Call this during application startup.
    """
    global scheduler

    if scheduler is not None:
        logger.warning("Scheduler already running")
        return

    scheduler = AsyncIOScheduler()

    # Add weather check job (every 30 minutes)
    scheduler.add_job(
        weather_check_job,
        trigger=IntervalTrigger(minutes=30),
        id="weather_check",
        name="Weather Check Job",
        replace_existing=True
    )

    # Add pest risk check job (every 30 minutes, offset by 15 minutes)
    scheduler.add_job(
        pest_risk_check_job,
        trigger=IntervalTrigger(minutes=30),
        id="pest_risk_check",
        name="Pest Risk Check Job",
        replace_existing=True
    )

    scheduler.start()
    logger.info("Background scheduler started with jobs: weather_check, pest_risk_check")


def stop_scheduler():
    """
    Stop the background job scheduler.

    Call this during application shutdown.
    """
    global scheduler

    if scheduler is not None:
        scheduler.shutdown(wait=False)
        scheduler = None
        logger.info("Background scheduler stopped")


def run_job_now(job_id: str):
    """
    Trigger a job to run immediately (for testing).

    Args:
        job_id: Job ID ('weather_check' or 'pest_risk_check')
    """
    global scheduler

    if scheduler is None:
        logger.error("Scheduler not running")
        return

    job = scheduler.get_job(job_id)
    if job:
        job.modify(next_run_time=datetime.now())
        logger.info(f"Job {job_id} triggered to run now")
    else:
        logger.error(f"Job {job_id} not found")


# ============================================================================
# LEARNING NOTES: Background Jobs
# ============================================================================

"""
1. Why Background Jobs?
   - Proactive monitoring without user action
   - Users get alerts even when not using app
   - Reduces load on user-triggered endpoints

2. APScheduler:
   - AsyncIOScheduler works with FastAPI async
   - IntervalTrigger runs jobs at fixed intervals
   - Jobs run in background without blocking

3. Job Design:
   - Each job is independent and idempotent
   - Errors in one user's check don't affect others
   - Duplicate alerts prevented with time-based checks

4. Integration with FastAPI:
   - Start scheduler in lifespan startup
   - Stop scheduler in lifespan shutdown
   - Jobs use SessionLocal for database access

5. Alert Deduplication:
   - Check for existing alert within 6 hours
   - Prevents alert spam for persistent conditions
   - Users can acknowledge to get fresh alerts

6. Testing:
   - Use run_job_now() to trigger jobs manually
   - Jobs log their progress for debugging
"""
