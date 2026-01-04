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
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import datetime, timedelta

from backend.database import get_db
from backend.models.sensor_data import SensorData
from backend.models.user import User
from backend.schemas.sensor import (
    SensorDataCreate,
    SensorDataResponse,
    SensorDataUpdate
)
from backend.dependencies.auth import get_current_user

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
            "humidity": 75.0,
            "rainfall": 12.5,
            "soil_moisture": 65.0,
            "wind_speed": 15.0
        }
    """
    # Create new sensor data record
    db_sensor_data = SensorData(
        user_id=current_user.id,
        temperature=sensor_data.temperature,
        humidity=sensor_data.humidity,
        rainfall=sensor_data.rainfall,
        soil_moisture=sensor_data.soil_moisture,
        wind_speed=sensor_data.wind_speed,
        recorded_at=datetime.utcnow()
    )
    
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
    query = db.query(SensorData).filter(SensorData.user_id == current_user.id)
    
    # Apply date filters
    if start_date:
        query = query.filter(SensorData.recorded_at >= start_date)
    if end_date:
        query = query.filter(SensorData.recorded_at <= end_date)
    
    # Apply temperature filters
    if min_temperature is not None:
        query = query.filter(SensorData.temperature >= min_temperature)
    if max_temperature is not None:
        query = query.filter(SensorData.temperature <= max_temperature)
    
    # Order by most recent first
    query = query.order_by(SensorData.recorded_at.desc())
    
    # Apply pagination
    sensor_data = query.offset(skip).limit(limit).all()
    
    return sensor_data


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
    sensor_data = db.query(SensorData).filter(
        and_(
            SensorData.id == sensor_data_id,
            SensorData.user_id == current_user.id
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
    db_sensor_data = db.query(SensorData).filter(
        and_(
            SensorData.id == sensor_data_id,
            SensorData.user_id == current_user.id
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
    db_sensor_data = db.query(SensorData).filter(
        and_(
            SensorData.id == sensor_data_id,
            SensorData.user_id == current_user.id
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
    query = db.query(SensorData).filter(
        and_(
            SensorData.user_id == current_user.id,
            SensorData.recorded_at >= start_date,
            SensorData.recorded_at <= end_date
        )
    )
    
    # Get aggregated statistics
    stats = db.query(
        func.count(SensorData.id).label('count'),
        func.avg(SensorData.temperature).label('avg_temperature'),
        func.min(SensorData.temperature).label('min_temperature'),
        func.max(SensorData.temperature).label('max_temperature'),
        func.avg(SensorData.humidity).label('avg_humidity'),
        func.min(SensorData.humidity).label('min_humidity'),
        func.max(SensorData.humidity).label('max_humidity'),
        func.sum(SensorData.rainfall).label('total_rainfall'),
        func.avg(SensorData.rainfall).label('avg_rainfall'),
        func.max(SensorData.rainfall).label('max_rainfall')
    ).filter(
        and_(
            SensorData.user_id == current_user.id,
            SensorData.recorded_at >= start_date,
            SensorData.recorded_at <= end_date
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
        "humidity": {
            "average": round(stats.avg_humidity, 2) if stats.avg_humidity else None,
            "minimum": round(stats.min_humidity, 2) if stats.min_humidity else None,
            "maximum": round(stats.max_humidity, 2) if stats.max_humidity else None
        },
        "rainfall": {
            "total": round(stats.total_rainfall, 2) if stats.total_rainfall else 0,
            "average": round(stats.avg_rainfall, 2) if stats.avg_rainfall else None,
            "maximum": round(stats.max_rainfall, 2) if stats.max_rainfall else None
        }
    }
