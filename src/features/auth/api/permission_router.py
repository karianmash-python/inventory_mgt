from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.security.user_helper import get_current_user

from src.features.auth.models.user_model import User
from src.features.auth.schemas.permission_schema import PermissionCreate, PermissionOut, PermissionUpdate
from src.features.auth.service import permission_service
from src.core.dependencies import get_db_session

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(
        permission: PermissionCreate,
        db: Session = Depends(get_db_session),
        current_user: User = Depends(get_current_user)
):
    return permission_service.create_permission_service(db, permission)


@router.get("/", response_model=list[PermissionOut])
def get_permissions(db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return permission_service.list_permissions_service(db)


@router.get("/{permission_id}", response_model=PermissionOut)
def get_permission(permission_id: UUID, db: Session = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    return permission_service.get_permission_service(db, permission_id)


@router.patch("/{permission_id}", response_model=PermissionOut)
def update_permission(permission_id: UUID, update_data: PermissionUpdate, db: Session = Depends(get_db_session),
                      current_user: User = Depends(get_current_user)):
    return permission_service.update_permission_service(db, permission_id, update_data)


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: UUID, db: Session = Depends(get_db_session),
                      current_user: User = Depends(get_current_user)):
    permission_service.delete_permission_service(db, permission_id)
