#!/bin/bash
set -e
cd /home/appuser/app

echo "Waiting for the database to be ready..."
sleep 10

echo "Applying database migrations..."
# Use the python from the venv directly
/home/appuser/app/.venv/bin/python -m alembic upgrade head

echo "Starting FastAPI application..."
# Use the python from the venv directly
exec /home/appuser/app/.venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000