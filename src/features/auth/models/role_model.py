from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from src.core.database.base_audit import AuditBase


class Role(AuditBase):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    permissions = relationship(
        "Permission",
        secondary="role_permissions",  # Matches __tablename__
        back_populates="roles",
        lazy="selectin"
    )
