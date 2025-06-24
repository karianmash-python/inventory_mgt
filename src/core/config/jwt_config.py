import os
from pydantic import BaseSettings, Field


class JWTSettings(BaseSettings):
    secret: str = Field(..., env="SECRET_KEY")
    algorithm: str = Field("HS256", env="ALGORITHM")
    access_token_expire_minutes: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(7, env="REFRESH_TOKEN_EXPIRE_DAYS")

    class Config:
        env_file = ".env"


jwt_settings = JWTSettings()
