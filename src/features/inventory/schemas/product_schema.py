from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    name: str = Field(..., example="Maize Flour")
    sku: str = Field(..., example="MF-001")
    description: str | None = Field(None, example="Refined maize flour")
    unit: str = Field(..., example="kg")


class ProductCreate(ProductBase):
    pass


class ProductOut(ProductBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
