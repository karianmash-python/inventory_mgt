from fastapi import Request, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from src.core.database.config import SessionLocal
from src.features.tracking.middleware.utm_middleware import UtmParams
from src.core.http.http_client import HttpClient
from src.core.config.external_api_config import external_api_settings


# Dependency to get the http client
def get_http_client() -> HttpClient:
    return HttpClient(
        base_url=external_api_settings.example_api_base_url,
        api_key=external_api_settings.example_api_key,
    )


# Dependency to get UTM params from the middleware
def get_utm_params(request: Request) -> UtmParams:
    return request.state.utm_params


# DB Session Dependency
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db_session)]
