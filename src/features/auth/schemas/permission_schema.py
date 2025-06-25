from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class PermissionCreate(BaseModel):
    name: str
    description: Optional[str] = None


class PermissionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class PermissionOut(PermissionCreate):
    id: UUID

    class Config:
        orm_mode = True
