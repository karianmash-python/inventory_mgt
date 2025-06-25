from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.security.user_helper import get_current_user

from src.features.auth.models.user_model import User
from src.features.auth.schemas.permission_schema import PermissionCreate, PermissionOut
from src.features.auth.service import permission_service
from src.dependencies import get_db

router = APIRouter(prefix="/permissions", tags=["Permissions"])


@router.post("/", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_permission(
        permission: PermissionCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return permission_service.create_permission_service(db, permission)


@router.get("/", response_model=list[PermissionOut])
def get_permissions(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return permission_service.list_permissions_service(db)


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(permission_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    permission_service.delete_permission_service(db, permission_id)
