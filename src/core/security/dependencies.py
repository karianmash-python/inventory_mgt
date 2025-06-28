from fastapi import Depends, HTTPException, status
from typing import Callable
from sqlalchemy.orm import Session

from src.features.auth.models.user_model import User
from src.core.security.user_helper import get_current_user
from src.dependencies import get_db


def require_permission(permission: str) -> Callable:
    def checker(
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user),
    ):
        # Flatten all permissions from the user's roles
        user_permissions = {
            perm.name
            for role in current_user.roles
            for perm in role.permissions
        }

        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permission: {permission}"
            )

    return checker
