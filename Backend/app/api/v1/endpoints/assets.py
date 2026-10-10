from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError
from app.db.session import get_db
from app.dependencies import require_active_user
from app.models.enums import AssetStatus, UserRole
from app.models.user import User
from app.schemas.asset import (
    AssetAssign,
    AssetCreate,
    AssetRead,
    AssetUpdate,
    MaintenanceRequest,
)
from app.schemas.ticket import TicketRead
from app.services import asset_service
from app.utils.pagination import paginate

router = APIRouter(prefix="/assets", tags=["Assets"])

STAFF = (UserRole.ADMIN, UserRole.TECHNICIAN)


def _require_staff(user: User) -> None:
    if user.role not in STAFF:
        raise ForbiddenError("FORBIDDEN", "Only staff can perform this action.")


@router.get("", response_model=list[AssetRead])
def list_assets(
    status: AssetStatus | None = None,
    assigned_to: uuid.UUID | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    filters: dict = {"status": status, "search": search}
    if user.role == UserRole.EMPLOYEE:
        filters["assigned_user_id"] = user.id
    else:
        filters["assigned_user_id"] = assigned_to
    stmt = asset_service.list_assets(db, **filters)
    rows, _ = paginate(db, stmt, page=page, page_size=page_size)
    return rows


@router.post("", response_model=AssetRead, status_code=201)
def create_asset(
    payload: AssetCreate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    _require_staff(user)
    return asset_service.create_asset(db, actor=user, data=payload)


@router.get("/{asset_id}", response_model=AssetRead)
def read_asset(
    asset_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    asset = asset_service.get_asset(db, asset_id)
    if user.role == UserRole.EMPLOYEE and asset.assigned_user_id != user.id:
        raise ForbiddenError("FORBIDDEN", "You cannot view this asset.")
    return asset


@router.patch("/{asset_id}", response_model=AssetRead)
def update_asset(
    asset_id: uuid.UUID,
    payload: AssetUpdate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    _require_staff(user)
    asset = asset_service.get_asset(db, asset_id)
    return asset_service.update_asset(db, actor=user, asset=asset, data=payload.model_dump(exclude_unset=True))


@router.post("/{asset_id}/assign", response_model=AssetRead)
def assign_asset(
    asset_id: uuid.UUID,
    payload: AssetAssign,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    _require_staff(user)
    asset = asset_service.get_asset(db, asset_id)
    return asset_service.assign_asset(db, actor=user, asset=asset, user_id=payload.user_id)


@router.get("/{asset_id}/tickets", response_model=list[TicketRead])
def read_asset_tickets(
    asset_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    asset = asset_service.get_asset(db, asset_id)
    if user.role == UserRole.EMPLOYEE and asset.assigned_user_id != user.id:
        raise ForbiddenError("FORBIDDEN", "You cannot view this asset.")
    return asset_service.list_asset_tickets(db, asset)


@router.post("/{asset_id}/maintenance", response_model=AssetRead)
def record_maintenance(
    asset_id: uuid.UUID,
    payload: MaintenanceRequest,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    _require_staff(user)
    asset = asset_service.get_asset(db, asset_id)
    return asset_service.record_maintenance(db, actor=user, asset=asset, note=payload.note)