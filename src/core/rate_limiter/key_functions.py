from fastapi import Request
from jose import jwt, JWTError

from src.core.config.jwt_config import jwt_settings


def user_or_ip_key_func(request: Request) -> str:
    auth = request.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        try:
            token = auth.split(" ")[1]
            payload = jwt.decode(token, jwt_settings.secret, algorithms=[jwt_settings.algorithm])
            user_id = payload.get("sub")
            if user_id:
                return f"user:{user_id}"
        except JWTError:
            pass
    return f"ip:{request.client.host}"
