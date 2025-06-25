from sqlalchemy.orm import Session

from src.features.auth.schemas.role_schema import RoleCreate
from src.features.auth.repository import role_repository


def create_role_service(db: Session, role_data: RoleCreate):
    return role_repository.create_role(db, name=role_data.name, description=role_data.description)


def list_roles_service(db: Session):
    return role_repository.get_roles(db)


def delete_role_service(db: Session, role_id: int):
    return role_repository.delete_role(db, role_id)
