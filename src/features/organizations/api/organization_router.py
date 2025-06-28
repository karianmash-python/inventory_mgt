from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from src.core.dependencies import get_db
from src.features.organizations.schemas.organization_schema import *
from src.features.organizations.schemas.membership_schema import *
from src.features.organizations.service import organization_service
from src.features.auth.models.user_model import User
from src.core.security.user_helper import get_current_user

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationOut)
def create_org(data: OrganizationCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return organization_service.create_organization(db, name=data.name, description=data.description)


@router.get("/", response_model=list[OrganizationOut])
def get_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return organization_service.get_all_organizations(db)


@router.get("/{org_id}", response_model=OrganizationOut)
def get_one(org_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    org = organization_service.get_organization_by_id(db, org_id)
    if not org:
        raise HTTPException(404, "Organization not found")
    return org


@router.put("/{org_id}")
def update_org(org_id: UUID, data: OrganizationUpdate, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    updated = organization_service.update_organization(db, org_id, data.name, data.description)
    if not updated:
        raise HTTPException(404, "Not found")
    return {"message": "Updated"}


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_org(org_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = organization_service.delete_organization(db, org_id)
    if not deleted:
        raise HTTPException(404, "Not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{org_id}/invite")
def invite_user(org_id: UUID, payload: InviteUserDTO, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    return organization_service.invite_user_to_org(db, org_id, payload.user_id)


@router.delete("/{org_id}/remove/{user_id}")
def remove_user(org_id: UUID, user_id: UUID, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    organization_service.remove_user_from_org(db, org_id, user_id)
    return {"message": "User removed"}


@router.post("/{org_id}/suspend/{user_id}")
def suspend_user(org_id: UUID, user_id: UUID, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    return organization_service.suspend_user(db, org_id, user_id)


@router.post("/{org_id}/unsuspend/{user_id}")
def unsuspend_user(org_id: UUID, user_id: UUID, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    return organization_service.unsuspend_user(db, org_id, user_id)
