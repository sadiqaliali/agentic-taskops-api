# --- Builder Stage ---
# Why: Use a full-featured base image to build dependencies, keeping the final image lean.
FROM python:3.11 as builder

# Why: Set a non-root user with a designated home directory for security.
RUN useradd --create-home --shell /bin/bash appuser
WORKDIR /home/appuser

# Why: Install uv, the fast package installer used by the project.
RUN pip install uv

# Why: Copy only the dependency files first to leverage Docker's layer caching.
# Dependencies change less often than source code, so this layer is rebuilt less frequently.
COPY pyproject.toml uv.lock ./

# Why: Install dependencies into a virtual environment.
# This isolates dependencies and mirrors the local development setup.
RUN uv venv .venv && . .venv/bin/activate && uv sync --no-dev


# --- Runner Stage ---
# Why: Use a slim base image for the final container to reduce its size and attack surface.
FROM python:3.11-slim

# Why: Set environment variables for Python.
# - UNBUFFERED: Prevents Python from buffering stdout/stderr, ensuring logs appear in real-time.
# - PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files, which aren't needed in a container.
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Why: Create a non-root user for running the application to enhance security.
RUN useradd --create-home --shell /bin/bash appuser
USER appuser
WORKDIR /home/appuser/app

# Why: Copy the virtual environment with all its dependencies from the builder stage.
COPY --from=builder /home/appuser/.venv .venv

# Why: Copy the application source code into the final image.
COPY . .

# Why: Make the entrypoint script executable.
# This script will run migrations and then start the application server.
RUN chmod +x ./docker-entrypoint.sh

# Why: Expose port 8000 to allow traffic to the FastAPI application.
EXPOSE 8000

# Why: Set the entrypoint script to run when the container starts.
# This ensures migrations are applied before the app server boots up.
ENTRYPOINT ["/home/appuser/app/docker-entrypoint.sh"]
