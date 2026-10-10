from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.notification import Notification


class NotificationRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, notification_id: UUID) -> Notification | None:
        return self.db.get(Notification, notification_id)

    def list_for_user(self, user_id: UUID, *, unread_only: bool = False):
        stmt = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            stmt = stmt.where(Notification.is_read.is_(False))
        return stmt.order_by(Notification.created_at.desc())

    def count_unread(self, user_id: UUID) -> int:
        return self.db.execute(
            select(func.count())
            .select_from(Notification)
            .where(Notification.user_id == user_id, Notification.is_read.is_(False))
        ).scalar_one()

    def mark_read(self, notification: Notification) -> Notification:
        notification.is_read = True
        notification.read_at = datetime.now(timezone.utc)
        return notification

    def mark_all_read(self, user_id: UUID) -> int:
        now = datetime.now(timezone.utc)
        rows = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read.is_(False))
            .all()
        )
        for row in rows:
            row.is_read = True
            row.read_at = now
        return len(rows)

    def add(self, notification: Notification) -> Notification:
        self.db.add(notification)
        return notification