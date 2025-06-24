from uuid import UUID
from pydantic import BaseModel, Field
from datetime import datetime


class ProductBase(BaseModel):
    name: str = Field(..., example="Maize Flour")
    sku: str = Field(..., example="MF-001")
    description: str | None = Field(None, example="Refined maize flour")
    unit: str = Field(..., example="kg")


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: UUID  # Changed from int to UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        orm_mode = True
