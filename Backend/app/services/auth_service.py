"""Authentication workflows: login, refresh, logout, password reset."""

from __future__ import annotations

import hashlib
import secrets
import uuid
from datetime import timedelta, datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.core.exceptions import UnauthorizedError, ValidationError
from app.models.user import PasswordResetToken, User
from app.services import audit_service

RESET_TOKEN_MINUTES = 30


def _hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def authenticate(db: Session, *, email: str, password: str) -> User:
    user = db.execute(
        select(User).where(User.email == email.lower())
    ).scalar_one_or_none()
    if user is None or not security.verify_password(password, user.password_hash):
        raise UnauthorizedError("INVALID_CREDENTIALS", "Invalid email or password.")
    if not user.is_active:
        raise UnauthorizedError("ACCOUNT_DISABLED", "This account is disabled.")
    return user


def issue_tokens(user: User) -> tuple[str, str]:
    claims = {"sub": str(user.id), "ver": user.token_version, "role": user.role.value}
    access = security.create_access_token(str(user.id), claims)
    refresh = security.create_refresh_token(str(user.id), {"ver": user.token_version})
    return access, refresh


def login(db: Session, *, email: str, password: str, ip: str | None = None) -> tuple[User, str, str]:
    user = authenticate(db, email=email, password=password)
    access, refresh = issue_tokens(user)
    audit_service.record(
        db,
        actor_id=user.id,
        action="auth.login",
        entity_type="user",
        entity_id=str(user.id),
        ip_address=ip,
    )
    db.commit()
    return user, access, refresh


def refresh(db: Session, *, refresh_token: str) -> tuple[User, str, str]:
    try:
        payload = security.decode_token(refresh_token)
    except Exception as exc:  # noqa: BLE001
        raise UnauthorizedError("INVALID_TOKEN", "Invalid or expired refresh token.") from exc

    if payload.get("type") != "refresh":
        raise UnauthorizedError("INVALID_TOKEN", "Invalid refresh token.")

    try:
        user_id = uuid.UUID(payload.get("sub"))
    except (TypeError, ValueError) as exc:
        raise UnauthorizedError("INVALID_TOKEN", "Invalid refresh token.") from exc

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise UnauthorizedError("INVALID_TOKEN", "Invalid refresh token.")
    if payload.get("ver") != user.token_version:
        raise UnauthorizedError("TOKEN_REVOKED", "This session has been revoked.")

    access, new_refresh = issue_tokens(user)
    return user, access, new_refresh


def logout(db: Session, user: User) -> None:
    user.token_version += 1
    audit_service.record(
        db,
        actor_id=user.id,
        action="auth.logout",
        entity_type="user",
        entity_id=str(user.id),
    )
    db.commit()


def request_password_reset(db: Session, *, email: str) -> str | None:
    """Create a reset token if the user exists.

    Always called with a generic response by the endpoint so the API never
    reveals whether an email address is registered.
    """
    user = db.execute(select(User).where(User.email == email.lower())).scalar_one_or_none()
    if user is None or not user.is_active:
        return None

    raw = secrets.token_urlsafe(32)
    token = PasswordResetToken(
        user_id=user.id,
        token_hash=_hash_token(raw),
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=RESET_TOKEN_MINUTES),
    )
    db.add(token)
    audit_service.record(
        db,
        actor_id=user.id,
        action="auth.password_reset_requested",
        entity_type="user",
        entity_id=str(user.id),
    )
    db.commit()
    return raw


def reset_password(db: Session, *, raw_token: str, new_password: str) -> None:
    token = db.execute(
        select(PasswordResetToken).where(PasswordResetToken.token_hash == _hash_token(raw_token))
    ).scalar_one_or_none()

    now = datetime.now(timezone.utc)
    if token is None or token.used_at is not None:
        raise ValidationError("INVALID_RESET_TOKEN", "This reset link is invalid.")
    from app.utils.datetime_utils import ensure_utc

    if (ensure_utc(token.expires_at) or now) < now:
        raise ValidationError("EXPIRED_RESET_TOKEN", "This reset link has expired.")

    user = db.get(User, token.user_id)
    if user is None or not user.is_active:
        raise ValidationError("INVALID_RESET_TOKEN", "This reset link is invalid.")

    user.password_hash = security.hash_password(new_password)
    user.token_version += 1
    token.used_at = now
    audit_service.record(
        db,
        actor_id=user.id,
        action="auth.password_reset_completed",
        entity_type="user",
        entity_id=str(user.id),
    )
    db.commit()


def change_password(db: Session, *, user: User, current_password: str, new_password: str) -> None:
    if not security.verify_password(current_password, user.password_hash):
        raise UnauthorizedError("INVALID_CREDENTIALS", "Current password is incorrect.")
    user.password_hash = security.hash_password(new_password)
    user.token_version += 1
    audit_service.record(
        db,
        actor_id=user.id,
        action="auth.password_changed",
        entity_type="user",
        entity_id=str(user.id),
    )
    db.commit()