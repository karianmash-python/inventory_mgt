from sqlalchemy.orm import Session
from uuid import UUID

from src.features.organizations.models.organization_model import Organization
from src.features.organizations.models.membership_model import OrganizationMembership, MembershipStatus


def create_organization(db: Session, name: str, description: str) -> Organization:
    org = Organization(name=name, description=description)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org


def get_organization(db: Session, org_id: UUID) -> Organization:
    return db.query(Organization).filter(Organization.id == org_id).first()


def get_all_organizations(db: Session):
    return db.query(Organization).all()


def update_organization(db: Session, org: Organization, name: str, description: str):
    org.name = name
    org.description = description
    db.commit()


def delete_organization(db: Session, org: Organization):
    db.delete(org)
    db.commit()


def invite_user(db: Session, org_id: UUID, user_id: UUID):
    membership = OrganizationMembership(user_id=user_id, organization_id=org_id)
    db.add(membership)
    db.commit()
    return membership


def remove_user(db: Session, org_id: UUID, user_id: UUID):
    membership = db.query(OrganizationMembership).filter_by(organization_id=org_id, user_id=user_id).first()
    if membership:
        db.delete(membership)
        db.commit()


def change_membership_status(db: Session, org_id: UUID, user_id: UUID, status: MembershipStatus):
    membership = db.query(OrganizationMembership).filter_by(organization_id=org_id, user_id=user_id).first()
    if membership:
        membership.status = status
        db.commit()
        return membership
    return None
