"""Add farm profile fields to User model

Revision ID: 397a1101836e
Revises: 001
Create Date: 2026-01-09 02:11:02.155807

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '397a1101836e'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Apply the migration (upgrade database schema).

    Adds farm profile fields to User model per PRD v2:
    - full_name: User's full name (optional)
    - farm_location_name: Malaysian state/region name
    - farm_location_lat: Latitude coordinate
    - farm_location_lng: Longitude coordinate
    - crop_type: Primary crop type (rice, vegetables, corn, oil_palm, rubber)
    """
    # Add new columns to users table with defaults for existing users
    op.add_column('users', sa.Column('full_name', sa.String(length=100), nullable=True, comment="User's full name"))
    op.add_column('users', sa.Column('farm_location_name', sa.String(length=100), nullable=False, server_default='Kuala Lumpur', comment='Farm location name (e.g., state/region)'))
    op.add_column('users', sa.Column('farm_location_lat', sa.Float(), nullable=False, server_default='3.1390', comment='Farm latitude coordinate'))
    op.add_column('users', sa.Column('farm_location_lng', sa.Float(), nullable=False, server_default='101.6869', comment='Farm longitude coordinate'))
    op.add_column('users', sa.Column('crop_type', sa.String(length=50), nullable=False, server_default='rice', comment='Primary crop type (rice, vegetables, corn, oil_palm, rubber)'))


def downgrade() -> None:
    """
    Revert the migration (downgrade database schema).

    Removes the farm profile fields from the User model.
    """
    op.drop_column('users', 'crop_type')
    op.drop_column('users', 'farm_location_lng')
    op.drop_column('users', 'farm_location_lat')
    op.drop_column('users', 'farm_location_name')
    op.drop_column('users', 'full_name')
