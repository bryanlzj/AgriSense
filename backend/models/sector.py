"""
Sector Model

This module defines the Sector database model for farm management.

A Sector represents a distinct area/plot within a user's farm,
allowing for more granular management of crops and monitoring.
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Sector(Base):
    """
    Sector Model

    Represents a farm sector/plot in the AgriSense system.
    Each user can have multiple sectors with different crops.

    Table: sectors
    """

    __tablename__ = "sectors"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique sector identifier"
    )

    # Foreign Key to User
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="Owner of this sector"
    )

    # Sector Details
    name = Column(
        String(100),
        nullable=False,
        comment="Sector name (e.g., 'Sector 1', 'North Field')"
    )

    location = Column(
        String(200),
        nullable=True,
        comment="Location description within the farm"
    )

    area = Column(
        String(50),
        nullable=True,
        comment="Area size (e.g., '2 acres', '1.5 hectares')"
    )

    area_value = Column(
        Float,
        nullable=True,
        comment="Numeric area value for calculations"
    )

    area_unit = Column(
        String(20),
        nullable=True,
        default="acres",
        comment="Area unit (acres, hectares, sq meters)"
    )

    crop = Column(
        String(100),
        nullable=True,
        comment="Crop type planted in this sector"
    )

    planted_date = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Date when crop was planted"
    )

    # Timestamps
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="When the sector was created"
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last time sector data was updated"
    )

    # Relationships
    user = relationship("User", back_populates="sectors")

    # Indexes for performance
    __table_args__ = (
        Index('idx_sector_user_name', 'user_id', 'name'),
        {'comment': 'Farm sectors for crop management'}
    )

    def __repr__(self):
        """String representation for debugging"""
        return f"<Sector(id={self.id}, name='{self.name}', crop='{self.crop}')>"

    def to_dict(self):
        """Convert sector object to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "name": self.name,
            "location": self.location,
            "area": self.area,
            "area_value": self.area_value,
            "area_unit": self.area_unit,
            "crop": self.crop,
            "planted_date": self.planted_date.isoformat() if self.planted_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
