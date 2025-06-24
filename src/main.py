from fastapi import FastAPI
from src.core.database import Base, engine

from src.core.auth.api.auth_router import router as auth_router
from src.features.inventory.api.router import router as inventory_router

app = FastAPI(title="Inventory API")

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
