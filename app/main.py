from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import auth, tasks, agent
from config.settings import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle application startup and shutdown events.
    """
    # NOTE: In a real production environment, you would use a migration tool like Alembic
    # to manage your database schema. This startup event is included for convenience
    # in a development setting.
    if settings.DEBUG:
        print("Running in debug mode. Creating database and tables...")
        await create_db_and_tables()
    yield
    # Any shutdown logic would go here

# Why: Initialize the FastAPI application with a title, version, and the lifespan context manager.
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    lifespan=lifespan
)

# --- API Routers ---
# Why: Include the routers with prefixes to organize the API endpoints.
# Tags are defined within each router file, so they don't need to be repeated here.
app.include_router(auth.router, prefix="/auth")
app.include_router(tasks.router, prefix="/tasks")
app.include_router(agent.router, prefix="/agent")


# --- Root Endpoint ---
# Why: A root endpoint that provides a simple health check or welcome message.
@app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint providing a welcome message and application version.
    """
    return {"message": f"Welcome to {settings.APP_NAME} v{settings.APP_VERSION}"}
