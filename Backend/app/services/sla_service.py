"""SLA policy resolution, deadline calculation, and breach monitoring."""

from __future__ import annotations

from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.enums import SLAEventType, TicketPriority, TicketStatus
from app.models.sla import SLAEvent
from app.models.ticket import Ticket
from app.utils.datetime_utils import ensure_utc, utcnow

DEFAULT_SLA_MINUTES: dict[TicketPriority, tuple[int, int]] = {
    TicketPriority.LOW: (480, 2880),
    TicketPriority.MEDIUM: (240, 1440),
    TicketPriority.HIGH: (60, 480),
    TicketPriority.CRITICAL: (15, 60),
}

WARN_THRESHOLD_MINUTES = 30

OPEN_STATUSES = (
    TicketStatus.OPEN,
    TicketStatus.ASSIGNED,
    TicketStatus.IN_PROGRESS,
    TicketStatus.PENDING,
    TicketStatus.REOPENED,
)


def get_policy_for_priority(db: Session, priority: TicketPriority) -> tuple[int, int]:
    """Return ``(response_minutes, resolution_minutes)`` for a priority."""
    from app.models.sla import SLAPolicy

    policy = db.execute(
        select(SLAPolicy).where(
            SLAPolicy.priority == priority,
            SLAPolicy.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if policy is not None:
        return policy.response_minutes, policy.resolution_minutes
    return DEFAULT_SLA_MINUTES.get(priority, (240, 1440))


def calculate_deadlines(
    base: datetime,
    *,
    response_minutes: int,
    resolution_minutes: int,
) -> tuple[datetime, datetime]:
    return (
        base + timedelta(minutes=response_minutes),
        base + timedelta(minutes=resolution_minutes),
    )


def record_event(
    db: Session,
    *,
    ticket_id,
    event_type: SLAEventType,
    deadline_at: datetime,
) -> SLAEvent | None:
    """Idempotently record an SLA event.

    Returns ``None`` when an equivalent (ticket, type, deadline) event already
    exists, so scheduled jobs can safely run repeatedly.
    """
    existing = db.execute(
        select(SLAEvent).where(
            SLAEvent.ticket_id == ticket_id,
            SLAEvent.event_type == event_type,
            SLAEvent.deadline_at == deadline_at,
        )
    ).scalar_one_or_none()
    if existing is not None:
        return None

    event = SLAEvent(ticket_id=ticket_id, event_type=event_type, deadline_at=deadline_at)
    db.add(event)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        return None
    return event


def scan_ticket_deadlines(db: Session, *, now: datetime | None = None) -> dict[str, list[str]]:
    """Warn on approaching deadlines and record breaches for overdue tickets.

    Designed to be called by the scheduler; safe to run every minute.
    """
    now = now or utcnow()
    warn_threshold = now + timedelta(minutes=WARN_THRESHOLD_MINUTES)

    tickets = db.query(Ticket).filter(Ticket.status.in_(OPEN_STATUSES)).all()

    warnings: list[str] = []
    breaches: list[str] = []

    for ticket in tickets:
        if ticket.response_due_at is not None and ticket.first_response_at is None:
            event = _evaluate(
                db,
                ticket,
                due_at=ticket.response_due_at,
                now=now,
                warn_threshold=warn_threshold,
            )
            _classify(event, ticket.ticket_number, warnings, breaches)

        if ticket.resolved_at is None and ticket.resolution_due_at is not None:
            event = _evaluate(
                db,
                ticket,
                due_at=ticket.resolution_due_at,
                now=now,
                warn_threshold=warn_threshold,
            )
            _classify(event, ticket.ticket_number, warnings, breaches)

    if warnings or breaches:
        db.commit()

    return {"warnings": warnings, "breaches": breaches}


def _evaluate(db, ticket, *, due_at, now, warn_threshold):
    due_at = ensure_utc(due_at)
    now = ensure_utc(now)
    warn_threshold = ensure_utc(warn_threshold)
    if now >= due_at:
        return record_event(
            db, ticket_id=ticket.id, event_type=SLAEventType.BREACH, deadline_at=due_at
        )
    if due_at <= warn_threshold:
        return record_event(
            db, ticket_id=ticket.id, event_type=SLAEventType.WARNING, deadline_at=due_at
        )
    return None


def _classify(event: SLAEvent | None, ticket_number: str, warnings: list, breaches: list) -> None:
    if event is None:
        return
    if event.event_type == SLAEventType.BREACH:
        breaches.append(ticket_number)
    else:
        warnings.append(ticket_number)


def is_overdue(ticket: Ticket, *, now: datetime | None = None) -> bool:
    now = ensure_utc(now) or utcnow()
    if ticket.resolved_at is not None:
        return False
    due = ensure_utc(ticket.resolution_due_at)
    return due is not None and due < now