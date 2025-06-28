from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from src.features.auth.models import UserRole
from src.features.auth.models.user_model import User
from src.features.auth.repository.login_history_repository import record_login_event
from src.features.auth.schemas.user_schema import UserCreate, UserLogin
from src.core.security.security import verify_password, get_password_hash
from src.core.security.jwt import create_access_token, create_refresh_token, verify_token
from src.features.auth.service.role_service import get_role_by_id


def create_user(db: Session, user: UserCreate) -> User:
    if user.password != user.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, user: UserLogin) -> Optional[User]:
    db_user = get_user_by_email(db, user.email)
    if not db_user:
        return None
    if not verify_password(user.password, db_user.hashed_password):
        return None

    # Update last login
    db_user.last_login = datetime.now(timezone.utc)

    record_login_event(db, db_user)
    db.commit()

    return db_user


def assign_role_to_user(db: Session, user_id: UUID, role_id: UUID) -> User:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    # Check if already assigned
    if any(ur.role_id == role_id for ur in user.user_roles):
        raise HTTPException(status_code=400, detail="Role already assigned to user")

    # Create the association explicitly
    user_role = UserRole(user_id=user_id, role_id=role_id)
    db.add(user_role)
    db.commit()
    db.refresh(user)

    return user


def remove_role_from_user(db: Session, user_id: UUID, role_id: UUID):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = get_role_by_id(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    user_role = db.query(UserRole).filter_by(user_id=user_id, role_id=role_id).first()
    if not user_role:
        raise HTTPException(status_code=404, detail="Role not assigned to user")

    db.delete(user_role)
    db.commit()
    return {"detail": f"Role '{role.name}' removed from user '{user.email}'"}


def create_user_tokens(user: User) -> dict:
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


def refresh_access_token(db: Session, refresh_token: str) -> dict:
    email = verify_token(refresh_token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = get_user_by_email(db, email)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    return create_user_tokens(user)


def request_password_reset(db: Session, email: str) -> bool:
    user = get_user_by_email(db, email)
    if not user:
        # Return True even if the user doesn't exist for security
        return True

    # Generate password reset token
    reset_token = create_access_token(
        data={"sub": user.email, "type": "reset"},
        expires_delta=timedelta(hours=1)
    )

    # TODO: Send email with reset token
    # For now, just print it (implement proper email sending in production)
    print(f"Password reset token for {email}: {reset_token}")

    return True


def reset_password(db: Session, token: str, new_password: str) -> bool:
    email = verify_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.hashed_password = get_password_hash(new_password)
    db.commit()

    return True


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()
