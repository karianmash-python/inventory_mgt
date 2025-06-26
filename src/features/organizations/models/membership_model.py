from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from enum import Enum as PyEnum

from src.core.database.base_audit import AuditBase


class MembershipStatus(PyEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"


class OrganizationMembership(AuditBase):
    __tablename__ = "organization_memberships"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(MembershipStatus), default=MembershipStatus.ACTIVE, nullable=False)

    user = relationship("User", backref="organization_memberships")
    organization = relationship("Organization", back_populates="members")
