"""Ticket lifecycle, assignment, resolution, comments, and history."""

from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, ForbiddenError, NotFoundError, ValidationError
from app.models.comment import Comment, TicketHistory
from app.models.enums import (
    CommentVisibility,
    HistoryEventType,
    SLAEventType,
    TicketPriority,
    TicketStatus,
    UserRole,
)
from app.models.ticket import Ticket
from app.models.user import User
from app.services import audit_service, notification_service, sla_service
from app.utils.ticket_number import generate_ticket_number

TRANSITIONS: dict[TicketStatus, set[TicketStatus]] = {
    TicketStatus.OPEN: {TicketStatus.ASSIGNED},
    TicketStatus.ASSIGNED: {
        TicketStatus.IN_PROGRESS,
        TicketStatus.OPEN,
        TicketStatus.RESOLVED,
    },
    TicketStatus.IN_PROGRESS: {TicketStatus.PENDING, TicketStatus.RESOLVED},
    TicketStatus.PENDING: {TicketStatus.IN_PROGRESS, TicketStatus.ASSIGNED},
    TicketStatus.RESOLVED: {TicketStatus.CLOSED, TicketStatus.REOPENED},
    TicketStatus.CLOSED: {TicketStatus.REOPENED},
    TicketStatus.REOPENED: {TicketStatus.ASSIGNED, TicketStatus.IN_PROGRESS},
}


def _now() -> datetime:
    return datetime.now(timezone.utc)


# --------------------------------------------------------------------------- access


def can_view(user: User, ticket: Ticket) -> bool:
    if user.role in (UserRole.ADMIN, UserRole.TECHNICIAN):
        return True
    return ticket.created_by_id == user.id


def can_assign(user: User, ticket: Ticket) -> bool:
    return user.role in (UserRole.ADMIN, UserRole.TECHNICIAN)


def can_resolve(user: User, ticket: Ticket) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    return user.role == UserRole.TECHNICIAN and ticket.assigned_to_id == user.id


def can_close(user: User, ticket: Ticket) -> bool:
    if user.role == UserRole.ADMIN:
        return True
    if user.role == UserRole.TECHNICIAN and ticket.assigned_to_id == user.id:
        return True
    return ticket.created_by_id == user.id


def can_reopen(user: User, ticket: Ticket) -> bool:
    return can_close(user, ticket)


# --------------------------------------------------------------------------- helpers


def _record_history(
    db: Session,
    ticket: Ticket,
    *,
    actor_id,
    event_type: HistoryEventType,
    old_value: str | None = None,
    new_value: str | None = None,
    note: str | None = None,
) -> TicketHistory:
    entry = TicketHistory(
        ticket_id=ticket.id,
        actor_id=actor_id,
        event_type=event_type,
        old_value=old_value,
        new_value=new_value,
        note=note,
    )
    db.add(entry)
    return entry


def get_ticket(db: Session, ticket_id, *, user: User | None = None) -> Ticket:
    ticket = db.execute(select(Ticket).where(Ticket.id == ticket_id)).scalar_one_or_none()
    if ticket is None:
        raise NotFoundError("TICKET_NOT_FOUND", "The requested ticket was not found.")
    if user is not None and not can_view(user, ticket):
        raise NotFoundError("TICKET_NOT_FOUND", "The requested ticket was not found.")
    return ticket


# --------------------------------------------------------------------------- create


def create_ticket(db: Session, *, creator: User, data) -> Ticket:
    asset_id = getattr(data, "asset_id", None)
    if asset_id is not None:
        from app.models.asset import Asset

        asset = db.get(Asset, asset_id)
        if asset is None:
            raise ValidationError("ASSET_NOT_FOUND", "The referenced asset does not exist.")
        if not (creator.role in (UserRole.ADMIN, UserRole.TECHNICIAN)) and asset.assigned_user_id not in (
            None,
            creator.id,
        ):
            raise ForbiddenError("ASSET_FORBIDDEN", "You cannot reference this asset.")

    response_minutes, resolution_minutes = sla_service.get_policy_for_priority(db, data.priority)
    now = _now()

    ticket = Ticket(
        title=data.title,
        description=data.description,
        category=data.category,
        priority=data.priority,
        status=TicketStatus.OPEN,
        created_by_id=creator.id,
        asset_id=asset_id,
        created_at=now,
    )

    for attempt in range(5):
        ticket.ticket_number = generate_ticket_number(db, when=now)
        db.add(ticket)
        try:
            db.flush()
            break
        except IntegrityError:
            db.rollback()
            continue
    else:
        raise ConflictError("TICKET_NUMBER_CONFLICT", "Could not allocate a ticket number.")

    (
        ticket.response_due_at,
        ticket.resolution_due_at,
    ) = sla_service.calculate_deadlines(
        now,
        response_minutes=response_minutes,
        resolution_minutes=resolution_minutes,
    )

    db.add(
        TicketHistory(
            ticket_id=ticket.id,
            actor_id=creator.id,
            event_type=HistoryEventType.CREATED,
            new_value=data.title,
        )
    )
    notification_service.ticket_created(db, ticket)
    audit_service.record(
        db,
        actor_id=creator.id,
        action="ticket.created",
        entity_type="ticket",
        entity_id=str(ticket.id),
    )
    db.commit()
    db.refresh(ticket)
    return ticket


