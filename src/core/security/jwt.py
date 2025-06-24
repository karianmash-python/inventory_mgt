from fastapi import HTTPException, status
from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import jwt, JWTError, ExpiredSignatureError

from src.core.config.jwt_config import jwt_settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=jwt_settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, jwt_settings.secret, algorithm=jwt_settings.algorithm)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(days=jwt_settings.refresh_token_expire_days)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, jwt_settings.secret, algorithm=jwt_settings.algorithm)


def verify_token(token: str) -> str:
    try:
        payload = jwt.decode(token, jwt_settings.secret, algorithms=[jwt_settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token payload invalid: missing subject",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return email

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token. Could not validate credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
