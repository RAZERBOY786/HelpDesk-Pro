from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError
from app.db.session import get_db
from app.dependencies import require_active_user, require_roles
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.auth import PasswordChange
from app.schemas.common import Message
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import auth_service, user_service
from app.utils.pagination import page_meta, paginate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserRead)
def read_current_user(user: User = Depends(require_active_user)):
    return user


@router.patch("/me", response_model=UserRead)
def update_current_user(
    payload: UserUpdate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    data = payload.model_dump(exclude_unset=True)
    data.pop("is_active", None)
    data.pop("email", None)
    data.pop("role", None)
    return user_service.update_user(db, actor=user, user_id=user.id, data=data)


@router.post("/me/password", response_model=Message)
def change_password(
    payload: PasswordChange,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    auth_service.change_password(
        db,
        user=user,
        current_password=payload.current_password,
        new_password=payload.new_password,
    )
    return Message(message="Password updated. Please sign in again.")


@router.get("", response_model=list[UserRead])
def list_users(
    role: UserRole | None = None,
    is_active: bool | None = None,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    _admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    stmt = user_service.list_users(db, role=role, is_active=is_active, search=search)
    rows, total = paginate(db, stmt, page=page, page_size=page_size)
    return rows


@router.post("", response_model=UserRead, status_code=201)
def create_user(
    payload: UserCreate,
    admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return user_service.create_user(
        db,
        actor_id=admin.id,
        name=payload.name,
        email=payload.email,
        password=payload.password,
        role=payload.role,
        department=payload.department,
    )


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    if user.role != UserRole.ADMIN and user.id != user_id:
        raise ForbiddenError("FORBIDDEN", "You can only view your own profile.")
    return user_service.get_user(db, user_id)


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: uuid.UUID,
    payload: UserUpdate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    if user.role != UserRole.ADMIN:
        if user.id != user_id:
            raise ForbiddenError("FORBIDDEN", "You can only update your own profile.")
        data = payload.model_dump(exclude_unset=True)
        data.pop("is_active", None)
        data.pop("email", None)
    else:
        data = payload.model_dump(exclude_unset=True)
    return user_service.update_user(db, actor=user, user_id=user_id, data=data)


@router.patch("/{user_id}/role", response_model=UserRead)
def change_role(
    user_id: uuid.UUID,
    role: UserRole,
    admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return user_service.change_role(db, actor=admin, user_id=user_id, new_role=role)


@router.patch("/{user_id}/status", response_model=UserRead)
def set_status(
    user_id: uuid.UUID,
    is_active: bool,
    admin: User = Depends(require_roles(UserRole.ADMIN)),
    db: Session = Depends(get_db),
):
    return user_service.set_status(db, actor=admin, user_id=user_id, is_active=is_active)