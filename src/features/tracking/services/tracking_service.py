from sqlalchemy.orm import Session
from uuid import UUID

from src.features.tracking.models.utm_event_model import UtmEvent
from src.core.middleware.utm_middleware import UtmParams


def track_event(
        db: Session,
        event_type: str,
        utm_params: UtmParams,
        user_id: UUID = None,
) -> UtmEvent:
    """
    Logs a UTM event to the database.
    """
    utm_event = UtmEvent(
        user_id=user_id,
        event_type=event_type,
        utm_source=utm_params.utm_source,
        utm_medium=utm_params.utm_medium,
        utm_campaign=utm_params.utm_campaign,
        utm_term=utm_params.utm_term,
        utm_content=utm_params.utm_content,
    )
    db.add(utm_event)
    db.commit()
    db.refresh(utm_event)
    return utm_event
