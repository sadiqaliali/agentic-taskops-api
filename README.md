# Agentic TaskOps API - v1.0.0

A production-grade, asynchronous, and secure FastAPI backend designed to serve as a robust foundation for internal or SaaS-based AI agentic applications. This project is architected for stability, scalability, and developer-friendliness from the ground up.

---

## Features

-   **Asynchronous Core**: Built entirely on an `async` stack (FastAPI, SQLAlchemy 2.0, `asyncpg`) for high-performance, non-blocking I/O.
-   **Secure Authentication**:
    -   Secure user registration (`/auth/register`) with `bcrypt` password hashing.
    -   Stateless JWT-based login (`/auth/login`) providing access tokens.
-   **Protected Task Management API**:
    -   Full asynchronous CRUD (Create, Read, Update, Delete) operations for tasks.
    -   Strict ownership-based authorization: Users can only access their own tasks.
-   **Streaming Agent Endpoint**:
    -   Real-time progress updates for long-running agentic tasks via Server-Sent Events (SSE).
-   **Production-Ready Tooling**:
    -   Uses `uv` for fast, modern dependency and environment management.
    -   Includes Alembic for robust database schema migrations.

---

## Tech Stack

-   **Framework**: FastAPI
-   **Database**: PostgreSQL (via `asyncpg`)
-   **ORM / Data Validation**: SQLModel (Pydantic + SQLAlchemy)
-   **Migrations**: Alembic
-   **Authentication**: `python-jose` for JWTs, `passlib[bcrypt]` for hashing
-   **Environment Management**: `uv`

---

## Getting Started

### Prerequisites

-   Python 3.11+
-   PostgreSQL 13+
-   `uv` (can be installed with `pip install uv`)

### 1. Set Up The Environment

First, clone the repository and set up your local `.env` file.

```shell
# Copy the example environment file
cp .env.example .env
```

Now, **edit the `.env` file** with your PostgreSQL database URL and a new, unique `SECRET_KEY`.

### 2. Install Dependencies

Create the virtual environment and install all dependencies using `uv`.

```shell
# Create the virtual environment
uv venv

# Activate the virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On macOS/Linux:
# source .venv/bin/activate

# Install dependencies
uv sync
```

### 3. Run Database Migrations

Apply all database migrations to set up your database schema correctly.

```shell
alembic upgrade head
```

### 4. Run the Application

Start the development server using `uvicorn`.

```shell
uv run uvicorn app.main:app --reload
```

The API will now be running at `http://127.0.0.1:8000`.

---

## API Endpoints

The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs`.

| Method | Path                | Description                               | Auth Required |
|--------|---------------------|-------------------------------------------|:-------------:|
| `GET`  | `/`                 | Health check / Welcome message            |       -       |
| `POST` | `/auth/register`    | Register a new user                       |       -       |
| `POST` | `/auth/login`       | Log in to get a JWT access token          |       -       |
| `POST` | `/tasks/`           | Create a new task                         |      ✅       |
| `GET`  | `/tasks/`           | Get all tasks for the current user        |      ✅       |
| `GET`  | `/tasks/{task_id}`  | Get a specific task by its ID             |      ✅       |
| `PATCH`| `/tasks/{task_id}`  | Update a specific task                    |      ✅       |
| `DELETE`| `/tasks/{task_id}`| Delete a specific task                    |      ✅       |
| `POST` | `/agent/run`        | Run an agent task and stream the response |      ✅       |

---

## Running with Docker

This project includes a `Dockerfile` for easy containerization.

### 1. Build the Docker Image

From the root of the project, run the build command:

```shell
docker build -t agentic-taskops-api .
```

### 2. Run the Docker Container

Run the container, making sure to expose port 8000 and pass your `.env` file.

```shell
docker run --env-file .env -p 8000:8000 agentic-taskops-api
```

The container will start, run the migrations, and launch the application, accessible at `http://127.0.0.1:8000`.

---

## Future Roadmap

-   **CI/CD Integration**: Add GitHub Actions to automate testing, linting, and image publishing to Docker Hub.
-   **Docker Compose**: Add a `docker-compose.yml` for a one-command setup of the API and PostgreSQL database.
-   **Background Task Processing**: Integrate Celery or ARQ for handling truly long-running, non-blocking agent tasks.
-   **Expanded Test Suite**: Increase unit and integration test coverage.
-   **Role-Based Access Control (RBAC)**: Introduce more granular user permissions.
