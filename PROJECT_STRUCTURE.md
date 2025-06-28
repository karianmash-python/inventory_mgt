# Project Structure Documentation

This document outlines the structure of the FastAPI application, designed for scalability, modularity, and maintainability.

## High-Level Philosophy

The project follows a **modular, feature-based architecture**. Each distinct business domain (e.g., Authentication, Inventory, Organizations) is encapsulated within its own "feature" directory. This approach promotes separation of concerns, making the codebase easier to navigate, develop, and test.

## Top-Level Directories

- **`/`**: The project root. Contains configuration files for Docker, Alembic, and the main application entry point.
  - `main.py`: The main FastAPI application entry point. It initializes the app, includes feature routers, and sets up middleware.
  - `alembic.ini` & `/alembic`: Configuration and scripts for database migrations using Alembic.
  - `Dockerfile` & `docker-compose.yml`: Files for containerizing the application.
  - `README.md`: General project information.
  - `PROJECT_STRUCTURE.md`: This file.

- **/src**: The main source code for the application.
  - **/core**: Contains cross-cutting concerns and core application logic shared across features.
    - `config/`: Application configuration (database, JWT, logging, etc.).
    - `database/`: SQLAlchemy base models and database session management.
    - `security/`: Authentication, authorization, password hashing, and CORS logic.
    - `logging/`: Application-wide logging setup and activity logging.
    - `rate_limiter/`: Global rate limiting implementation.
    - `dependencies.py`: Shared FastAPI dependencies.
    - `middleware.py`: Application middleware.
  - **/features**: Houses all the business-specific modules.
  - **/utils**: General utility functions and custom exception handlers.

- **/tests**: Contains all tests for the application. The structure within `tests` should mirror the `src` directory.

## Feature Module Structure

Each module inside `src/features/<feature_name>/` follows a standardized structure:

- **/api**: Defines the API endpoints.
  - `*_router.py`: Contains the FastAPI `APIRouter` for the feature, exposing the endpoints.

- **/service**: Contains the business logic.
  - `*_service.py`: Implements the core functionality for the feature, acting as an intermediary between the API layer and the data layer.

- **/repository**: Handles data access and persistence.
  - `*_repository.py`: Contains functions to query the database, interacting with the SQLAlchemy models.

- **/models**: Defines the database table structures.
  - `*_model.py`: Contains the SQLAlchemy ORM models for the feature.

- **/schemas**: Defines the data shapes for API requests and responses.
  - `*_schema.py`: Contains the Pydantic models used for data validation and serialization.

- **/tests**: Co-located tests for the feature (optional, can also be in the root `tests` directory).

---

## Changes Made

To align with this structure, the following files and directories have been renamed or moved:

- **Centralized Core Files:**
  - `src/dependencies.py` -> `src/core/dependencies.py`
  - `src/middleware.py` -> `src/core/middleware.py`

- **Standardized Feature File Naming:**
  - `src/features/auth/service/auth_services.py` -> `src/features/auth/service/auth_service.py`
  - `src/features/inventory/api/inventory_router.py` -> `src/features/inventory/api/router.py`
  - `src/features/inventory/models/product.py` -> `src/features/inventory/models/product_model.py`
  - `src/features/inventory/repository/inventory_repo.py` -> `src/features/inventory/repository/inventory_repository.py`
  - `src/features/inventory/services/` -> `src/features/inventory/service/`
  - `src/features/stock/api/router.py` -> `src/features/stock/api/stock_router.py`
  - `src/features/stock/models/stock.py` -> `src/features/stock/models/stock_model.py`
  - `src/features/stock/repository/stock_repo.py` -> `src/features/stock/repository/stock_repository.py`
  - `src/features/stock/services/` -> `src/features/stock/service/`
  - `src/features/warehouse/api/router.py` -> `src/features/warehouse/api/warehouse_router.py`
  - `src/features/warehouse/models/warehouse.py` -> `src/features/warehouse/models/warehouse_model.py`
  - `src/features/warehouse/repository/warehouse_repo.py` -> `src/features/warehouse/repository/warehouse_repository.py`
