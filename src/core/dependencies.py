from fastapi import Request, Depends
from typing import Annotated
from sqlalchemy.orm import Session

from src.core.database.config import SessionLocal
from src.core.middleware.utm_middleware import UtmParams


# UTM Middleware for getting utm params
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
