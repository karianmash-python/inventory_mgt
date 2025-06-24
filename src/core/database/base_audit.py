import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declared_attr
from src.core.database.config import Base


class AuditBase(Base):
    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this base class

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc),
                      onupdate=lambda: datetime.now(timezone.utc))

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime(timezone=True), nullable=True)

    @declared_attr
    def created_by(cls):
        return Column(String, nullable=True)

    @declared_attr
    def modified_by(cls):
        return Column(String, nullable=True)
