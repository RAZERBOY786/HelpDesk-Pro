from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import NotificationType


class NotificationRead(BaseModel):
    id: UUID
    user_id: UUID
    ticket_id: UUID | None
    type: NotificationType
    message: str
    is_read: bool
    read_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)