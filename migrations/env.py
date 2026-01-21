import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# Add the app directory to the path so we can import the models
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))

# add your model's MetaData object here
# for 'autogenerate' support
from app.models import user, task  # noqa
from sqlmodel import SQLModel
target_metadata = SQLModel.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
from config.settings import settings
# Why: Alembic runs synchronously, so it needs a sync database driver.
# We get the async URL from the settings, which might contain '+asyncpg'
# and async-specific query parameters (e.g., '?ssl=true').
# We convert it to a sync-compatible URL for psycopg2.
db_url = settings.ALEMBIC_DATABASE_URL or settings.DATABASE_URL
# 1. Convert the Pydantic DSN object to a string.
# 2. Remove the '+asyncpg' driver part.
# 3. Split the URL at the query string '?' and take the first part to remove all query params.
sync_db_url = str(db_url).replace("+asyncpg", "").split("?")[0]
config.set_main_option('sqlalchemy.url', sync_db_url)


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
