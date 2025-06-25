from pydantic import BaseModel
from typing import List, Optional


class RoleCreate(BaseModel):
    name: str
    description: Optional[str] = None


class RoleOut(RoleCreate):
    id: int

    class Config:
        orm_mode = True
