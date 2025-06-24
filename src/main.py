from fastapi import FastAPI
from src.core.database.config import Base, engine

from src.features.auth.api.auth_router import router as auth_router
from src.features.inventory.api.router import router as inventory_router

app = FastAPI(
    title="Inventory Management API",
    description="This API manages inventory operations such as products and users.",
    # version="1.0.0",
    # swagger_ui_parameters={
    #     "defaultModelsExpandDepth": -1  # Collapse models section
    # }
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
