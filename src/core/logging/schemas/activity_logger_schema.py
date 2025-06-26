from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ActivityLogDTO(BaseModel):
    id: UUID
    user_id: Optional[UUID]
    action: str
    resource_type: str
    resource_id: Optional[UUID]
    timestamp: datetime
    metadata: Optional[dict]

    class Config:
        orm_mode = True
