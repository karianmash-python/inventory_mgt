from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from src.core.database.base_audit import AuditBase
from src.features.auth.models.user_role_model import UserRoles


class User(AuditBase):
    __tablename__ = "users"  # Optionally, explicit is better if your naming differs

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)

    roles = relationship("Role", secondary=UserRoles, back_populates="users", lazy="selectin")
