"""Drop weather_cache table

Revision ID: a1b2c3d4e5f6
Revises: 0ca24217266c
Create Date: 2026-02-13 00:00:00.000000

The weather_cache table was never actively used by any service.
Weather data is cached in-memory in weather_service.py instead.
Removing dead code to keep the database schema clean.
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '0ca24217266c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Drop the unused weather_cache table."""
    op.drop_index('idx_weather_cache_fetched', table_name='weather_cache')
    op.drop_table('weather_cache')


def downgrade() -> None:
    """Recreate weather_cache table if needed."""
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
    op.create_index('idx_weather_cache_fetched', 'weather_cache', ['fetched_at'])
