from __future__ import annotations

import pytest

from app.core.exceptions import ConflictError, ValidationError
from app.models.enums import AssetStatus, UserRole
from app.schemas.asset import AssetCreate
from app.services import asset_service


def _asset(**overrides) -> AssetCreate:
    data = {
        "asset_tag": "LAP-0001",
        "name": "Dell Latitude",
        "serial_number": "SN-1",
    }
    data.update(overrides)
    return AssetCreate(**data)


def test_duplicate_asset_tag_rejected(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    asset_service.create_asset(db, actor=admin, data=_asset())
    with pytest.raises(ConflictError):
        asset_service.create_asset(db, actor=admin, data=_asset(serial_number="SN-2"))


def test_asset_assigned_user_sets_in_use(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    employee = make_user(email="emp@example.test")
    asset = asset_service.create_asset(db, actor=admin, data=_asset(assigned_user_id=employee.id))
    assert asset.status == AssetStatus.IN_USE


def test_invalid_status_transition_rejected(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    asset = asset_service.create_asset(db, actor=admin, data=_asset())

    asset = asset_service.record_maintenance(db, actor=admin, asset=asset, note="Screen repair")
    assert asset.status == AssetStatus.UNDER_REPAIR

    asset_service.update_asset(db, actor=admin, asset=asset, data={"status": AssetStatus.RETIRED})
    with pytest.raises(ValidationError):
        asset_service.update_asset(
            db, actor=admin, asset=asset, data={"status": AssetStatus.IN_USE}
        )