from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError
from pwdlib import PasswordHash

from app.core.config import settings

password_hash = PasswordHash.recommended()

HASH_VERSION = 1


def hash_password(plain: str) -> str:
    return password_hash.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return password_hash.verify(plain, hashed)
    except Exception:
        return False


def create_jwt_token(
    subject: str,
    *,
    token_type: str,
    expires_delta: timedelta,
    extra: dict[str, Any] | None = None,
) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": subject,
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra:
        payload.update(extra)
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")


def create_access_token(subject: str, extra: dict[str, Any] | None = None) -> str:
    return create_jwt_token(
        subject,
        token_type="access",
        expires_delta=timedelta(minutes=settings.access_token_minutes),
        extra=extra,
    )


def create_refresh_token(subject: str, extra: dict[str, Any] | None = None) -> str:
    return create_jwt_token(
        subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.refresh_token_days),
        extra=extra,
    )


def decode_token(
    token: str, expected_type: str | None = None
) -> dict[str, Any]:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    if expected_type is not None and payload.get("type") != expected_type:
        raise InvalidTokenError("Unexpected token type")
    return payload


def validate_access_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type="access")


def validate_refresh_token(token: str) -> dict[str, Any]:
    return decode_token(token, expected_type="refresh")