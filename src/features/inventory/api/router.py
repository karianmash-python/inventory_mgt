from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.features.inventory.schemas.product_schema import ProductCreate, ProductOut
from src.features.inventory.services import inventory_service
from src.core.security.user_helper import get_current_user

router = APIRouter(prefix="/products", tags=["Inventory"])


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_current_user)
):
    return inventory_service.create_new_product(db, product)


@router.get("/", response_model=list[ProductOut])
def get_products(
        db: Session = Depends(get_current_user)
):
    return inventory_service.list_all_products(db)