# --------------------------------------------------------------------------- update


def update_ticket(db: Session, *, actor: User, ticket: Ticket, data: dict) -> Ticket:
    allowed = {"title", "description", "category", "asset_id"}
    if actor.role in (UserRole.ADMIN, UserRole.TECHNICIAN):
        allowed.add("priority")

    for field, value in data.items():
        if value is None or field not in allowed:
            continue
        old = getattr(ticket, field)
        if old == value:
            continue
        setattr(ticket, field, value)
        history_type = (
            HistoryEventType.PRIORITY_CHANGED
            if field == "priority"
            else HistoryEventType.EDITED
        )
        _add_history(db, ticket, actor.id, history_type, str(old), str(value))

    audit_service.record(
        db,
        actor_id=actor.id,
        action="ticket.updated",
        entity_type="ticket",
        entity_id=str(ticket.id),
    )
    db.commit()
    db.refresh(ticket)
    return ticket


# --------------------------------------------------------------------------- assignment


def assign_ticket(db: Session, *, actor: User, ticket: Ticket, technician_id, note: str | None = None) -> Ticket:
    technician = db.get(User, technician_id)
    if technician is None:
        raise NotFoundError("USER_NOT_FOUND", "The technician was not found.")
    if technician.role not in (UserRole.TECHNICIAN, UserRole.ADMIN):
        raise ValidationError("NOT_A_TECHNICIAN", "Tickets can only be assigned to technicians.")
    if not technician.is_active:
        raise ValidationError("INACTIVE_USER", "This technician is not active.")

    old_assignee = ticket.assigned_to_id
    ticket.assigned_to_id = technician.id

    if ticket.status in (TicketStatus.OPEN, TicketStatus.REOPENED):
        _transition(db, ticket, TicketStatus.ASSIGNED, actor, note=None)

    _add_history(
        db,
        ticket,
        actor.id,
        HistoryEventType.ASSIGNED,
        str(old_assignee) if old_assignee else None,
        str(technician.id),
        note,
    )
    notification_service.ticket_assigned(db, ticket, technician)
    audit_service.record(
        db,
        actor_id=actor.id,
        action="ticket.assigned",
        entity_type="ticket",
        entity_id=str(ticket.id),
        after_state=str(technician.id),
    )
    db.commit()
    db.refresh(ticket)
    return ticket


def unassign_ticket(db: Session, *, actor: User, ticket: Ticket) -> Ticket:
    ticket.assigned_to_id = None
    if ticket.status == TicketStatus.ASSIGNED:
        _transition(db, ticket, TicketStatus.OPEN, actor)
    _add_history(db, ticket, actor.id, HistoryEventType.UNASSIGNED, None, None)
    db.commit()
    db.refresh(ticket)
    return ticket


# --------------------------------------------------------------------------- lifecycle


def resolve_ticket(db: Session, *, actor: User, ticket: Ticket, resolution_summary: str, note: str | None = None) -> Ticket:
    if not can_resolve(actor, ticket):
        raise ForbiddenError("RESOLVE_FORBIDDEN", "You cannot resolve this ticket.")
    if ticket.status not in (TicketStatus.IN_PROGRESS, TicketStatus.PENDING, TicketStatus.ASSIGNED):
        raise ConflictError("INVALID_TRANSITION", f"Cannot resolve a ticket in status '{ticket.status.value}'.")

    ticket.resolution_summary = resolution_summary
    ticket.resolved_at = _now()
    _transition(db, ticket, TicketStatus.RESOLVED, actor, note=resolution_summary)
    _add_history(
        db,
        ticket,
        actor.id,
        HistoryEventType.RESOLVED,
        note=resolution_summary,
    )

    sla_service.record_event(
        db,
        ticket_id=ticket.id,
        event_type=SLAEventType.COMPLIED,
        deadline_at=ticket.resolution_due_at or ticket.resolved_at,
    )
    audit_service.record(
        db,
        actor_id=actor.id,
        action="ticket.resolved",
        entity_type="ticket",
        entity_id=str(ticket.id),
    )
    db.commit()
    db.refresh(ticket)
    return ticket


