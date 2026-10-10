"""User administration."""

from __future__ import annotations

from uuid import UUID

from sqlalchemy.orm import Session

from app.core import security
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services import audit_service


def create_user(
    db: Session,
    *,
    actor_id,
    name: str,
    email: str,
    password: str,
    role,
    department: str | None = None,
) -> User:
    repo = UserRepository(db)
    if repo.get_by_email(email) is not None:
        raise ConflictError("EMAIL_TAKEN", "A user with this email already exists.")

    user = User(
        name=name,
        email=email.lower(),
        password_hash=security.hash_password(password),
        role=role,
        department=department,
        is_active=True,
    )
    db.add(user)
    db.flush()
    audit_service.record(
        db,
        actor_id=actor_id,
        action="user.created",
        entity_type="user",
        entity_id=str(user.id),
    )
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session, **filters):
    from app.repositories.user_repository import UserRepository

    return UserRepository(db).list(**filters)


def get_user(db: Session, user_id) -> User:
    from app.core.exceptions import NotFoundError

    user = db.get(User, user_id)
    if user is None:
        raise NotFoundError("USER_NOT_FOUND", "The requested user was not found.")
    return user


def update_user(db: Session, *, actor, user_id, data: dict) -> User:
    user = get_user(db, user_id)
    for field, value in data.items():
        if value is not None and hasattr(user, field):
            setattr(user, field, value)
    audit_service.record(
        db,
        actor_id=actor.id,
        action="user.updated",
        entity_type="user",
        entity_id=str(user.id),
        after_state=str(data),
    )
    db.commit()
    db.refresh(user)
    return user


def change_role(db: Session, *, actor, user_id, new_role) -> User:
    user = get_user(db, user_id)
    old_role = user.role

    if old_role == UserRole.ADMIN and new_role != UserRole.ADMIN:
        if _count_active_admins(db) <= 1:
            raise ValidationError(
                "LAST_ADMIN",
                "You cannot remove the last active administrator.",
            )

    user.role = new_role
    audit_service.record(
        db,
        actor_id=actor.id,
        action="user.role_changed",
        entity_type="user",
        entity_id=str(user.id),
        before_state=old_role.value,
        after_state=new_role.value,
    )
    db.commit()
    db.refresh(user)
    return user


def set_status(db: Session, *, actor, user_id, is_active: bool) -> User:
    user = get_user(db, user_id)

    if not is_active and user.role == UserRole.ADMIN and _count_active_admins(db) <= 1:
        raise ValidationError("LAST_ADMIN", "You cannot disable the last active administrator.")

    user.is_active = is_active
    if not is_active:
        user.token_version += 1
    audit_service.record(
        db,
        actor_id=actor.id,
        action="user.status_changed",
        entity_type="user",
        entity_id=str(user.id),
        after_state="active" if is_active else "disabled",
    )
    db.commit()
    db.refresh(user)
    return user


def _count_active_admins(db: Session) -> int:
    from sqlalchemy import func, select

    return db.execute(
        select(func.count())
        .select_from(User)
        .where(User.role == UserRole.ADMIN, User.is_active.is_(True))
    ).scalar_one()