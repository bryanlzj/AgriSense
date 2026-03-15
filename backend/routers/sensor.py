"""
API endpoints for sensor data management.

This module provides endpoints for:
- Creating new sensor readings
- Retrieving sensor data (with filtering)
- Updating sensor readings
- Deleting sensor readings
- Getting sensor statistics

All endpoints require authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import datetime, timedelta
import csv
import io

from database import get_db
from models.sensor_reading import SensorReading
from models.user import User
from services.weather_ml_service import weather_ml_service
from schemas.sensor import (
    SensorDataCreate,
    SensorDataResponse,
    SensorDataUpdate
)
from dependencies.auth import get_current_user

router = APIRouter(prefix="/sensor", tags=["Sensor Data"])


@router.post("/", response_model=SensorDataResponse, status_code=201)
def create_sensor_data(
    sensor_data: SensorDataCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a new sensor data reading.

    This endpoint allows authenticated users to submit new sensor readings.
    The reading is automatically associated with the current user.
    Fields aligned with Open-Meteo API parameters.

    Args:
        sensor_data: The sensor data to create
        current_user: The authenticated user (from JWT token)
        db: Database session

    Returns:
        The created sensor data with ID and timestamps

    Example:
        POST /api/v1/sensor/
        {
            "temperature": 28.5,
            "relative_humidity": 75.0,
            "rain": 0.0,
            "wind_speed": 12.5,
            "solar_radiation": 650.0,
            "soil_temperature": 26.0,
            "soil_moisture": 0.35,
            "weather_code": 1
        }
    """
    # Create new sensor data record
    db_sensor_data = SensorReading(
        user_id=current_user.id,
        temperature=sensor_data.temperature,
        relative_humidity=sensor_data.relative_humidity,
        rain=sensor_data.rain,
        wind_speed=sensor_data.wind_speed,
        solar_radiation=sensor_data.solar_radiation,
        soil_temperature=sensor_data.soil_temperature,
        soil_moisture=sensor_data.soil_moisture,
        weather_code=sensor_data.weather_code
    )

    # Auto-classify weather condition using ML model
    try:
        prediction = weather_ml_service.predict({
            "temperature": db_sensor_data.temperature,
            "relative_humidity": db_sensor_data.relative_humidity,
            "rain": db_sensor_data.rain,
            "wind_speed": db_sensor_data.wind_speed,
            "soil_temperature": db_sensor_data.soil_temperature,
            "soil_moisture": db_sensor_data.soil_moisture,
            "solar_radiation": db_sensor_data.solar_radiation,
        })
        db_sensor_data.weather_condition = prediction.condition
    except Exception:
        pass  # Classification failure shouldn't block reading creation

    db.add(db_sensor_data)
    db.commit()
    db.refresh(db_sensor_data)
    
    return db_sensor_data


