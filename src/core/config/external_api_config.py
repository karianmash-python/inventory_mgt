from pydantic import BaseSettings


class ExternalAPISettings(BaseSettings):
    example_api_base_url: str = "https://api.example.com"
    example_api_key: str = "your-default-api-key"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


external_api_settings = ExternalAPISettings()
