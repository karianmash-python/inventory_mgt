from fastapi import APIRouter

from src.features.auth.api.auth_router import router as auth_router
from src.features.auth.api.role_router import router as role_router
from src.features.auth.api.permission_router import router as permission_router

router = APIRouter()

# Mount individual routers
router.include_router(auth_router)
router.include_router(role_router)
router.include_router(permission_router)

__all__ = ["router"]
