from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID

from src.features.auth.schemas.permission_schema import PermissionOut


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class RolePermissionAssign(BaseModel):
    permissions: List[PermissionOut]


class RoleOut(RoleCreate):
    id: UUID

    class Config:
        orm_mode = True
