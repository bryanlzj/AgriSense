"""update_sensor_reading_for_open_meteo

Revision ID: 0ca24217266c
Revises: 05337b94f4df
Create Date: 2026-01-15 12:46:02.194689

This migration updates the sensor_readings table to align with Open-Meteo API parameters:
- Renames 'humidity' to 'relative_humidity'
- Removes 'light_intensity'
- Adds: rain, wind_speed, solar_radiation, soil_temperature, weather_code
- Converts soil_moisture from percentage (0-100) to volumetric (0-1 m³/m³)
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ca24217266c'
down_revision = '05337b94f4df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Apply the migration (upgrade database schema).

    Steps:
    1. Add new columns with defaults for existing data
    2. Copy humidity data to relative_humidity
    3. Convert soil_moisture from % to m³/m³
    4. Drop old columns
    5. Make NOT NULL columns actually NOT NULL
    """
    # Step 1: Add new columns (nullable first to handle existing data)
    op.add_column('sensor_readings', sa.Column('relative_humidity', sa.Float(), nullable=True))
    op.add_column('sensor_readings', sa.Column('rain', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('sensor_readings', sa.Column('wind_speed', sa.Float(), nullable=True, server_default='0.0'))
    op.add_column('sensor_readings', sa.Column('solar_radiation', sa.Float(), nullable=True))
    op.add_column('sensor_readings', sa.Column('soil_temperature', sa.Float(), nullable=True))
    op.add_column('sensor_readings', sa.Column('weather_code', sa.Integer(), nullable=True))

    # Step 2: Copy existing humidity data to relative_humidity
    op.execute("UPDATE sensor_readings SET relative_humidity = humidity WHERE humidity IS NOT NULL")

    # Step 3: Convert soil_moisture from percentage (0-100) to volumetric (0-1 m³/m³)
    # Only if existing values are > 1 (indicating percentage format)
    op.execute("UPDATE sensor_readings SET soil_moisture = soil_moisture / 100.0 WHERE soil_moisture > 1")

    # Step 4: Set default values for new NOT NULL columns where data is missing
    op.execute("UPDATE sensor_readings SET relative_humidity = 65.0 WHERE relative_humidity IS NULL")
    op.execute("UPDATE sensor_readings SET rain = 0.0 WHERE rain IS NULL")
    op.execute("UPDATE sensor_readings SET wind_speed = 10.0 WHERE wind_speed IS NULL")

    # Step 5: Make NOT NULL columns actually NOT NULL
    op.alter_column('sensor_readings', 'relative_humidity', nullable=False)
    op.alter_column('sensor_readings', 'rain', nullable=False)
    op.alter_column('sensor_readings', 'wind_speed', nullable=False)

    # Step 6: Drop old columns
    op.drop_column('sensor_readings', 'light_intensity')
    op.drop_column('sensor_readings', 'humidity')

    # Remove server defaults (they were only for migration)
    op.alter_column('sensor_readings', 'rain', server_default=None)
    op.alter_column('sensor_readings', 'wind_speed', server_default=None)


def downgrade() -> None:
    """
    Revert the migration (downgrade database schema).

    This restores the original schema with humidity and light_intensity.
    Note: Data conversion is lossy - soil_moisture is converted back to percentage.
    """
    # Step 1: Add back old columns
    op.add_column('sensor_readings', sa.Column('humidity', sa.DOUBLE_PRECISION(precision=53), nullable=True))
    op.add_column('sensor_readings', sa.Column('light_intensity', sa.DOUBLE_PRECISION(precision=53), nullable=True, server_default='500.0'))

    # Step 2: Copy relative_humidity back to humidity
    op.execute("UPDATE sensor_readings SET humidity = relative_humidity")

    # Step 3: Convert soil_moisture back from volumetric (0-1) to percentage (0-100)
    op.execute("UPDATE sensor_readings SET soil_moisture = soil_moisture * 100.0 WHERE soil_moisture <= 1")

    # Step 4: Set defaults for NULL values
    op.execute("UPDATE sensor_readings SET light_intensity = 500.0 WHERE light_intensity IS NULL")

    # Step 5: Make columns NOT NULL
    op.alter_column('sensor_readings', 'humidity', nullable=False)
    op.alter_column('sensor_readings', 'light_intensity', nullable=False)

    # Step 6: Drop new columns
    op.drop_column('sensor_readings', 'weather_code')
    op.drop_column('sensor_readings', 'soil_temperature')
    op.drop_column('sensor_readings', 'solar_radiation')
    op.drop_column('sensor_readings', 'wind_speed')
    op.drop_column('sensor_readings', 'rain')
    op.drop_column('sensor_readings', 'relative_humidity')

    # Remove server default
    op.alter_column('sensor_readings', 'light_intensity', server_default=None)
