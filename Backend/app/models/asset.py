"""Asset inventory."""

from __future__ import annotations

import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum as SAEnum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base
from app.models.enums import AssetStatus
from app.models.user import utcnow


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    asset_tag: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(128), unique=True, nullable=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    model: Mapped[str | None] = mapped_column(String(120), nullable=True)
    category: Mapped[str | None] = mapped_column(String(80), nullable=True)
    status: Mapped[AssetStatus] = mapped_column(
        SAEnum(
            AssetStatus,
            name="assetstatus",
            native_enum=False,
            length=24,
            values_callable=lambda e: [m.value for m in e],
        ),
        default=AssetStatus.AVAILABLE,
        nullable=False,
    )
    assigned_user_id: Mapped[uuid.UUID | None] = mapped_column(
        Uuid, ForeignKey("users.id"), index=True, nullable=True
    )
    warranty_expiry: Mapped[date | None] = mapped_column(Date, nullable=True)
    purchase_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False
    )

    assigned_user = relationship("User")
    tickets = relationship("Ticket", back_populates="asset")