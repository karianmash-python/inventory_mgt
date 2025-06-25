from sqlalchemy.orm import Session
from datetime import datetime, timezone

from src.features.auth.models import UserLoginHistory
from src.features.auth.models import User


def record_login_event(db: Session, user: User):
    login_event = UserLoginHistory(user_id=user.id)
    user.last_login = datetime.now(timezone.utc)
    db.add(login_event)
    db.commit()
