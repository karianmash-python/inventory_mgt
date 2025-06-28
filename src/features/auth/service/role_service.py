from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from uuid import UUID

from src.features.auth.schemas.role_schema import RoleCreate, RoleUpdate
from src.features.auth.repository import role_repository, permission_repository
from src.features.auth.models.role_model import Role


def create_role_service(db: Session, role_data: RoleCreate) -> Role:
    existing = role_repository.get_role_by_name(db, role_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role with this name already exists."
        )
    return role_repository.create_role(db, name=role_data.name, description=role_data.description)


def list_roles_service(db: Session) -> list[Role]:
    return role_repository.get_roles(db)


def get_role_by_id(db: Session, role_id: UUID) -> Role:
    role = role_repository.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role


def update_role_service(db: Session, role_id: UUID, update_data: RoleUpdate) -> Role:
    role = role_repository.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    if update_data.name:
        existing = role_repository.get_role_by_name(db, update_data.name)
        if existing and existing.id != role_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already in use."
            )

    return role_repository.update_role(db, role, update_data)


def delete_role_service(db: Session, role_id: UUID):
    role = role_repository.get_role(db, role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role_repository.delete_role(db, role_id)


def assign_permissions_to_role_service(db: Session, role_id: UUID, permission_ids: list[UUID]):
    role = get_role_by_id(db, role_id)

    permissions = permission_repository.get_permissions_by_ids(db, permission_ids)
    if len(permissions) != len(permission_ids):
        raise HTTPException(
            status_code=400,
            detail="One or more permissions not found."
        )

    role.permissions = permissions
    db.commit()
    db.refresh(role)
    return role
