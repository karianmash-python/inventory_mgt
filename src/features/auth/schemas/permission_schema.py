from pydantic import BaseModel
from typing import Optional


class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None


class PermissionOut(PermissionCreate):
    id: int

    class Config:
        orm_mode = True
