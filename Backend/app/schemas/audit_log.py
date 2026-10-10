from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AuditLogRead(BaseModel):
    id: UUID
    actor_id: UUID | None
    action: str
    entity_type: str
    entity_id: str
    ip_address: str | None
    user_agent: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)