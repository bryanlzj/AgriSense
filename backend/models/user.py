"""
User Model

This module defines the User database model for authentication.

Learning Notes:
- SQLAlchemy ORM maps Python classes to database tables
- Each class attribute becomes a database column
- Relationships define connections between tables
- Indexes improve query performance on frequently searched columns
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Index, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

from database import Base


# Valid crop types for validation
VALID_CROP_TYPES = ["rice", "vegetables", "corn", "oil_palm", "rubber"]


class User(Base):
    """
    User Model
    
    Represents a farmer/user in the AgriSense system.
    Simplified for learning - just username and password.
    
    Table: users
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Unique user identifier"
    )
    
    # Authentication Fields
    username = Column(
        String(50), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="Unique username for login"
    )
    
    hashed_password = Column(
        String(255),
        nullable=False,
        comment="Bcrypt hashed password (never store plain passwords!)"
    )

    # Profile Fields (PRD v2)
    full_name = Column(
        String(100),
        nullable=True,
        comment="User's full name"
    )

    # Farm Location Fields
    farm_location_name = Column(
        String(100),
        nullable=False,
        default="Kuala Lumpur",
        comment="Farm location name (e.g., state/region)"
    )

    farm_location_lat = Column(
        Float,
        nullable=False,
        default=3.1390,
        comment="Farm latitude coordinate"
    )

    farm_location_lng = Column(
        Float,
        nullable=False,
        default=101.6869,
        comment="Farm longitude coordinate"
    )

    # Crop Type
    crop_type = Column(
        String(50),
        nullable=False,
        default="rice",
        comment="Primary crop type (rice, vegetables, corn, oil_palm, rubber)"
    )

    # Account Status
    is_active = Column(
        Boolean, 
        default=True, 
        nullable=False,
        comment="Whether the account is active (for soft deletes)"
    )
    
    # Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        comment="When the user registered"
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last time user data was updated"
    )
    
    # Relationships (will be used by other models)
    # These create connections to other tables
    
    # One user can have many sensor readings
    sensor_readings = relationship(
        "SensorReading",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # One user can have many pest detections
    pest_detections = relationship(
        "PestDetection",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )
    
    # One user can have many alerts
    alerts = relationship(
        "Alert",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # One user can have many pest reports (manual reports for unidentified pests)
    pest_reports = relationship(
        "PestReport",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # One user can have many farm sectors
    sectors = relationship(
        "Sector",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    # Indexes for performance
    # Composite index for common query patterns
    __table_args__ = (
        Index('idx_username_active', 'username', 'is_active'),
        {'comment': 'Users table for authentication and user management'}
    )
    
    def __repr__(self):
        """String representation for debugging"""
        return f"<User(id={self.id}, username='{self.username}', active={self.is_active})>"
    
    def to_dict(self):
        """
        Convert user object to dictionary (for API responses)

        Note: Never include hashed_password in API responses!
        """
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "farm_location_name": self.farm_location_name,
            "farm_location_lat": self.farm_location_lat,
            "farm_location_lng": self.farm_location_lng,
            "crop_type": self.crop_type,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


# ============================================================================
# LEARNING NOTES: Understanding SQLAlchemy Models
# ============================================================================

"""
1. What is an ORM?
   - ORM = Object-Relational Mapping
   - Maps Python classes → Database tables
   - Maps Python objects → Database rows
   - You work with Python objects, SQLAlchemy handles SQL

2. Column Types:
   - Integer: Whole numbers (user IDs, counts)
   - String(length): Text with max length
   - Boolean: True/False values
   - DateTime: Date and time stamps

3. Column Options:
   - primary_key=True: Unique identifier for each row
   - unique=True: No two rows can have same value
   - nullable=False: Must have a value (NOT NULL in SQL)
   - index=True: Create database index for faster searches
   - default=value: Default value if not provided

4. Timestamps:
   - server_default=func.now(): Database sets timestamp on insert
   - onupdate=func.now(): Database updates timestamp on update
   - timezone=True: Store timezone-aware timestamps (best practice)

5. Relationships:
   - Define connections between tables
   - back_populates: Two-way relationship (User ↔ PestDetection)
   - cascade="all, delete-orphan": Delete related records when user deleted
   - lazy="dynamic": Load related data only when accessed (performance)

6. Indexes:
   - Speed up database queries
   - Trade-off: Faster reads, slightly slower writes
   - Create indexes on columns you search/filter frequently
   - Composite indexes: Multiple columns together

7. Why Hash Passwords?
   - NEVER store plain text passwords!
   - Hashing is one-way (can't reverse)
   - Even if database is stolen, passwords are safe
   - We use bcrypt (industry standard)

8. Soft Deletes:
   - is_active field allows "soft delete"
   - Instead of deleting row, set is_active=False
   - Preserves data for auditing/recovery
   - Can "undelete" by setting is_active=True

Example Usage:
    # Create new user
    user = User(username="ahmad", hashed_password="$2b$12$...")
    db.add(user)
    db.commit()
    
    # Query user
    user = db.query(User).filter(User.username == "ahmad").first()
    
    # Update user
    user.is_active = False
    db.commit()
    
    # Get user's pest detections
    detections = user.pest_detections.all()
"""
