"""Add weather_cache table

Revision ID: 4f71b8840e6a
Revises: 3e60a6739d5f
Create Date: 2026-01-09 02:25:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '4f71b8840e6a'
down_revision = '3e60a6739d5f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create weather_cache table.

    This table stores cached weather data from OpenWeatherMap API.
    Cache is shared across users by location (30-minute TTL).
    """
    op.create_table(
        'weather_cache',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, comment='Unique cache entry identifier'),
        sa.Column('location_key', sa.String(50), unique=True, nullable=False, index=True, comment='Unique location key (lat_lng format)'),
        sa.Column('location_name', sa.String(100), nullable=False, comment='Human-readable location name'),
        sa.Column('current_conditions', JSONB(), nullable=False, comment='Current weather data from API'),
        sa.Column('forecast_data', JSONB(), nullable=False, comment='7-day forecast data from API'),
        sa.Column('ml_predictions', JSONB(), nullable=True, comment='Output from weather ML model'),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment='When the weather data was fetched'),
        comment='Cache for weather API data, shared across users by location'
    )

    # Create index for fetched_at queries (cache expiry checks)
    op.create_index('idx_weather_cache_fetched', 'weather_cache', ['fetched_at'])


def downgrade() -> None:
    """
    Drop weather_cache table.
    """
    op.drop_index('idx_weather_cache_fetched', table_name='weather_cache')
    op.drop_table('weather_cache')
