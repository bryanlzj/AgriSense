"""
Alembic Environment Configuration

This file is run whenever Alembic migrations are executed.
It sets up the database connection and migration context.

LEARNING NOTES:
- env.py is the entry point for Alembic migrations
- It connects Alembic to your SQLAlchemy models
- Supports both online (connected) and offline (SQL script) migrations
"""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import our application's configuration and models
from config import settings, get_database_url
from database import Base

# Import all models so Alembic can detect them
# This is important! If you don't import models, Alembic won't see them
from models import *  # noqa: F401, F403

# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Add your model's MetaData object here for 'autogenerate' support
# This allows Alembic to automatically detect schema changes
target_metadata = Base.metadata

# Other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_url():
    """
    Get the database URL from our application config.
    
    This overrides the URL in alembic.ini with the one from config.py,
    which allows us to use environment variables for database configuration.
    """
    return get_database_url()


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.
    
    LEARNING NOTES:
    - Offline mode generates SQL scripts without connecting to database
    - Useful for generating migration SQL to run manually
    - Run with: alembic upgrade head --sql > migration.sql
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    
    LEARNING NOTES:
    - Online mode connects to the database and runs migrations directly
    - This is the default mode when you run: alembic upgrade head
    - Changes are applied immediately to the database
    """
    # Override the sqlalchemy.url in alembic.ini with our config
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # Don't use connection pooling for migrations
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# Determine which mode to run in
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
