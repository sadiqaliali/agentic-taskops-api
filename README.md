# Agentic TaskOps API

A production-grade, asynchronous, and secure FastAPI backend designed to serve as a robust foundation for internal or SaaS-based AI agentic applications. 

---

## Vision & Mission

In the rapidly evolving world of AI, developers need more than just a simple API. They need a stable, scalable, and secure "operating system" to deploy, manage, and monitor their AI agents. 

The mission of **Agentic TaskOps API** is to be that system. This project provides the essential backend infrastructure—from asynchronous task handling to enterprise-grade security—so developers can focus on building intelligent agents, not rebuilding boilerplate infrastructure.

---

## Project Status & Roadmap

This project is actively developed. We have a clear roadmap for new features and enhancements.

### ✅ Version 1.0: Core Foundation

-   **Asynchronous Core**: High-performance stack (FastAPI, SQLAlchemy 2.0).
-   **Secure Authentication**: JWT-based login with password hashing.
-   **Protected Task Management API**: Full async CRUD for tasks with ownership-based authorization.
-   **Production-Ready Tooling**: `uv` for dependency management and Alembic for migrations.
-   **Containerization**: Ready-to-use `Dockerfile`.

### 🚀 Version 2.0: Production Readiness & Core Features

This version focuses on building a robust, scalable, and monitorable foundation, making the API ready for production use and more advanced agentic workflows.

-   [ ] **Observability & Monitoring:** Structured logging, Prometheus metrics, and distributed tracing.
-   [ ] **Asynchronous Task Queues:** Celery/ARQ integration for true background processing.
-   [ ] **Scheduled & Recurring Tasks:** Time-based and recurring job scheduling.
-   [ ] **Real-Time Updates:** WebSocket integration for live task updates.
-   [ ] **Enhanced Security:** Role-Based Access Control (RBAC) and dedicated API Key management.
-   [ ] **High Availability:** Advanced health checks and graceful shutdown procedures.

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
-   Docker & Docker Compose
-   `uv` (can be installed with `pip install uv`)

### 1. Set Up The Environment

Clone the repository and create a `.env` file from the example.

```shell
cp .env.example .env
```
**Edit the `.env` file** with your database credentials and a unique `SECRET_KEY`.

### 2. Install & Run (Docker Recommended)

For a seamless setup, we recommend using Docker. 

```shell
# Build and run the API and a PostgreSQL database
docker-compose up --build
```
The API will be available at `http://127.0.0.1:8000`. Migrations are applied automatically on startup.

### 3. Local Development (Without Docker)

If you prefer to run locally:
```shell
# Install dependencies
uv sync

# Run database migrations
alembic upgrade head

# Run the development server
uv run uvicorn app.main:app --reload
```
---

## API Endpoints

The interactive API documentation (Swagger UI) is available at `http://127.0.0.1:8000/docs` once the application is running.