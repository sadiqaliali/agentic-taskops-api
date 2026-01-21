from collections.abc import AsyncGenerator
from urllib.parse import urlparse, parse_qs, urlunparse

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from config.settings import settings

# --- Database URL Transformation for asyncpg ---
# Why: The asyncpg driver does not handle URL query parameters like 'sslmode'
# or 'channel_binding' correctly. They can be misinterpreted as part of the
# database name, leading to an InvalidCatalogNameError.
# This block of code properly parses the database URL, extracts the 'sslmode'
# to configure the SSL connection via connect_args, and then rebuilds the URL
# without any query parameters to ensure the driver connects to the correct database.

# Parse the full database URL from settings
db_url = urlparse(str(settings.DATABASE_URL))

# Parse the query string into a dictionary
query_params = parse_qs(db_url.query)

connect_args = {}

# Check for 'sslmode' and translate it to the 'ssl' connect_arg for asyncpg
if "sslmode" in query_params:
    sslmode = query_params.get("sslmode", [None])[0]
    if sslmode in ["require", "prefer", "allow"]:
        connect_args["ssl"] = True
    elif sslmode == "disable":
        connect_args["ssl"] = False
    # Note: 'verify-ca' and 'verify-full' require a more complex SSLContext object

# Rebuild the URL without any query parameters
clean_db_url = urlunparse(db_url._replace(query=""))

# Why: Create an asynchronous engine.
# The 'echo' setting logs SQL statements in debug mode.
# `connect_args` handles SSL, and the URL is now clean of query parameters.
# The pool settings are added for robust connection management in serverless/cloud environments.
async_engine = create_async_engine(
    clean_db_url,
    echo=settings.DEBUG,
    future=True,
    connect_args=connect_args,
    pool_size=10,
    max_overflow=20,
    pool_recycle=1800,
    pool_pre_ping=True,
)

# Why: Create a factory for asynchronous sessions.
AsyncSessionFactory = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def create_db_and_tables():
    """
    Development utility to create all database tables.
    For production, use Alembic for migrations.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency to provide a database session per request.
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()
