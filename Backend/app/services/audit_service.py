from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def record(
    db: Session,
    *,
    actor_id: object | None,
    action: str,
    entity_type: str,
    entity_id: object,
    ip_address: str | None = None,
    user_agent: str | None = None,
    before_state: str | None = None,
    after_state: str | None = None,
) -> AuditLog:
    """Record an administrative or security event.

    The caller controls the transaction boundary; this function only stages
    the record via ``db.add`` so it commits atomically with the change it
    describes.
    """
    entry = AuditLog(
        actor_id=actor_id,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        ip_address=ip_address,
        user_agent=user_agent,
        before_state=before_state,
        after_state=after_state,
    )
    db.add(entry)
    return entry