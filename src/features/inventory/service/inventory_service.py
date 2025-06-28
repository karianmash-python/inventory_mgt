from sqlalchemy.orm import Session
from ..schemas.product_schema import ProductCreate
from ..repository import inventory_repository as inventory_repo


def create_new_product(db: Session, product: ProductCreate):
    return inventory_repo.create_product(db, product)


def list_all_products(db: Session):
    return inventory_repository.get_all_products(db)
