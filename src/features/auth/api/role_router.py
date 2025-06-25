from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.security.user_helper import get_current_user

from src.features.auth.models.user_model import User
from src.features.auth.schemas.role_schema import RoleCreate, RoleOut
from src.features.auth.service import role_service
from src.dependencies import get_db

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_role(role: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return role_service.create_role_service(db, role)


@router.get("/", response_model=list[RoleOut])
def get_roles(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return role_service.list_roles_service(db)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    role_service.delete_role_service(db, role_id)
