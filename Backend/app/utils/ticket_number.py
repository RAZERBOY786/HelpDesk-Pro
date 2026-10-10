from __future__ import annotations

from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket


def generate_ticket_number(db: Session, *, when: datetime | None = None) -> str:
    """Generate a unique human-readable ticket number ``HD-YYYY-NNNN``.

    Uses the current row count for the year. Callers must hold the ticket
    insert within the same transaction and retry on unique-constraint errors
    under high concurrency.
    """
    year = (when or datetime.utcnow()).year
    prefix = f"HD-{year}-"
    count = db.execute(
        select(func.count()).select_from(Ticket).where(Ticket.ticket_number.like(f"{prefix}%"))
    ).scalar_one()
    return f"{prefix}{count + 1:04d}"