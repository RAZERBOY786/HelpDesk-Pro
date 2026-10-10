from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from app.core.exceptions import UnauthorizedError, ValidationError
from app.models.enums import UserRole
from app.models.user import PasswordResetToken
from app.services import auth_service


def test_authenticate_rejects_bad_password(db, make_user):
    make_user(email="emp@example.test")
    with pytest.raises(UnauthorizedError):
        auth_service.authenticate(db, email="emp@example.test", password="wrong-password")


def test_authenticate_rejects_inactive_user(db, make_user):
    make_user(email="off@example.test", is_active=False)
    with pytest.raises(UnauthorizedError):
        auth_service.authenticate(db, email="off@example.test", password="Password123!")


def test_forgot_password_generic_for_unknown_email(db):
    assert auth_service.request_password_reset(db, email="ghost@example.test") is None


def test_password_reset_token_single_use(db, make_user):
    user = make_user(email="emp@example.test")
    raw = auth_service.request_password_reset(db, email="emp@example.test")
    assert raw is not None

    auth_service.reset_password(db, raw_token=raw, new_password="BrandNew123!")
    assert auth_service.authenticate(db, email="emp@example.test", password="BrandNew123!").id == user.id

    with pytest.raises(ValidationError):
        auth_service.reset_password(db, raw_token=raw, new_password="Another123!")


def test_expired_reset_token_rejected(db, make_user):
    make_user(email="emp@example.test")
    raw = auth_service.request_password_reset(db, email="emp@example.test")
    assert raw is not None

    token = db.query(PasswordResetToken).one()
    token.expires_at = datetime.now(timezone.utc) - timedelta(minutes=1)
    db.commit()

    with pytest.raises(ValidationError):
        auth_service.reset_password(db, raw_token=raw, new_password="TooLate123!")


def test_logout_revokes_refresh_token(db, make_user):
    user = make_user(email="emp@example.test")
    _access, refresh = auth_service.issue_tokens(user)
    auth_service.logout(db, user)

    with pytest.raises(UnauthorizedError):
        auth_service.refresh(db, refresh_token=refresh)