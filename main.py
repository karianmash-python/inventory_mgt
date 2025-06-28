import uvicorn
from fastapi import FastAPI

from src.core.config.app_config import app_settings
from src.core.config.logging_config import setup_logging
from src.core.rate_limiter.handlers import init_rate_limiter

# Setup logging
setup_logging()

from src.core.database.config import Base, engine
from src.core.security.cors import configure_cors

# Import routers
from src.features.auth.api import router as auth_router  # Authentication, Authorization, and User Management
from src.features.organizations.api.organization_router import router as organization_router
from src.features.inventory.api.router import router as inventory_router

# Create FastAPI app and configure settings
app = FastAPI(
    title="Inventory Management API",
    description="This API manages inventory operations such as products and users.",
    version="1.0.0",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,  # Equivalent to springdoc.swagger-ui.defaultModelsExpandDepth=-1
        "defaultModelExpandDepth": 1,
        "displayOperationId": True,
        "displayRequestDuration": True,
        "docExpansion": "none",  # Can be "list", "full", or "none"
        "filter": True,
        "showExtensions": False,
        "showCommonExtensions": True,
        "tryItOutEnabled": True,
    }
)

# Register CORS settings
configure_cors(app)

# Attach limiter middleware and handler
init_rate_limiter(app)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(organization_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=app_settings.port, reload=app_settings.reload)
