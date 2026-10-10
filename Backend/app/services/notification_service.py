"""Notification creation (in-app) and email dispatch.

Notifications are recorded durably in the database. Email delivery is treated
as best-effort after the database transaction commits.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.enums import NotificationType, UserRole
from app.models.notification import Notification
from app.models.ticket import Ticket
from app.models.user import User
from app.services import email_service

TICKET_CREATED = "ticket_created"
TICKET_ASSIGNED = "ticket_assigned"
NEW_COMMENT = "new_comment"
STATUS_CHANGED = "status_changed"
SLA_WARNING = "sla_warning"
SLA_BREACH = "sla_breach"
TICKET_RESOLVED = "ticket_resolved"
TICKET_REOPENED = "ticket_reopened"


def create(
    db: Session,
    *,
    user_id: UUID,
    message: str,
    ticket_id: UUID | None = None,
    type: NotificationType = NotificationType.INFO,
) -> Notification:
    notification = Notification(
        user_id=user_id,
        ticket_id=ticket_id,
        type=type,
        message=message,
    )
    db.add(notification)
    return notification


def notify_user(
    db: Session,
    *,
    user_id: UUID,
    message: str,
    ticket_id: UUID | None = None,
    type: NotificationType = NotificationType.INFO,
    email_to: str | None = None,
) -> None:
    create(db, user_id=user_id, message=message, ticket_id=ticket_id, type=type)
    if email_to:
        email_service.send_email(to=email_to, subject="HelpDesk Pro notification", body=message)


def _notify_role(db: Session, role: UserRole, message: str, ticket_id: UUID | None) -> None:
    users = (
        db.query(User)
        .filter(User.role == role, User.is_active.is_(True))
        .all()
    )
    for user in users:
        create(db, user_id=user.id, message=message, ticket_id=ticket_id)


def notify_technicians(db: Session, *, message: str, ticket_id: UUID | None = None) -> None:
    _notify_role(db, UserRole.TECHNICIAN, message, ticket_id)


def notify_admins(db: Session, *, message: str, ticket_id: UUID | None = None) -> None:
    _notify_role(db, UserRole.ADMIN, message, ticket_id)


def ticket_created(db: Session, ticket: Ticket) -> None:
    notify_technicians(
        db,
        message=f"New ticket {ticket.ticket_number} created: {ticket.title}",
        ticket_id=ticket.id,
    )
    notify_user(
        db,
        user_id=ticket.created_by_id,
        message=f"Your ticket {ticket.ticket_number} has been received.",
        ticket_id=ticket.id,
    )


def ticket_assigned(db: Session, ticket: Ticket, technician: User) -> None:
    notify_user(
        db,
        user_id=technician.id,
        message=f"You were assigned ticket {ticket.ticket_number}: {ticket.title}",
        ticket_id=ticket.id,
        email_to=technician.email,
    )


def status_changed(db: Session, ticket: Ticket, *, new_status: str) -> None:
    notify_user(
        db,
        user_id=ticket.created_by_id,
        message=f"Ticket {ticket.ticket_number} is now {new_status}.",
        ticket_id=ticket.id,
    )