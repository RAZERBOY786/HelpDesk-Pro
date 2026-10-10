"""Tickets."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import TicketCategory, TicketPriority, TicketStatus
from app.models.user import utcnow


class Ticket(Base):
    __tablename__ = "tickets"
    __table_args__ = (
        UniqueConstraint("ticket_number", name="uq_tickets_ticket_number"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    ticket_number: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    category: Mapped[TicketCategory] = mapped_column(
        SAEnum(
            TicketCategory,
            name="ticketcategory",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=TicketCategory.SOFTWARE,
        nullable=False,
    )
    priority: Mapped[TicketPriority] = mapped_column(
        SAEnum(
            TicketPriority,
            name="ticketpriority",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=TicketPriority.MEDIUM,
        nullable=False,
        index=True,
    )
    status: Mapped[TicketStatus] = mapped_column(
        SAEnum(
            TicketStatus,
            name="ticketstatus",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=TicketStatus.OPEN,
        nullable=False,
        index=True,
    )

    created_by_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id"), index=True, nullable=False
    )
    assigned_to_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id"), index=True, nullable=True
    )
    asset_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("assets.id", ondelete="SET NULL"), nullable=True
    )
    sequence: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False, index=True)
    first_response_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    reopened_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    response_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    resolution_due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    resolution_summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    creator = relationship(
        "User", back_populates="created_tickets", foreign_keys=[created_by_id]
    )
    assignee = relationship(
        "User", back_populates="assigned_tickets", foreign_keys=[assigned_to_id]
    )
    asset = relationship("Asset", back_populates="tickets")
    comments = relationship(
        "Comment",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="Comment.created_at",
    )
    history = relationship(
        "TicketHistory",
        back_populates="ticket",
        cascade="all, delete-orphan",
        order_by="TicketHistory.created_at",
    )
    attachments = relationship(
        "Attachment",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )
    notifications = relationship("Notification", back_populates="ticket", cascade="all, delete-orphan")
    sla_events = relationship(
        "SLAEvent",
        back_populates="ticket",
        cascade="all, delete-orphan",
    )