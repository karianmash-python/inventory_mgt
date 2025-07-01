from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.core.database.base_audit import AuditBase
from src.features.auth.models.role_permission_model import role_permissions
from src.features.auth.models.user_role_model import UserRoles


class Role(AuditBase):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    users = relationship("User", secondary=UserRoles, back_populates="roles", lazy="selectin")
    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin"
    )
