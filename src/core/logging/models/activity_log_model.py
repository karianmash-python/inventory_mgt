from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.core.database.base_audit import AuditBase


class ActivityLog(AuditBase):
    __tablename__ = "activity_logs"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String, nullable=False)  # e.g., 'create', 'update', 'delete'
    resource_type = Column(String, nullable=False)  # e.g., 'organization', 'user'
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    metadata = Column(JSON, nullable=True)

    user = relationship("User", backref="activity_logs")
