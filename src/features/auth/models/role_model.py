from sqlalchemy import Column, String, Text

from src.core.database.base_audit import AuditBase


class Role(AuditBase):
    __tablename__ = "roles"

    name = Column(String(50), unique=True, nullable=False)
    description = Column(Text, nullable=True)
