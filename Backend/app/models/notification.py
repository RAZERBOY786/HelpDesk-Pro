"""Notifications."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import NotificationType
from app.models.user import utcnow


class Notification(Base):
    __tablename__ = "notifications"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    ticket_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=True
    )
    type: Mapped[NotificationType] = mapped_column(
        SAEnum(
            NotificationType,
            name="notificationtype",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=NotificationType.INFO,
        nullable=False,
    )
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User")
    ticket = relationship("Ticket", back_populates="notifications")