from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.enums import AssetStatus


class AssetRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, asset_id: UUID) -> Asset | None:
        return self.db.get(Asset, asset_id)

    def get_by_tag(self, asset_tag: str) -> Asset | None:
        return self.db.execute(
            select(Asset).where(func.lower(Asset.asset_tag) == asset_tag.lower())
        ).scalar_one_or_none()

    def get_by_serial(self, serial_number: str) -> Asset | None:
        return self.db.execute(
            select(Asset).where(Asset.serial_number == serial_number)
        ).scalar_one_or_none()

    def list(
        self,
        *,
        status: AssetStatus | None = None,
        assigned_user_id: UUID | None = None,
        search: str | None = None,
    ):
        stmt = select(Asset)
        if status is not None:
            stmt = stmt.where(Asset.status == status)
        if assigned_user_id is not None:
            stmt = stmt.where(Asset.assigned_user_id == assigned_user_id)
        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(
                func.lower(Asset.name).like(like)
                | func.lower(Asset.asset_tag).like(like)
            )
        return stmt.order_by(Asset.created_at.desc())

    def add(self, asset: Asset) -> Asset:
        self.db.add(asset)
        return asset