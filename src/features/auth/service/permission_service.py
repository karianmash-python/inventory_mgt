from sqlalchemy.orm import Session
from src.features.auth.schemas.permission_schema import PermissionCreate
from src.features.auth.repository import permission_repository


def create_permission_service(db: Session, permission_data: PermissionCreate):
    return permission_repository.create_permission(db, name=permission_data.name,
                                                   description=permission_data.description)


def list_permissions_service(db: Session):
    return permission_repository.get_permissions(db)


def delete_permission_service(db: Session, permission_id: int):
    return permission_repository.delete_permission(db, permission_id)
