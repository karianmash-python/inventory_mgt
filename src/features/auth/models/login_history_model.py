from sqlalchemy import Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from src.core.database.base_audit import AuditBase
from sqlalchemy.dialects.postgresql import UUID


class UserLoginHistory(AuditBase):
    __tablename__ = "user_login_history"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    login_time = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    user = relationship("User", backref="login_events")
