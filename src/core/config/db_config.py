from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    user: str = Field(..., env="DB_USER")
    password: str = Field(..., env="DB_PASSWORD")
    host: str = Field(..., env="DB_HOST")
    port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")

    @property
    def url(self) -> str:
        return f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"

    class Config:
        env_file = ".env"


db_settings = DBSettings()
