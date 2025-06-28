from sqlalchemy.orm import Session
from ..models.product_model import Product
from ..schemas.product_schema import ProductCreate


def create_product(db: Session, product: ProductCreate) -> Product:
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_all_products(db: Session) -> list[Product]:
    return db.query(Product).all()


def get_product_by_sku(db: Session, sku: str) -> Product | None:
    return db.query(Product).filter(Product.sku == sku).first()
