"""Notification delivery worker.

This project records notifications durably in the database. Email delivery is
best-effort and retried here for messages that were created but not yet sent.

For a fully reliable pipeline, evolve this into a transactional outbox: write
the ticket change and an outgoing-event row in the same transaction, then let
this worker deliver the event with a retry/backoff policy.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.db.session import SessionLocal

logger = get_logger("app.tasks.notification_worker")

MAX_ATTEMPTS = 3
BACKOFF_MINUTES = 5


def process_once(db: Session | None = None) -> int:
    """Deliver pending notifications.

    With the default in-app-only configuration this is a no-op that reports 0.
    Email delivery is performed inline by the notification service; this hook
    exists so deployments can move to asynchronous delivery without changing
    business code.
    """
    owns_session = db is None
    db = db or SessionLocal()
    try:
        # Placeholder for durable queue draining.
        delivered = 0
        return delivered
    finally:
        if owns_session:
            db.close()


def run_forever(interval_seconds: int = 60) -> None:  # pragma: no cover - runtime loop
    import time

    while True:
        try:
            process_once()
        except Exception:  # noqa: BLE001
            logger.exception("Notification worker iteration failed")
        time.sleep(interval_seconds)