from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional

from src.features.auth.models.permission_model import Permission
from src.features.auth.schemas.permission_schema import PermissionUpdate


def create_permission(db: Session, name: str, description: Optional[str] = None) -> Permission:
    permission = Permission(name=name, description=description)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def get_permissions(db: Session) -> list[Permission]:
    return db.query(Permission).all()


def get_permission(db: Session, permission_id: UUID) -> Optional[Permission]:
    return db.query(Permission).filter(Permission.id == permission_id).first()


def get_permission_by_name(db: Session, name: str) -> Optional[Permission]:
    return db.query(Permission).filter(Permission.name == name).first()


def update_permission(db: Session, permission_id: UUID, update_data: PermissionUpdate) -> Optional[Permission]:
    permission = get_permission(db, permission_id)
    if not permission:
        return None

    if update_data.name is not None:
        permission.name = update_data.name
    if update_data.description is not None:
        permission.description = update_data.description

    db.commit()
    db.refresh(permission)
    return permission


def delete_permission(db: Session, permission_id: UUID) -> None:
    permission = get_permission(db, permission_id)
    if permission:
        db.delete(permission)
        db.commit()


def get_permissions_by_ids(db: Session, ids: list[UUID]) -> list[Permission]:
    return db.query(Permission).filter(Permission.id.in_(ids)).all()
