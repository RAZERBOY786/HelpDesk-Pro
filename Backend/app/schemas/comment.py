from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.enums import CommentVisibility


class CommentCreate(BaseModel):
    body: str = Field(min_length=1, max_length=5000)
    visibility: CommentVisibility = CommentVisibility.PUBLIC


class CommentRead(BaseModel):
    id: UUID
    ticket_id: UUID
    author_id: UUID
    body: str
    visibility: CommentVisibility
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CommentUpdate(BaseModel):
    body: str = Field(min_length=1, max_length=5000)


class TicketHistoryRead(BaseModel):
    id: UUID
    ticket_id: UUID
    actor_id: UUID | None
    event_type: str
    old_value: str | None
    new_value: str | None
    note: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)