from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from src.features.auth.models.role_model import Role
from src.features.auth.schemas.role_schema import RoleUpdate


def create_role(db: Session, name: str, description: str = None) -> Role:
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_roles(db: Session) -> list[Role]:
    return db.query(Role).all()


def get_role(db: Session, role_id: UUID) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()


def update_role(db: Session, role: Role, update_data: RoleUpdate) -> Role:
    if update_data.name is not None:
        role.name = update_data.name
    if update_data.description is not None:
        role.description = update_data.description

    db.commit()
    db.refresh(role)
    return role


def delete_role(db: Session, role_id: UUID):
    role = get_role(db, role_id)
    if role:
        db.delete(role)
        db.commit()
