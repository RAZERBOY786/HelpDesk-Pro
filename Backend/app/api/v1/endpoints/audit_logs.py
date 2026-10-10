from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import require_roles
from app.models.audit_log import AuditLog
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.audit_log import AuditLogRead
from app.utils.pagination import paginate

router = APIRouter(prefix="/admin", tags=["Audit Logs"])


@router.get("/audit-logs", response_model=list[AuditLogRead])
def list_audit_logs(
    action: str | None = None,
    entity_type: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    _admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    stmt = select(AuditLog)
    if action:
        stmt = stmt.where(AuditLog.action == action)
    if entity_type:
        stmt = stmt.where(AuditLog.entity_type == entity_type)
    stmt = stmt.order_by(AuditLog.created_at.desc())
    rows, _ = paginate(db, stmt, page=page, page_size=page_size)
    return rows