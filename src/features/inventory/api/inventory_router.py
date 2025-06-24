from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session

from src.core.rate_limiter.limiter import limiter
from src.dependencies import get_db
from src.features.inventory.schemas.product_schema import ProductCreate, ProductOut
from src.features.inventory.services import inventory_service
from src.core.security.user_helper import get_current_user
from src.features.auth.models.user import User

router = APIRouter(prefix="/products", tags=["Inventory"])


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return inventory_service.create_new_product(db, product)


@router.get("/", response_model=list[ProductOut])
@limiter.limit("2/minute")  # Optional override
def get_products(
        request: Request,  # HTTP request for rate limiting (required by SlowAPI)
        db: Session = Depends(get_db),  # DB session
        user: User = Depends(get_current_user)
        # Authenticated user for protecting routes. Enables JWT-based rate limiting via the user_or_ip_key_func
):
    return inventory_service.list_all_products(db)
