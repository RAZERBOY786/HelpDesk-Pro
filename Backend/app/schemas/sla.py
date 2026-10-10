from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import SLAEventType, TicketPriority


class SLAPolicyBase(BaseModel):
    priority: TicketPriority
    response_minutes: int = Field(ge=1)
    resolution_minutes: int = Field(ge=1)
    is_active: bool = True


class SLAPolicyCreate(SLAPolicyBase):
    pass


class SLAPolicyUpdate(BaseModel):
    response_minutes: int | None = Field(default=None, ge=1)
    resolution_minutes: int | None = Field(default=None, ge=1)
    is_active: bool | None = None


class SLAPolicyRead(SLAPolicyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SLAEventRead(BaseModel):
    id: UUID
    ticket_id: UUID
    event_type: SLAEventType
    deadline_at: datetime
    recorded_at: datetime

    model_config = ConfigDict(from_attributes=True)