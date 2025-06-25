from sqlalchemy.orm import Session

from src.features.auth.models import Role


def create_role(db: Session, name: str, description: str = None):
    role = Role(name=name, description=description)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role


def get_roles(db: Session):
    return db.query(Role).all()


def get_role(db: Session, role_id: int):
    return db.query(Role).filter(Role.id == role_id).first()


def delete_role(db: Session, role_id: int):
    role = get_role(db, role_id)
    if role:
        db.delete(role)
        db.commit()
