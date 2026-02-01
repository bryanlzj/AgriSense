"""
Sector Router

API endpoints for managing farm sectors.

Endpoints:
- POST /sector/ - Create a new sector
- GET /sector/ - List all sectors for the current user
- GET /sector/{sector_id} - Get a specific sector
- PUT /sector/{sector_id} - Update a sector
- DELETE /sector/{sector_id} - Delete a sector
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.user import User
from models.sector import Sector
from schemas.sector import (
    SectorCreate,
    SectorUpdate,
    SectorResponse,
    SectorListResponse,
)
from dependencies.auth import get_current_user

router = APIRouter(prefix="/sector", tags=["Sector"])


@router.post(
    "/",
    response_model=SectorResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sector"
)
async def create_sector(
    sector_data: SectorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new farm sector.

    - **name**: Sector name (required)
    - **location**: Location description within the farm
    - **area**: Area size as string (e.g., '2 acres')
    - **crop**: Crop type planted
    - **planted_date**: Date when crop was planted
    """
    # Create new sector
    sector = Sector(
        user_id=current_user.id,
        name=sector_data.name,
        location=sector_data.location,
        area=sector_data.area,
        area_value=sector_data.area_value,
        area_unit=sector_data.area_unit,
        crop=sector_data.crop,
        planted_date=sector_data.planted_date,
    )

    db.add(sector)
    db.commit()
    db.refresh(sector)

    return sector


@router.get(
    "/",
    response_model=List[SectorResponse],
    summary="List all sectors"
)
async def list_sectors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Maximum number of records to return"),
    crop: Optional[str] = Query(None, description="Filter by crop type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    List all sectors for the current user.

    Supports pagination and filtering by crop type.
    """
    query = db.query(Sector).filter(Sector.user_id == current_user.id)

    # Apply filters
    if crop:
        query = query.filter(Sector.crop.ilike(f"%{crop}%"))

    # Order by created_at descending (newest first)
    query = query.order_by(Sector.created_at.desc())

    # Apply pagination
    sectors = query.offset(skip).limit(limit).all()

    return sectors


@router.get(
    "/{sector_id}",
    response_model=SectorResponse,
    summary="Get a specific sector"
)
async def get_sector(
    sector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific sector by ID.

    Returns 404 if sector not found or doesn't belong to current user.
    """
    sector = db.query(Sector).filter(
        Sector.id == sector_id,
        Sector.user_id == current_user.id
    ).first()

    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector not found"
        )

    return sector


@router.put(
    "/{sector_id}",
    response_model=SectorResponse,
    summary="Update a sector"
)
async def update_sector(
    sector_id: int,
    sector_data: SectorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a sector.

    Only the fields provided will be updated.
    """
    sector = db.query(Sector).filter(
        Sector.id == sector_id,
        Sector.user_id == current_user.id
    ).first()

    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector not found"
        )

    # Update only provided fields
    update_data = sector_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sector, field, value)

    db.commit()
    db.refresh(sector)

    return sector


@router.delete(
    "/{sector_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a sector"
)
async def delete_sector(
    sector_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a sector.

    Returns 204 No Content on success.
    Returns 404 if sector not found or doesn't belong to current user.
    """
    sector = db.query(Sector).filter(
        Sector.id == sector_id,
        Sector.user_id == current_user.id
    ).first()

    if not sector:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sector not found"
        )

    db.delete(sector)
    db.commit()

    return None


@router.get(
    "/stats/summary",
    summary="Get sector statistics"
)
async def get_sector_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get summary statistics for user's sectors.

    Returns:
    - Total sector count
    - Crops breakdown
    - Total area (if available)
    """
    from sqlalchemy import func

    # Total sectors
    total_sectors = db.query(func.count(Sector.id)).filter(
        Sector.user_id == current_user.id
    ).scalar()

    # Get all sectors for crop breakdown
    sectors = db.query(Sector).filter(Sector.user_id == current_user.id).all()

    # Crop breakdown
    crop_counts = {}
    for sector in sectors:
        if sector.crop:
            crop_counts[sector.crop] = crop_counts.get(sector.crop, 0) + 1

    return {
        "total_sectors": total_sectors,
        "crops": crop_counts,
        "sector_names": [s.name for s in sectors]
    }
