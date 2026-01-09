"""Add pest_reports table

Revision ID: 5a82c9951f7b
Revises: 4f71b8840e6a
Create Date: 2026-01-09 03:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '5a82c9951f7b'
down_revision = '4f71b8840e6a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create pest_reports table.

    This table stores manual pest reports from farmers when AI detection fails.
    Used as fallback mechanism per PRD v2 Section 5.5.

    Columns:
    - id: Primary key
    - user_id: Foreign key to users table
    - image_url: Path to uploaded image
    - description: User's description of the pest
    - observed_severity: Farmer's assessment (minor, moderate, severe)
    - ai_response: JSONB storing AI-generated analysis
    - status: Report status (pending, reviewed)
    - reported_at: Timestamp when report was submitted
    """
    op.create_table(
        'pest_reports',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, comment='Unique report identifier'),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True, comment='User who submitted the report'),
        sa.Column('image_url', sa.String(500), nullable=False, comment='Path to uploaded image'),
        sa.Column('description', sa.Text(), nullable=True, comment='User description of what they observed'),
        sa.Column('observed_severity', sa.String(20), nullable=False, server_default='moderate', comment='Severity as observed by farmer: minor, moderate, severe'),
        sa.Column('ai_response', JSONB(), nullable=True, comment='AI-generated best-guess analysis and advice'),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending', comment='Report status: pending, reviewed'),
        sa.Column('reported_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment='When the report was submitted'),
        comment='Manual pest reports for unidentified pests'
    )

    # Create composite index for user_id + status queries
    op.create_index('idx_pest_reports_user_status', 'pest_reports', ['user_id', 'status'])

    # Create index for reported_at queries (for sorting/pagination)
    op.create_index('idx_pest_reports_reported_at', 'pest_reports', ['reported_at'])


def downgrade() -> None:
    """
    Drop pest_reports table.
    """
    op.drop_index('idx_pest_reports_reported_at', table_name='pest_reports')
    op.drop_index('idx_pest_reports_user_status', table_name='pest_reports')
    op.drop_table('pest_reports')
