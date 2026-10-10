from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import UserRole
from app.schemas.common import EmailAddress


class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=160)
    email: EmailAddress
    department: str | None = Field(default=None, max_length=120)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=255)
    role: UserRole = UserRole.EMPLOYEE


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=160)
    email: EmailAddress | None = None
    department: str | None = Field(default=None, max_length=120)
    is_active: bool | None = None


class UserRead(UserBase):
    id: UUID
    role: UserRole
    is_active: bool
    token_version: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
