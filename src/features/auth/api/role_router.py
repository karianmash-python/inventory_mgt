from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from src.core.security.user_helper import get_current_user
from src.features.auth.models.user_model import User
from src.features.auth.schemas.role_schema import RoleCreate, RoleUpdate, RoleOut, RolePermissionAssign
from src.features.auth.service import role_service
from src.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(
        role: RoleCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return role_service.create_role_service(db, role)


@router.get("/", response_model=list[RoleOut])
def get_roles(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return role_service.list_roles_service(db)


@router.get("/{role_id}", response_model=RoleOut)
def get_role(
        role_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return role_service.get_role_service(db, role_id)


@router.put("/{role_id}", response_model=RoleOut)
def update_role(
        role_id: UUID,
        update_data: RoleUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return role_service.update_role_service(db, role_id, update_data)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(
        role_id: UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    role_service.delete_role_service(db, role_id)


@router.post("/{role_id}/permissions", response_model=RoleOut)
def assign_permissions_to_role(
        role_id: UUID,
        data: RolePermissionAssign,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return role_service.assign_permissions_to_role_service(db, role_id, data.permission_ids)
