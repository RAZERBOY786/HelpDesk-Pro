from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TicketCategory, TicketPriority, TicketStatus


class TicketBase(BaseModel):
    title: str = Field(min_length=5, max_length=160)
    description: str = Field(min_length=10, max_length=10000)
    category: TicketCategory = TicketCategory.SOFTWARE
    priority: TicketPriority = TicketPriority.MEDIUM
    asset_id: UUID | None = None


class TicketCreate(TicketBase):
    pass


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=5, max_length=160)
    description: str | None = Field(default=None, min_length=10, max_length=10000)
    category: TicketCategory | None = None
    priority: TicketPriority | None = None
    asset_id: UUID | None = None


class TicketRead(BaseModel):
    id: UUID
    ticket_number: str
    title: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    created_by_id: UUID
    assigned_to_id: UUID | None
    asset_id: UUID | None
    created_at: datetime
    first_response_at: datetime | None
    resolved_at: datetime | None
    closed_at: datetime | None
    reopened_at: datetime | None
    updated_at: datetime
    response_due_at: datetime | None
    resolution_due_at: datetime | None
    resolution_summary: str | None
    sequence: int

    model_config = ConfigDict(from_attributes=True)


class TicketAssign(BaseModel):
    assigned_to_id: UUID
    note: str | None = Field(default=None, max_length=500)


class TicketResolve(BaseModel):
    resolution_summary: str = Field(min_length=10, max_length=5000)
    note: str | None = Field(default=None, max_length=500)


class TicketClose(BaseModel):
    note: str | None = Field(default=None, max_length=500)


class TicketReopen(BaseModel):
    note: str | None = Field(default=None, max_length=500)