def close_ticket(db: Session, *, actor: User, ticket: Ticket, note: str | None = None) -> Ticket:
    if ticket.status != TicketStatus.RESOLVED:
        raise ConflictError("INVALID_TRANSITION", "Only resolved tickets can be closed.")
    ticket.closed_at = _now()
    _transition(db, ticket, TicketStatus.CLOSED, actor, note=note)
    _add_history(db, ticket, actor.id, HistoryEventType.CLOSED, note=note)
    audit_service.record(
        db,
        actor_id=actor.id,
        action="ticket.closed",
        entity_type="ticket",
        entity_id=str(ticket.id),
    )
    db.commit()
    db.refresh(ticket)
    return ticket


def reopen_ticket(db: Session, *, actor: User, ticket: Ticket, note: str | None = None) -> Ticket:
    if ticket.status not in (TicketStatus.RESOLVED, TicketStatus.CLOSED):
        raise ConflictError("INVALID_TRANSITION", "Only resolved or closed tickets can be reopened.")
    ticket.reopened_at = _now()
    ticket.resolved_at = None
    _transition(db, ticket, TicketStatus.REOPENED, actor, note=note)
    _add_history(db, ticket, actor.id, HistoryEventType.REOPENED, note=note)
    notification_service.status_changed(db, ticket, new_status="reopened")
    audit_service.record(
        db,
        actor_id=actor.id,
        action="ticket.reopened",
        entity_type="ticket",
        entity_id=str(ticket.id),
    )
    db.commit()
    db.refresh(ticket)
    return ticket


def _transition(db: Session, ticket: Ticket, new_status: TicketStatus, actor: User, note: str | None) -> None:
    old = ticket.status
    if new_status not in TRANSITIONS.get(old, set()):
        raise ValidationError(
            "INVALID_TRANSITION",
            f"Cannot move ticket from '{old.value}' to '{new_status.value}'.",
        )
    ticket.status = new_status
    _add_history(
        db,
        ticket,
        actor.id,
        HistoryEventType.STATUS_CHANGED,
        old.value,
        new_status.value,
        note,
    )


def _add_history(db, ticket, actor_id, event_type, old_value=None, new_value=None, note=None):
    db.add(
        TicketHistory(
            ticket_id=ticket.id,
            actor_id=actor_id,
            event_type=event_type,
            old_value=old_value,
            new_value=new_value,
            note=note,
        )
    )


# --------------------------------------------------------------------------- comments


def add_comment(db: Session, *, author: User, ticket: Ticket, body: str, visibility) -> Comment:
    if visibility == CommentVisibility.INTERNAL and author.role == UserRole.EMPLOYEE:
        raise ForbiddenError("FORBIDDEN", "Only staff can post internal notes.")

    comment = Comment(
        ticket_id=ticket.id,
        author_id=author.id,
        body=body,
        visibility=visibility,
    )
    db.add(comment)

    # The first qualifying staff response satisfies the response SLA.
    if (
        author.role in (UserRole.TECHNICIAN, UserRole.ADMIN)
        and ticket.first_response_at is None
        and comment.visibility == CommentVisibility.PUBLIC
    ):
        ticket.first_response_at = _now()

    _add_history(db, ticket, author.id, HistoryEventType.COMMENT_ADDED, None, None)
    if comment.visibility == CommentVisibility.PUBLIC:
        notification_service.notify_user(
            db,
            user_id=ticket.created_by_id,
            message=f"New comment on ticket {ticket.ticket_number}.",
            ticket_id=ticket.id,
        )
    db.commit()
    db.refresh(comment)
    return comment


def get_history(db: Session, ticket: Ticket) -> list[TicketHistory]:
    return list(
        db.execute(
            select(TicketHistory)
            .where(TicketHistory.ticket_id == ticket.id)
            .order_by(TicketHistory.created_at.asc())
        ).scalars()
    )