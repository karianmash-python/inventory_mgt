from typing import Optional
from pydantic import BaseModel

from src.features.auth.schemas.user_schema import UserOut


class TokenData(BaseModel):
    email: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshToken(BaseModel):
    refresh_token: str

class LoginResponse(TokenResponse):
    user: UserOut