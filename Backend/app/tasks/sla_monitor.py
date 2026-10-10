"""SLA deadline monitoring task."""

from __future__ import annotations

from app.core.logging import get_logger
from app.services import sla_service

logger = get_logger("app.tasks.sla_monitor")


def run_once() -> dict[str, list[str]]:
    """Scan open tickets for approaching or breached SLA deadlines.

    Idempotent: relies on the unique (ticket_id, event_type, deadline_at)
    constraint so repeated runs do not duplicate events.
    """
    from app.db.session import SessionLocal

    db = SessionLocal()
    try:
        result = sla_service.scan_ticket_deadlines(db)
        if result["warnings"] or result["breaches"]:
            logger.info(
                "SLA scan: %d warning(s), %d breach(es)",
                len(result["warnings"]),
                len(result["breaches"]),
            )
        return result
    finally:
        db.close()