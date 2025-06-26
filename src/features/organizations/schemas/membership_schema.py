from pydantic import BaseModel
from uuid import UUID
from enum import Enum


class MembershipStatus(str, Enum):
    active = "active"
    suspended = "suspended"


class InviteUserDTO(BaseModel):
    user_id: UUID


class MembershipOut(BaseModel):
    user_id: UUID
    organization_id: UUID
    status: MembershipStatus

    class Config:
        orm_mode = True
