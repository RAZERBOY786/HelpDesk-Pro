"""SLA policies and SLA breach/compliance events."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import SLAEventType, TicketPriority
from app.models.user import utcnow


class SLAPolicy(Base):
    __tablename__ = "sla_policies"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    priority: Mapped[TicketPriority] = mapped_column(
        SAEnum(
            TicketPriority,
            name="ticketpriority",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        unique=True,
        nullable=False,
    )
    response_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    resolution_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )


class SLAEvent(Base):
    __tablename__ = "sla_events"
    __table_args__ = (
        # Deduplication key: one event per ticket per (type, deadline).
        __import__("sqlalchemy").UniqueConstraint(
            "ticket_id",
            "event_type",
            "deadline_at",
            name="uq_sla_events_ticket_type_deadline",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    ticket_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tickets.id", ondelete="CASCADE"), index=True, nullable=False
    )
    event_type: Mapped[SLAEventType] = mapped_column(
        SAEnum(
            SLAEventType,
            name="slaeventtype",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    )
    deadline_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    ticket = relationship("Ticket", back_populates="sla_events")