from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.dependencies import get_db
from src.features.auth.models.user import User
from src.features.auth.schemas.user_schema import UserOut
from src.features.auth.service.auth_services import verify_token

bearer_scheme = HTTPBearer(
    scheme_name="bearerAuth",
    description="JWT auth description"
)


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db: Session = Depends(get_db)
) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_str = token.credentials
    email = verify_token(token_str)
    if not email:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    return UserOut.from_orm(user)

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Get current user dependency
# async def get_current_user(
#         token: str = Depends(bearer_scheme),
#         db: Session = Depends(get_db)
# ) -> UserOut:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#
#     email = verify_token(token)
#     if not email:
#         raise credentials_exception
#
#     user = db.query(User).filter(User.email == email).first()
#     if not user:
#         raise credentials_exception
#
#     return UserOut.from_orm(user)
