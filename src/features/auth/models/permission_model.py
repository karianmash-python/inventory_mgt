from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.core.database.base_audit import AuditBase


class Permission(AuditBase):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    roles = relationship(
        "Role",  # This tells SQLAlchemy: “I want to link to the Role model.”
        secondary="role_permissions",  # This tells it: “Go through the role_permissions table (join table)”
        back_populates="permissions"  # This creates a 2-way link: Role -> Permission and Permission -> Role
    )
