from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class OrganizationCreate(BaseModel):
    name: str
    description: Optional[str]


class OrganizationUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]


class OrganizationOut(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
