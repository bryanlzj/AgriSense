"""Add pest_weather_correlations table

Revision ID: 3e60a6739d5f
Revises: 397a1101836e
Create Date: 2026-01-09 02:20:34.890305

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '3e60a6739d5f'
down_revision = '397a1101836e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Create pest_weather_correlations table.

    This table stores reference data for pest-weather correlations
    used in the pest risk early warning system (PRD v2 Section 5.4).
    """
    op.create_table(
        'pest_weather_correlations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, comment='Unique correlation identifier'),
        sa.Column('pest_name', sa.String(100), nullable=False, index=True, comment='Common name of the pest'),
        sa.Column('scientific_name', sa.String(150), nullable=True, comment='Scientific name of the pest'),
        sa.Column('affected_crops', JSONB(), nullable=False, comment='Array of crop types affected by this pest'),
        sa.Column('risk_conditions', JSONB(), nullable=False, comment='Weather conditions that increase risk'),
        sa.Column('risk_level', sa.String(20), nullable=False, comment='Risk severity: low, medium, high'),
        sa.Column('risk_message', sa.Text(), nullable=False, comment='Descriptive message explaining the risk'),
        sa.Column('prevention_tips', JSONB(), nullable=False, comment='Array of prevention/treatment recommendations'),
        sa.Column('data_source', sa.String(200), nullable=True, comment='Source of correlation data'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False, comment='When this correlation was added'),
        comment='Reference data for pest-weather correlations used in risk prediction'
    )

    # Create index for risk_level queries
    op.create_index('idx_correlations_risk_level', 'pest_weather_correlations', ['risk_level'])


def downgrade() -> None:
    """
    Drop pest_weather_correlations table.
    """
    op.drop_index('idx_correlations_risk_level', table_name='pest_weather_correlations')
    op.drop_table('pest_weather_correlations')
