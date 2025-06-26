from sqlalchemy.orm import Session
from uuid import UUID
from typing import Optional
from src.core.logging.models.activity_log_model import ActivityLog


def log_activity(
        db: Session,
        user_id: Optional[UUID],
        action: str,
        resource_type: str,
        resource_id: Optional[UUID] = None,
        metadata: Optional[dict] = None
):
    log = ActivityLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        metadata=metadata or {}
    )
    db.add(log)
    db.commit()
