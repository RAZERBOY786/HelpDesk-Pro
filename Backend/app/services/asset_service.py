"""Asset management."""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.asset import Asset
from app.models.enums import AssetStatus
from app.models.ticket import Ticket
from app.models.user import User
from app.services import audit_service

VALID_TRANSITIONS: dict[AssetStatus, set[AssetStatus]] = {
    AssetStatus.AVAILABLE: {AssetStatus.IN_USE, AssetStatus.UNDER_REPAIR, AssetStatus.RETIRED},
    AssetStatus.IN_USE: {AssetStatus.AVAILABLE, AssetStatus.UNDER_REPAIR, AssetStatus.RETIRED},
    AssetStatus.UNDER_REPAIR: {AssetStatus.AVAILABLE, AssetStatus.RETIRED},
    AssetStatus.RETIRED: set(),
}


def get_asset(db: Session, asset_id) -> Asset:
    asset = db.get(Asset, asset_id)
    if asset is None:
        raise NotFoundError("ASSET_NOT_FOUND", "The requested asset was not found.")
    return asset


def list_assets(db: Session, **filters):
    from app.repositories.asset_repository import AssetRepository

    return AssetRepository(db).list(**filters)


def create_asset(db: Session, *, actor: User, data) -> Asset:
    if db.execute(
        select(Asset).where(func.lower(Asset.asset_tag) == data.asset_tag.lower())
    ).scalar_one_or_none():
        raise ConflictError("DUPLICATE_ASSET_TAG", "An asset with this tag already exists.")
    if data.serial_number and db.execute(
        select(Asset).where(Asset.serial_number == data.serial_number)
    ).scalar_one_or_none():
        raise ConflictError("DUPLICATE_SERIAL", "An asset with this serial number already exists.")

    payload = data.model_dump()
    assigned_user_id = payload.get("assigned_user_id")
    status = AssetStatus.IN_USE if assigned_user_id else AssetStatus.AVAILABLE

    if assigned_user_id is not None:
        _validate_assignee(db, assigned_user_id)

    asset = Asset(**payload, status=status)
    db.add(asset)
    db.flush()
    audit_service.record(
        db,
        actor_id=actor.id,
        action="asset.created",
        entity_type="asset",
        entity_id=str(asset.id),
    )
    db.commit()
    db.refresh(asset)
    return asset


def update_asset(db: Session, *, actor: User, asset: Asset, data: dict) -> Asset:
    if data.get("asset_tag") and data["asset_tag"].lower() != asset.asset_tag.lower():
        if db.execute(
            select(Asset).where(
                func.lower(Asset.asset_tag) == data["asset_tag"].lower(),
                Asset.id != asset.id,
            )
        ).scalar_one_or_none():
            raise ConflictError("DUPLICATE_ASSET_TAG", "An asset with this tag already exists.")

    new_status = data.pop("status", None)
    if new_status is not None and new_status != asset.status:
        _change_status(db, actor, asset, new_status)

    if "assigned_user_id" in data:
        assignee = data["assigned_user_id"]
        if assignee is not None:
            _validate_assignee(db, assignee)

    for field, value in data.items():
        setattr(asset, field, value)

    audit_service.record(
        db,
        actor_id=actor.id,
        action="asset.updated",
        entity_type="asset",
        entity_id=str(asset.id),
    )
    db.commit()
    db.refresh(asset)
    return asset


def assign_asset(db: Session, *, actor: User, asset: Asset, user_id) -> Asset:
    _validate_assignee(db, user_id)
    asset.assigned_user_id = user_id
    if asset.status == AssetStatus.AVAILABLE:
        asset.status = AssetStatus.IN_USE
    audit_service.record(
        db,
        actor_id=actor.id,
        action="asset.assigned",
        entity_type="asset",
        entity_id=str(asset.id),
        after_state=str(user_id),
    )
    db.commit()
    db.refresh(asset)
    return asset


def record_maintenance(db: Session, *, actor: User, asset: Asset, note: str) -> Asset:
    _change_status(db, actor, asset, AssetStatus.UNDER_REPAIR)
    audit_service.record(
        db,
        actor_id=actor.id,
        action="asset.maintenance",
        entity_type="asset",
        entity_id=str(asset.id),
        after_state=note,
    )
    db.commit()
    db.refresh(asset)
    return asset


def list_asset_tickets(db: Session, asset: Asset):
    return db.execute(
        select(Ticket).where(Ticket.asset_id == asset.id).order_by(Ticket.created_at.desc())
    ).scalars().all()


def _change_status(db: Session, actor: User, asset: Asset, new_status: AssetStatus) -> None:
    if new_status not in VALID_TRANSITIONS.get(asset.status, set()):
        raise ValidationError(
            "INVALID_ASSET_TRANSITION",
            f"Cannot move asset from '{asset.status.value}' to '{new_status.value}'.",
        )
    old = asset.status
    asset.status = new_status
    audit_service.record(
        db,
        actor_id=actor.id,
        action="asset.status_changed",
        entity_type="asset",
        entity_id=str(asset.id),
        before_state=old.value,
        after_state=new_status.value,
    )


def _validate_assignee(db: Session, user_id) -> None:
    user = db.get(User, user_id)
    if user is None:
        raise NotFoundError("USER_NOT_FOUND", "The user to assign was not found.")
    if not user.is_active:
        raise ValidationError("INACTIVE_USER", "Cannot assign an asset to an inactive user.")