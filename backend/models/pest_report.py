"""
Pest Report Model

This module defines the model for manual pest reports submitted by farmers
when the AI detection fails to identify a pest after multiple attempts.

Learning Notes:
- Reports are created after 3 failed detection attempts
- AI provides best-guess analysis even without positive identification
- Status tracks whether report has been reviewed
- JSONB stores flexible AI response structure
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from database import Base


class ObservedSeverity(str, enum.Enum):
    """Severity levels as observed by the farmer"""
    MINOR = "minor"       # Few pests visible, limited damage
    MODERATE = "moderate" # Noticeable pest presence, some crop damage
    SEVERE = "severe"     # Heavy infestation, significant damage


class ReportStatus(str, enum.Enum):
    """Status of the pest report"""
    PENDING = "pending"   # Report submitted, awaiting review
    REVIEWED = "reviewed" # Report has been reviewed/processed


class PestReport(Base):
    """
    Pest Report Model

    Stores manual pest reports from farmers when AI detection fails.
    Used as fallback mechanism per PRD v2 Section 5.5.

    Table: pest_reports

    Workflow:
    1. User uploads image for pest detection
    2. After 3 failed attempts (confidence < 50%), offer manual report
    3. User submits report with description and observed severity
    4. AI provides best-guess analysis and general advice
    5. Report stored for potential future model improvement
    """

    __tablename__ = "pest_reports"

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Unique report identifier"
    )

    # Foreign Key to User
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="User who submitted the report"
    )

    # Image Information
    image_url = Column(
        String(500),
        nullable=False,
        comment="Path to uploaded image (from failed detection attempts)"
    )

    # User-provided Description (optional)
    description = Column(
        Text,
        nullable=True,
        comment="User's description of what they observed"
    )

    # Observed Severity (user's assessment)
    observed_severity = Column(
        String(20),
        nullable=False,
        default=ObservedSeverity.MODERATE.value,
        comment="Severity as observed by farmer: minor, moderate, severe"
    )

    # AI Response (JSONB for flexible structure)
    # Example: {
    #   "possible_identification": "Based on description, this could be...",
    #   "general_advice": ["Monitor daily", "Apply neem spray", ...],
    #   "when_to_seek_help": "If infestation spreads to more than 20%..."
    # }
    ai_response = Column(
        JSONB,
        nullable=True,
        comment="AI-generated best-guess analysis and advice"
    )

    # Report Status
    status = Column(
        String(20),
        nullable=False,
        default=ReportStatus.PENDING.value,
        comment="Report status: pending, reviewed"
    )

    # Timestamps
    reported_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="When the report was submitted"
    )

    # Relationships
    user = relationship("User", back_populates="pest_reports")

    # Indexes for common queries
    __table_args__ = (
        Index('idx_pest_reports_user_status', 'user_id', 'status'),
        Index('idx_pest_reports_reported_at', 'reported_at'),
        {'comment': 'Manual pest reports for unidentified pests'}
    )

    def __repr__(self):
        """String representation for debugging"""
        return f"<PestReport(id={self.id}, user_id={self.user_id}, severity='{self.observed_severity}', status='{self.status}')>"

    def to_dict(self):
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_url": self.image_url,
            "description": self.description,
            "observed_severity": self.observed_severity,
            "ai_response": self.ai_response,
            "status": self.status,
            "reported_at": self.reported_at.isoformat() if self.reported_at else None
        }


# ============================================================================
# LEARNING NOTES: Manual Pest Reports
# ============================================================================

"""
1. Why Manual Reports?
   - AI pest detection isn't perfect (especially for rare pests)
   - Farmers need help even when AI can't identify the pest
   - Reports can improve future model training
   - Provides fallback mechanism for frustrated users

2. When Reports Are Triggered:
   - After 3 failed detection attempts (confidence < 50%)
   - User chooses to submit manual report
   - Can still upload new images or retry detection

3. AI Response Structure:
   ai_response = {
       "possible_identification": "Based on description...",
       "general_advice": [
           "Monitor the affected area daily",
           "Remove heavily infested leaves",
           "Consider applying neem oil spray",
           "Consult local agricultural extension office"
       ],
       "when_to_seek_help": "If infestation spreads to more than 20%..."
   }

4. Report Status:
   - PENDING: New report, needs attention
   - REVIEWED: Report has been processed/acknowledged

5. Integration with AI Service:
   - When report is submitted, call OpenRouter API
   - Provide context: image description, severity, crop type
   - Request best-guess identification and general advice
   - Store response in ai_response JSONB field

6. Future Improvements:
   - Reports could be used to retrain ML model
   - Admin could manually identify pests in pending reports
   - Community-based identification feature
"""
