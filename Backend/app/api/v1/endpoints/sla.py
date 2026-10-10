from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.db.session import get_db
from app.dependencies import require_active_user, require_roles
from app.models.enums import UserRole
from app.models.sla import SLAPolicy
from app.models.user import User
from app.schemas.sla import SLAPolicyCreate, SLAPolicyRead, SLAPolicyUpdate
from app.services import audit_service

router = APIRouter(prefix="/sla", tags=["SLA"])


@router.get("/policies", response_model=list[SLAPolicyRead])
def list_policies(
    _user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    return list(db.execute(select(SLAPolicy).order_by(SLAPolicy.priority)).scalars())


@router.post("/policies", response_model=SLAPolicyRead, status_code=201)
def create_policy(
    payload: SLAPolicyCreate,
    admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    existing = db.execute(
        select(SLAPolicy).where(SLAPolicy.priority == payload.priority)
    ).scalar_one_or_none()
    if existing is not None:
        raise ConflictError("POLICY_EXISTS", "An SLA policy for this priority already exists.")

    policy = SLAPolicy(**payload.model_dump())
    db.add(policy)
    audit_service.record(
        db,
        actor_id=admin.id,
        action="sla.policy_created",
        entity_type="sla_policy",
        entity_id=str(policy.id),
    )
    db.commit()
    db.refresh(policy)
    return policy


@router.post("/scan")
def run_sla_scan(
    _admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    """Manually trigger the SLA monitor (idempotent)."""
    from app.services import sla_service

    return sla_service.scan_ticket_deadlines(db)


@router.patch("/policies/{policy_id}", response_model=SLAPolicyRead)
def update_policy(
    policy_id: uuid.UUID,
    payload: SLAPolicyUpdate,
    admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    policy = db.get(SLAPolicy, policy_id)
    if policy is None:
        raise NotFoundError("POLICY_NOT_FOUND", "The requested SLA policy was not found.")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(policy, field, value)
    audit_service.record(
        db,
        actor_id=admin.id,
        action="sla.policy_updated",
        entity_type="sla_policy",
        entity_id=str(policy.id),
    )
    db.commit()
    db.refresh(policy)
    return policy