@router.get("/", response_model=List[SensorDataResponse])
def get_sensor_data(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date"),
    min_temperature: Optional[float] = Query(None, description="Minimum temperature filter"),
    max_temperature: Optional[float] = Query(None, description="Maximum temperature filter"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get sensor data for the current user with optional filtering.
    
    This endpoint retrieves sensor data with support for:
    - Pagination (skip/limit)
    - Date range filtering
    - Temperature range filtering
    
    Args:
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return
        start_date: Filter records after this date
        end_date: Filter records before this date
        min_temperature: Filter records with temperature >= this value
        max_temperature: Filter records with temperature <= this value
        current_user: The authenticated user
        db: Database session
        
    Returns:
        List of sensor data records matching the filters
        
    Example:
        GET /api/v1/sensor/?start_date=2024-01-01&limit=50
    """
    # Build query with filters
    query = db.query(SensorReading).filter(SensorReading.user_id == current_user.id)
    
    # Apply date filters
    if start_date:
        query = query.filter(SensorReading.timestamp >= start_date)
    if end_date:
        query = query.filter(SensorReading.timestamp <= end_date)
    
    # Apply temperature filters
    if min_temperature is not None:
        query = query.filter(SensorReading.temperature >= min_temperature)
    if max_temperature is not None:
        query = query.filter(SensorReading.temperature <= max_temperature)
    
    # Order by most recent first
    query = query.order_by(SensorReading.timestamp.desc())
    
    # Apply pagination
    sensor_data = query.offset(skip).limit(limit).all()
    
    return sensor_data


@router.post("/import", status_code=200)
async def import_sensor_data(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Import sensor data from a CSV file.

    Accepted columns: temperature, relative_humidity (alias: humidity),
    soil_moisture, rain (alias: rainfall), wind_speed, solar_radiation,
    soil_temperature, weather_code, timestamp.

    Required per row: temperature, relative_humidity, soil_moisture.
    Missing optional columns default to 0.0 or NULL.
    Max 10,000 rows per import.
    """
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = await file.read()
    # Handle UTF-8 BOM
    text = content.decode('utf-8-sig')

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV file is empty or has no headers")

    # Column aliases
    aliases = {
        'humidity': 'relative_humidity',
        'rainfall': 'rain',
    }

    # Normalize headers
    normalized_fields = []
    for f in reader.fieldnames:
        clean = f.strip().lower()
        normalized_fields.append(aliases.get(clean, clean))

    expected_columns = [
        'temperature', 'relative_humidity', 'soil_moisture',
        'rain', 'wind_speed', 'solar_radiation',
        'soil_temperature', 'weather_code', 'timestamp'
    ]
    required_columns = ['temperature', 'relative_humidity', 'soil_moisture']

    columns_matched = [c for c in expected_columns if c in normalized_fields]
    columns_missing = [c for c in expected_columns if c not in normalized_fields]

    rows_imported = 0
    rows_skipped = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):
        if rows_imported + rows_skipped >= 10000:
            errors.append({"row": row_num, "message": "Row limit (10,000) reached"})
            break

        # Normalize row keys
        normalized_row = {}
        for key, value in row.items():
            clean_key = key.strip().lower()
            normalized_row[aliases.get(clean_key, clean_key)] = value.strip() if value else None

        # Check required fields
        missing_required = []
        for req in required_columns:
            if req not in normalized_row or not normalized_row[req]:
                missing_required.append(req)

        if missing_required:
            rows_skipped += 1
            errors.append({"row": row_num, "message": f"Missing required fields: {', '.join(missing_required)}"})
            continue

        try:
            # Parse timestamp
            ts = None
            if 'timestamp' in normalized_row and normalized_row['timestamp']:
                ts_str = normalized_row['timestamp']
                for fmt in ['%Y-%m-%dT%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S', '%d/%m/%Y']:
                    try:
                        ts = datetime.strptime(ts_str, fmt)
                        break
                    except ValueError:
                        continue
                if ts is None:
                    rows_skipped += 1
                    errors.append({"row": row_num, "message": f"Invalid timestamp format: {ts_str}"})
                    continue

            def safe_float(val, default=None):
                if val is None or val == '':
                    return default
                return float(val)

            def safe_int(val, default=None):
                if val is None or val == '':
                    return default
                return int(float(val))

            reading = SensorReading(
                user_id=current_user.id,
                temperature=safe_float(normalized_row.get('temperature')),
                relative_humidity=safe_float(normalized_row.get('relative_humidity')),
                soil_moisture=safe_float(normalized_row.get('soil_moisture')),
                rain=safe_float(normalized_row.get('rain'), 0.0),
                wind_speed=safe_float(normalized_row.get('wind_speed'), 0.0),
                solar_radiation=safe_float(normalized_row.get('solar_radiation')),
                soil_temperature=safe_float(normalized_row.get('soil_temperature')),
                weather_code=safe_int(normalized_row.get('weather_code')),
            )
            if ts:
                reading.timestamp = ts

            db.add(reading)
            rows_imported += 1
        except (ValueError, TypeError) as e:
            rows_skipped += 1
            errors.append({"row": row_num, "message": str(e)})

    db.commit()

    return {
        "rows_imported": rows_imported,
        "rows_skipped": rows_skipped,
        "columns_matched": columns_matched,
        "columns_missing": columns_missing,
        "errors": errors[:50],
    }


@router.get("/{sensor_data_id}", response_model=SensorDataResponse)
def get_sensor_data_by_id(
    sensor_data_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get a specific sensor data record by ID.
    
    Args:
        sensor_data_id: The ID of the sensor data record
        current_user: The authenticated user
        db: Database session
        
    Returns:
        The sensor data record
        
    Raises:
        404: If the sensor data record is not found or doesn't belong to the user
    """
    sensor_data = db.query(SensorReading).filter(
        and_(
            SensorReading.id == sensor_data_id,
            SensorReading.user_id == current_user.id
        )
    ).first()
    
    if not sensor_data:
        raise HTTPException(
            status_code=404,
            detail="Sensor data not found"
        )
    
    return sensor_data


@router.put("/{sensor_data_id}", response_model=SensorDataResponse)
def update_sensor_data(
    sensor_data_id: int,
    sensor_data_update: SensorDataUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update a sensor data record.
    
    Only the fields provided in the request will be updated.
    Users can only update their own sensor data.
    
    Args:
        sensor_data_id: The ID of the sensor data record to update
        sensor_data_update: The fields to update
        current_user: The authenticated user
        db: Database session
        
    Returns:
        The updated sensor data record
        
    Raises:
        404: If the sensor data record is not found or doesn't belong to the user
    """
    # Find the sensor data record
    db_sensor_data = db.query(SensorReading).filter(
        and_(
            SensorReading.id == sensor_data_id,
            SensorReading.user_id == current_user.id
        )
    ).first()
    
    if not db_sensor_data:
        raise HTTPException(
            status_code=404,
            detail="Sensor data not found"
        )
    
    # Update only provided fields
    update_data = sensor_data_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sensor_data, field, value)
    
    db.commit()
    db.refresh(db_sensor_data)
    
    return db_sensor_data


@router.delete("/{sensor_data_id}", status_code=204)
def delete_sensor_data(
    sensor_data_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a sensor data record.
    
    Users can only delete their own sensor data.
    
    Args:
        sensor_data_id: The ID of the sensor data record to delete
        current_user: The authenticated user
        db: Database session
        
    Returns:
        204 No Content on success
        
    Raises:
        404: If the sensor data record is not found or doesn't belong to the user
    """
    # Find the sensor data record
    db_sensor_data = db.query(SensorReading).filter(
        and_(
            SensorReading.id == sensor_data_id,
            SensorReading.user_id == current_user.id
        )
    ).first()
    
    if not db_sensor_data:
        raise HTTPException(
            status_code=404,
            detail="Sensor data not found"
        )
    
    db.delete(db_sensor_data)
    db.commit()
    
    return None


@router.get("/stats/summary")
def get_sensor_statistics(
    days: int = Query(7, ge=1, le=365, description="Number of days to include in statistics"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get statistical summary of sensor data.
    
    This endpoint provides aggregated statistics for the user's sensor data
    over a specified time period.
    
    Args:
        days: Number of days to include in the statistics (default: 7)
        current_user: The authenticated user
        db: Database session
        
    Returns:
        Dictionary with statistical summary including:
        - Average, min, max for temperature, humidity, rainfall
        - Total rainfall
        - Record count
        - Date range
        
    Example:
        GET /api/v1/sensor/stats/summary?days=30
    """
    # Calculate date range
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=days)
    
    # Query sensor data within date range
    query = db.query(SensorReading).filter(
        and_(
            SensorReading.user_id == current_user.id,
            SensorReading.timestamp >= start_date,
            SensorReading.timestamp <= end_date
        )
    )
    
    # Get aggregated statistics (aligned with Open-Meteo fields)
    stats = db.query(
        func.count(SensorReading.id).label('count'),
        func.avg(SensorReading.temperature).label('avg_temperature'),
        func.min(SensorReading.temperature).label('min_temperature'),
        func.max(SensorReading.temperature).label('max_temperature'),
        func.avg(SensorReading.relative_humidity).label('avg_humidity'),
        func.min(SensorReading.relative_humidity).label('min_humidity'),
        func.max(SensorReading.relative_humidity).label('max_humidity'),
        func.avg(SensorReading.rain).label('avg_rain'),
        func.sum(SensorReading.rain).label('total_rain'),
        func.max(SensorReading.rain).label('max_rain'),
        func.avg(SensorReading.wind_speed).label('avg_wind_speed'),
        func.max(SensorReading.wind_speed).label('max_wind_speed'),
        func.avg(SensorReading.solar_radiation).label('avg_solar_radiation'),
        func.max(SensorReading.solar_radiation).label('max_solar_radiation'),
        func.avg(SensorReading.soil_temperature).label('avg_soil_temperature'),
        func.avg(SensorReading.soil_moisture).label('avg_soil_moisture'),
        func.min(SensorReading.soil_moisture).label('min_soil_moisture'),
        func.max(SensorReading.soil_moisture).label('max_soil_moisture')
    ).filter(
        and_(
            SensorReading.user_id == current_user.id,
            SensorReading.timestamp >= start_date,
            SensorReading.timestamp <= end_date
        )
    ).first()

    # Return formatted statistics
    return {
        "period": {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "days": days
        },
        "record_count": stats.count or 0,
        "temperature": {
            "average": round(stats.avg_temperature, 2) if stats.avg_temperature else None,
            "minimum": round(stats.min_temperature, 2) if stats.min_temperature else None,
            "maximum": round(stats.max_temperature, 2) if stats.max_temperature else None
        },
        "relative_humidity": {
            "average": round(stats.avg_humidity, 2) if stats.avg_humidity else None,
            "minimum": round(stats.min_humidity, 2) if stats.min_humidity else None,
            "maximum": round(stats.max_humidity, 2) if stats.max_humidity else None
        },
        "rain": {
            "average": round(stats.avg_rain, 2) if stats.avg_rain else None,
            "total": round(stats.total_rain, 2) if stats.total_rain else 0,
            "maximum": round(stats.max_rain, 2) if stats.max_rain else None
        },
        "wind_speed": {
            "average": round(stats.avg_wind_speed, 2) if stats.avg_wind_speed else None,
            "maximum": round(stats.max_wind_speed, 2) if stats.max_wind_speed else None
        },
        "solar_radiation": {
            "average": round(stats.avg_solar_radiation, 2) if stats.avg_solar_radiation else None,
            "maximum": round(stats.max_solar_radiation, 2) if stats.max_solar_radiation else None
        },
        "soil_temperature": {
            "average": round(stats.avg_soil_temperature, 2) if stats.avg_soil_temperature else None
        },
        "soil_moisture": {
            "average": round(stats.avg_soil_moisture, 4) if stats.avg_soil_moisture else None,
            "minimum": round(stats.min_soil_moisture, 4) if stats.min_soil_moisture else None,
            "maximum": round(stats.max_soil_moisture, 4) if stats.max_soil_moisture else None
        }
    }
