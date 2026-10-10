from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class AttachmentRead(BaseModel):
    id: UUID
    ticket_id: UUID
    uploaded_by_id: UUID
    original_name: str
    content_type: str
    size_bytes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)