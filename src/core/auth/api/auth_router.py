from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from sqlalchemy.orm import Session

from src.core.auth.schemas.user_schema import (
    UserCreate, UserOut, PasswordReset, PasswordResetConfirm, UserLogin
)
from src.core.auth.schemas.token import TokenResponse, RefreshToken
from src.core.auth.service.auth_services import (
    create_user, authenticate_user, create_user_tokens,
    refresh_access_token, request_password_reset,
    reset_password, verify_token
)
from src.core.auth.models.user import User  # Needed for ORM query
from src.dependencies import DbSession, get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


# Get current user dependency
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserOut:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = verify_token(token)
    if not email:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise credentials_exception

    return UserOut.from_orm(user)


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.post("/login", response_model=TokenResponse)
def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, UserLogin(email=form_data.username, password=form_data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_user_tokens(user)


@router.post("/refresh", response_model=TokenResponse)
def refresh(refresh_token: RefreshToken, db: Session = Depends(get_db)):
    return refresh_access_token(db, refresh_token.refresh_token)


@router.post("/password-reset/request")
def request_reset(reset_request: PasswordReset, db: Session = Depends(get_db)):
    request_password_reset(db, reset_request.email)
    return {"message": "If the email exists, a password reset link will be sent"}


@router.post("/password-reset/confirm")
def confirm_reset(reset_confirm: PasswordResetConfirm, db: Session = Depends(get_db)):
    if reset_confirm.new_password != reset_confirm.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    reset_password(db, reset_confirm.token, reset_confirm.new_password)
    return {"message": "Password has been reset successfully"}


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    return current_user
