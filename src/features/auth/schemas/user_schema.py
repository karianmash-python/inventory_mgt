from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from src.features.auth.schemas.role_schema import RoleOut


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    confirm_password: str


class UserLogin(UserBase):
    password: str


class UserOut(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    roles: List[RoleOut]

    class Config:
        orm_mode = True


class RoleAssignIn(BaseModel):
    user_id: UUID
    role_id: UUID


class LoginEventDTO(BaseModel):
    id: UUID
    user_id: UUID
    login_time: datetime

    class Config:
        orm_mode = True


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
    confirm_password: str
