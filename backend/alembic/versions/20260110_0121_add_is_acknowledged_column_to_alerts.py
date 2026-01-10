"""Add is_acknowledged column to alerts

Revision ID: 05337b94f4df
Revises: 5a82c9951f7b
Create Date: 2026-01-10 01:21:10.285810

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '05337b94f4df'
down_revision = '5a82c9951f7b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add is_acknowledged column to alerts table."""
    # Add the is_acknowledged column with default value False
    op.add_column('alerts', sa.Column(
        'is_acknowledged',
        sa.Boolean(),
        nullable=False,
        server_default='false',
        comment='Whether user has acknowledged this alert'
    ))

    # Create index for the new column
    op.create_index(
        op.f('ix_alerts_is_acknowledged'),
        'alerts',
        ['is_acknowledged'],
        unique=False
    )


def downgrade() -> None:
    """Remove is_acknowledged column from alerts table."""
    op.drop_index(op.f('ix_alerts_is_acknowledged'), table_name='alerts')
    op.drop_column('alerts', 'is_acknowledged')
