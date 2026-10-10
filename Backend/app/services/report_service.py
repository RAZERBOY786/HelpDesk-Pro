"""Report calculations."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.enums import TicketStatus, UserRole
from app.models.sla import SLAEvent
from app.models.ticket import Ticket
from app.models.user import User


def _status_counts(db: Session) -> dict[str, int]:
    rows = db.execute(
        select(Ticket.status, func.count()).group_by(Ticket.status)
    ).all()
    return {status.value: count for status, count in rows}


def _priority_counts(db: Session) -> dict[str, int]:
    rows = db.execute(
        select(Ticket.priority, func.count()).group_by(Ticket.priority)
    ).all()
    return {priority.value: count for priority, count in rows}


def _category_counts(db: Session) -> dict[str, int]:
    rows = db.execute(
        select(Ticket.category, func.count()).group_by(Ticket.category)
    ).all()
    return {category.value: count for category, count in rows}


def overview(db: Session) -> dict:
    statuses = _status_counts(db)
    breached = db.execute(
        select(func.count(func.distinct(SLAEvent.ticket_id))).where(
            SLAEvent.event_type == "breach"
        )
    ).scalar_one()
    unassigned = db.execute(
        select(func.count()).select_from(Ticket).where(Ticket.assigned_to_id.is_(None))
    ).scalar_one()
    technicians = db.execute(
        select(func.count()).select_from(User).where(User.role == UserRole.TECHNICIAN)
    ).scalar_one()
    assets = db.execute(select(func.count()).select_from(Asset)).scalar_one()

    return {
        "open_tickets": statuses.get(TicketStatus.OPEN.value, 0)
        + statuses.get(TicketStatus.REOPENED.value, 0),
        "in_progress_tickets": statuses.get(TicketStatus.IN_PROGRESS.value, 0)
        + statuses.get(TicketStatus.ASSIGNED.value, 0)
        + statuses.get(TicketStatus.PENDING.value, 0),
        "resolved_tickets": statuses.get(TicketStatus.RESOLVED.value, 0),
        "closed_tickets": statuses.get(TicketStatus.CLOSED.value, 0),
        "sla_breached": int(breached),
        "unassigned_tickets": int(unassigned),
        "technicians": int(technicians),
        "assets": int(assets),
    }


def ticket_metrics(db: Session) -> dict:
    total = db.execute(select(func.count()).select_from(Ticket)).scalar_one()
    return {
        "total": int(total),
        "by_status": _status_counts(db),
        "by_priority": _priority_counts(db),
        "by_category": _category_counts(db),
    }


def technician_metrics(db: Session) -> list[dict]:
    technicians = db.execute(
        select(User).where(User.role == UserRole.TECHNICIAN)
    ).scalars().all()

    results: list[dict] = []
    for tech in technicians:
        assigned = db.execute(
            select(func.count()).select_from(Ticket).where(Ticket.assigned_to_id == tech.id)
        ).scalar_one()
        resolved = db.execute(
            select(func.count())
            .select_from(Ticket)
            .where(Ticket.assigned_to_id == tech.id, Ticket.resolved_at.is_not(None))
        ).scalar_one()
        overdue = db.execute(
            select(func.count())
            .select_from(Ticket)
            .where(
                Ticket.assigned_to_id == tech.id,
                Ticket.resolved_at.is_(None),
                Ticket.resolution_due_at < func.now(),
            )
        ).scalar_one()

        avg_hours = None
        durations = db.execute(
            select(Ticket.created_at, Ticket.resolved_at).where(
                Ticket.assigned_to_id == tech.id, Ticket.resolved_at.is_not(None)
            )
        ).all()
        if durations:
            total_hours = sum(
                (resolved_at - created_at).total_seconds() / 3600 for created_at, resolved_at in durations
            )
            avg_hours = round(total_hours / len(durations), 2)

        results.append(
            {
                "technician_id": str(tech.id),
                "technician_name": tech.name,
                "assigned": int(assigned),
                "resolved": int(resolved),
                "overdue": int(overdue),
                "average_resolution_hours": avg_hours,
            }
        )
    return results


def sla_metrics(db: Session) -> dict:
    breached = db.execute(
        select(func.count(func.distinct(SLAEvent.ticket_id))).where(
            SLAEvent.event_type == "breach"
        )
    ).scalar_one()
    total = db.execute(select(func.count()).select_from(Ticket)).scalar_one()
    total = int(total)
    return {
        "total_tickets": total,
        "breached_tickets": int(breached),
        "compliance_rate": round((1 - breached / total) * 100, 2) if total else 100.0,
    }