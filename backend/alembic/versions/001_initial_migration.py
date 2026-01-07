"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2026-01-08 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )
    op.create_index('idx_username_active', 'users', ['username', 'is_active'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Create sensor_readings table
    op.create_table('sensor_readings',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('temperature', sa.Float(), nullable=False),
        sa.Column('humidity', sa.Float(), nullable=False),
        sa.Column('soil_moisture', sa.Float(), nullable=False),
        sa.Column('light_intensity', sa.Float(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_timestamp_desc', 'sensor_readings', ['timestamp'], unique=False)
    op.create_index('idx_user_timestamp', 'sensor_readings', ['user_id', 'timestamp'], unique=False)
    op.create_index(op.f('ix_sensor_readings_id'), 'sensor_readings', ['id'], unique=False)
    op.create_index(op.f('ix_sensor_readings_timestamp'), 'sensor_readings', ['timestamp'], unique=False)

    # Create pest_detections table
    op.create_table('pest_detections',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('image_url', sa.String(length=500), nullable=False),
        sa.Column('pest_type', sa.String(length=100), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('severity_level', sa.String(length=20), nullable=True),
        sa.Column('detections_json', sa.JSON(), nullable=True),
        sa.Column('recommendations', sa.Text(), nullable=True),
        sa.Column('detected_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_pest_user_detected', 'pest_detections', ['user_id', 'detected_at'], unique=False)
    op.create_index('idx_severity', 'pest_detections', ['severity'], unique=False)
    op.create_index(op.f('ix_pest_detections_detected_at'), 'pest_detections', ['detected_at'], unique=False)
    op.create_index(op.f('ix_pest_detections_id'), 'pest_detections', ['id'], unique=False)

    # Create alerts table
    op.create_table('alerts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('alert_type', sa.String(length=50), nullable=False),
        sa.Column('severity', sa.String(length=20), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('is_read', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('read_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_alert_user_created', 'alerts', ['user_id', 'created_at'], unique=False)
    op.create_index('idx_alert_user_read', 'alerts', ['user_id', 'is_read'], unique=False)
    op.create_index(op.f('ix_alerts_created_at'), 'alerts', ['created_at'], unique=False)
    op.create_index(op.f('ix_alerts_id'), 'alerts', ['id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order (due to foreign key constraints)
    op.drop_index(op.f('ix_alerts_id'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_created_at'), table_name='alerts')
    op.drop_index('idx_alert_user_read', table_name='alerts')
    op.drop_index('idx_alert_user_created', table_name='alerts')
    op.drop_table('alerts')
    
    op.drop_index(op.f('ix_pest_detections_id'), table_name='pest_detections')
    op.drop_index(op.f('ix_pest_detections_detected_at'), table_name='pest_detections')
    op.drop_index('idx_severity', table_name='pest_detections')
    op.drop_index('idx_pest_user_detected', table_name='pest_detections')
    op.drop_table('pest_detections')
    
    op.drop_index(op.f('ix_sensor_readings_timestamp'), table_name='sensor_readings')
    op.drop_index(op.f('ix_sensor_readings_id'), table_name='sensor_readings')
    op.drop_index('idx_user_timestamp', table_name='sensor_readings')
    op.drop_index('idx_timestamp_desc', table_name='sensor_readings')
    op.drop_table('sensor_readings')
    
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index('idx_username_active', table_name='users')
    op.drop_table('users')
