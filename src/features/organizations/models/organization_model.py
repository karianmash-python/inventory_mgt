from sqlalchemy import Column, String
from src.core.database.base_audit import AuditBase
from sqlalchemy.orm import relationship


class Organization(AuditBase):
    __tablename__ = "organizations"

    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    members = relationship("OrganizationMembership", back_populates="organization", cascade="all, delete-orphan")
