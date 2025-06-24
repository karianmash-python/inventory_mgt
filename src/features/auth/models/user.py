from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.core.database.base_audit import AuditBase


class User(AuditBase):
    __tablename__ = "users"  # Optionally, explicit is better if your naming differs

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
