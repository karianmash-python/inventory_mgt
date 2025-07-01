from sqlalchemy import Column, ForeignKey, Table

from src.core.database.config import Base

UserRoles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)
