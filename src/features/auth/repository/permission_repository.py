from sqlalchemy.orm import Session

from src.features.auth.models import Permission


def create_permission(db: Session, name: str, description: str = None):
    permission = Permission(name=name, description=description)
    db.add(permission)
    db.commit()
    db.refresh(permission)
    return permission


def get_permissions(db: Session):
    return db.query(Permission).all()


def get_permission(db: Session, permission_id: int):
    return db.query(Permission).filter(Permission.id == permission_id).first()


def delete_permission(db: Session, permission_id: int):
    permission = get_permission(db, permission_id)
    if permission:
        db.delete(permission)
        db.commit()
