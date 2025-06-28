from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from src.core.database.base_audit import AuditBase


class User(AuditBase):
    __tablename__ = "users"  # Optionally, explicit is better if your naming differs

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)

    user_roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    roles = association_proxy("user_roles", "role")
