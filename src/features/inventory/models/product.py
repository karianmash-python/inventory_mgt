from sqlalchemy import Column, Integer, String, Boolean

from src.core.database.base_audit import AuditBase


class Product(AuditBase):
    __tablename__ = "products"

    name = Column(String, nullable=False)
    sku = Column(String, unique=True, nullable=False)
    description = Column(String)
    unit = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
