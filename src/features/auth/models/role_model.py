from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.core.database.base_audit import AuditBase


class Role(AuditBase):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    user_roles = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")

    permissions = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin"
    )
