import logging

from src.core.logging.service.activity_logger import log_activity
from src.core.security.dependencies import require_permission
from src.features.auth.models.login_history_model import UserLoginHistory
from src.features.tracking.middleware.utm_middleware import UtmParams

logger = logging.getLogger(__name__)

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from sqlalchemy.orm import Session
from uuid import UUID

from src.features.auth.schemas.token import RefreshToken, LoginResponse
from src.core.dependencies import get_db_session, get_utm_params
from src.core.security.user_helper import get_current_user
from src.features.auth.schemas.user_schema import (
    UserCreate, UserOut, PasswordReset, PasswordResetConfirm, UserLogin, LoginEventDTO, RoleAssignIn
)
from src.features.auth.service.auth_service import (
    create_user, authenticate_user, create_user_tokens,
    refresh_access_token, request_password_reset,
    reset_password, assign_role_to_user, remove_role_from_user
)

from src.features.tracking.services.tracking_service import track_event

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(
        user: UserCreate,
        db: Session = Depends(get_db_session),
        utm_params: UtmParams = Depends(get_utm_params),
):
    new_user = create_user(db, user)
    track_event(
        db,
        event_type="user_registration",
        utm_params=utm_params,
        user_id=new_user.id,
    )

    logger.info(f"UTM Parameters: {utm_params.__dict__}")
    return new_user


@router.post("/login", response_model=LoginResponse)
def login(
        login_request: UserLogin,
        db: Session = Depends(get_db_session),
        utm_params: UtmParams = Depends(get_utm_params)
):
    """
    Logs in a user and returns access and refresh tokens.
    """
    logger.info(f"UTM Parameters: {utm_params.__dict__}")
    user = authenticate_user(db, login_request)
    logger.info("User logged in: email=%s id=%s", user.email, user.id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tokens = create_user_tokens(user)

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": tokens["token_type"],
        "user": UserOut.from_orm(user)
    }


@router.post("/assign-role", response_model=UserOut)
def assign_role(payload: RoleAssignIn, db: Session = Depends(get_db_session)):
    return assign_role_to_user(db, payload.user_id, payload.role_id)


@router.delete("/remove-role",
               summary="Remove role from user",
               description="Remove role from user. Requires user:role:remove permission",
               dependencies=[Depends(require_permission("user:role:remove"))])
def remove_role(payload: RoleAssignIn, db=Depends(get_db_session)):
    return remove_role_from_user(db, payload.user_id, payload.role_id)


@router.post("/refresh", response_model=LoginResponse)
def refresh(refresh_token: RefreshToken, db: Session = Depends(get_db_session)):
    return refresh_access_token(db, refresh_token.refresh_token)


@router.post("/password-reset/request")
def request_reset(reset_request: PasswordReset, db: Session = Depends(get_db_session)):
    request_password_reset(db, reset_request.email)
    return {"message": "If the email exists, a password reset link will be sent"}


@router.post("/password-reset/confirm")
def confirm_reset(reset_confirm: PasswordResetConfirm, db: Session = Depends(get_db_session)):
    if reset_confirm.new_password != reset_confirm.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    reset_password(db, reset_confirm.token, reset_confirm.new_password)
    return {"message": "Password has been reset successfully"}


@router.get("/users/{user_id}/login-history", response_model=list[LoginEventDTO])
def get_login_history(
        user_id: UUID,
        db: Session = Depends(get_db_session),
        current_user: UserOut = Depends(get_current_user)
):
    events = db.query(UserLoginHistory).filter(UserLoginHistory.user_id == user_id).all()

    log_activity(db, current_user.id, "VIEW_LOGIN_HISTORY", "USER", current_user.id)
    return events


@router.get("/me", response_model=UserOut)
def read_users_me(current_user: UserOut = Depends(get_current_user)):
    logger.info("Current user: %s", current_user)
    return current_user
