from typing import Annotated
from sqlalchemy.orm import Session
from src.core.database.config import SessionLocal
from fastapi import Depends


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
