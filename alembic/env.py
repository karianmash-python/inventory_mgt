# 👇 ADD THIS
from src.core.database.config import Base

from src.features.auth.models.user_model import User
from src.features.organizations.models.organization_model import Organization
from src.core.logging.models.activity_log_model import ActivityLog

target_metadata = Base.metadata
