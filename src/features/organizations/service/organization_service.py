from uuid import UUID
from sqlalchemy.orm import Session

from src.features.organizations.repository import organization_repository
from src.features.organizations.models.organization_model import Organization
from src.features.organizations.models.membership_model import MembershipStatus


def create_organization(db: Session, name: str, description: str) -> Organization:
    return organization_repository.create_organization(db, name, description)


def get_all_organizations(db: Session):
    return organization_repository.get_all_organizations(db)


def get_organization_by_id(db: Session, org_id: UUID) -> Organization:
    return organization_repository.get_organization(db, org_id)


def update_organization(db: Session, org_id: UUID, name: str, description: str):
    org = get_organization_by_id(db, org_id)
    if not org:
        return None
    organization_repository.update_organization(db, org, name, description)
    return org


def delete_organization(db: Session, org_id: UUID):
    org = get_organization_by_id(db, org_id)
    if not org:
        return None
    organization_repository.delete_organization(db, org)
    return org


def invite_user_to_org(db: Session, org_id: UUID, user_id: UUID):
    return organization_repository.invite_user(db, org_id, user_id)


def remove_user_from_org(db: Session, org_id: UUID, user_id: UUID):
    organization_repository.remove_user(db, org_id, user_id)


def suspend_user(db: Session, org_id: UUID, user_id: UUID):
    return organization_repository.change_membership_status(db, org_id, user_id, MembershipStatus.SUSPENDED)


def unsuspend_user(db: Session, org_id: UUID, user_id: UUID):
    return organization_repository.change_membership_status(db, org_id, user_id, MembershipStatus.ACTIVE)
