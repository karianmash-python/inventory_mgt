from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    port: int = Field(..., env="APP_PORT")
    reload: bool = Field(False, env="RELOAD")

    class Config:
        env_file = ".env"


app_settings = AppSettings()
