#!/bin/bash
# docker-entrypoint.sh

# Why: Exit immediately if a command exits with a non-zero status.
set -e

# Why: Navigate to the application directory as defined in the Dockerfile WORKDIR.
cd /home/appuser/app

# --- Wait for Database ---
# Why: Add a 10-second delay. This is a simple but effective way to give an external
# database (like Neon) time to accept connections before the application tries to
# run migrations or start up. This prevents crashes on startup due to race conditions.
echo "Waiting for the database to be ready..."
sleep 10

# Why: Apply Alembic database migrations. This ensures the database schema is up-to-date
# before the application attempts to connect and use it.
echo "Applying database migrations..."
./.venv/bin/alembic upgrade head

# Why: Start the FastAPI application using Uvicorn.
# --host 0.0.0.0 makes the application accessible from outside the container.
# --port 8000 matches the EXPOSE instruction in the Dockerfile.
echo "Starting FastAPI application..."
exec ./.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000