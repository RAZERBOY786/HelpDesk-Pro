"""Public comments, internal notes, and ticket history."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import CommentVisibility, HistoryEventType
from app.models.user import utcnow


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    ticket_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tickets.id", ondelete="CASCADE"), index=True, nullable=False
    )
    author_id: Mapped[uuid.UUID] = mapped_column(Uuid, ForeignKey("users.id"), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    visibility: Mapped[CommentVisibility] = mapped_column(
        SAEnum(
            CommentVisibility,
            name="commentvisibility",
            native_enum=False,
            length=16,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=CommentVisibility.PUBLIC,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    ticket = relationship("Ticket", back_populates="comments")
    author = relationship("User")


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    ticket_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("tickets.id", ondelete="CASCADE"), index=True, nullable=False
    )
    actor_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, ForeignKey("users.id"), nullable=True)
    event_type: Mapped[HistoryEventType] = mapped_column(
        SAEnum(
            HistoryEventType,
            name="historyeventtype",
            native_enum=False,
            length=32,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
    )
    old_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    new_value: Mapped[str | None] = mapped_column(String(255), nullable=True)
    note: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    ticket = relationship("Ticket", back_populates="history")
    actor = relationship("User")