from __future__ import annotations

from datetime import datetime, date
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import AssetStatus


class AssetBase(BaseModel):
    asset_tag: str = Field(min_length=1, max_length=64)
    serial_number: str | None = Field(default=None, max_length=128)
    name: str = Field(min_length=1, max_length=160)
    model: str | None = Field(default=None, max_length=120)
    category: str | None = Field(default=None, max_length=80)
    assigned_user_id: UUID | None = None
    warranty_expiry: date | None = None
    purchase_date: date | None = None
    notes: str | None = Field(default=None, max_length=5000)


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    asset_tag: str | None = Field(default=None, min_length=1, max_length=64)
    serial_number: str | None = Field(default=None, max_length=128)
    name: str | None = Field(default=None, min_length=1, max_length=160)
    model: str | None = Field(default=None, max_length=120)
    category: str | None = Field(default=None, max_length=80)
    status: AssetStatus | None = None
    assigned_user_id: UUID | None = None
    warranty_expiry: date | None = None
    purchase_date: date | None = None
    notes: str | None = Field(default=None, max_length=5000)


class AssetRead(AssetBase):
    id: UUID
    status: AssetStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetAssign(BaseModel):
    user_id: UUID


class MaintenanceRequest(BaseModel):
    note: str = Field(min_length=1, max_length=2000)