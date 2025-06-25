from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException, status

from src.features.auth.schemas.permission_schema import PermissionCreate, PermissionUpdate
from src.features.auth.repository import permission_repository
from src.features.auth.models.permission_model import Permission


def create_permission_service(db: Session, permission_data: PermissionCreate) -> Permission:
    existing = permission_repository.get_permission_by_name(db, permission_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission with this name already exists."
        )

    return permission_repository.create_permission(
        db,
        name=permission_data.name,
        description=permission_data.description
    )


def list_permissions_service(db: Session) -> list[Permission]:
    return permission_repository.get_permissions(db)


def get_permission_service(db: Session, permission_id: UUID) -> Permission:
    permission = permission_repository.get_permission(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found."
        )
    return permission


def update_permission_service(db: Session, permission_id: UUID, update_data: PermissionUpdate) -> Permission:
    permission = permission_repository.get_permission(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found."
        )

    if update_data.name:
        existing = permission_repository.get_permission_by_name(db, update_data.name)
        if existing and existing.id != permission_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission name already in use."
            )

    return permission_repository.update_permission(db, permission_id, update_data)


def delete_permission_service(db: Session, permission_id: UUID):
    permission = permission_repository.get_permission(db, permission_id)
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Permission not found."
        )
    return permission_repository.delete_permission(db, permission_id)
