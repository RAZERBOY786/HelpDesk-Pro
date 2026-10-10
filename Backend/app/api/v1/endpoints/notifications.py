from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.db.session import get_db
from app.dependencies import require_active_user
from app.models.user import User
from app.repositories.notification_repository import NotificationRepository
from app.schemas.common import Message
from app.schemas.notification import NotificationRead
from app.utils.pagination import paginate

router = APIRouter(prefix="/notifications", tags=["Notifications"])


@router.get("", response_model=list[NotificationRead])
def list_notifications(
    unread_only: bool = False,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    stmt = NotificationRepository(db).list_for_user(user.id, unread_only=unread_only)
    rows, _ = paginate(db, stmt, page=page, page_size=page_size)
    return rows


@router.patch("/{notification_id}/read", response_model=NotificationRead)
def mark_read(
    notification_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    repo = NotificationRepository(db)
    notification = repo.get(notification_id)
    if notification is None or notification.user_id != user.id:
        raise NotFoundError("NOTIFICATION_NOT_FOUND", "The requested notification was not found.")
    repo.mark_read(notification)
    db.commit()
    db.refresh(notification)
    return notification


@router.post("/read-all", response_model=Message)
def mark_all_read(
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    NotificationRepository(db).mark_all_read(user.id)
    db.commit()
    return Message(message="All notifications marked as read.")