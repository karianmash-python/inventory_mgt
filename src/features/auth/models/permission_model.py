from sqlalchemy import Column, String, Text

from src.core.database.base_audit import AuditBase


class Permission(AuditBase):
    __tablename__ = "permissions"

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
