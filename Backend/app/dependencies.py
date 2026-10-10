"""Reusable FastAPI dependencies: auth, RBAC, and resource access checks."""

from __future__ import annotations

import uuid

from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core import security
from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.ticket import Ticket
from app.models.user import User

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or not credentials.credentials:
        raise UnauthorizedError("NOT_AUTHENTICATED", "Authentication credentials were not provided.")

    try:
        payload = security.decode_token(credentials.credentials)
    except Exception as exc:  # noqa: BLE001
        raise UnauthorizedError("INVALID_TOKEN", "Invalid or expired access token.") from exc

    if payload.get("type") != "access":
        raise UnauthorizedError("INVALID_TOKEN", "Invalid access token.")

    try:
        user_id = uuid.UUID(str(payload.get("sub")))
    except (ValueError, TypeError) as exc:
        raise UnauthorizedError("INVALID_TOKEN", "Invalid access token.") from exc

    user = db.get(User, user_id)
    if user is None:
        raise UnauthorizedError("INVALID_TOKEN", "Invalid access token.")
    if payload.get("ver") != user.token_version:
        raise UnauthorizedError("TOKEN_REVOKED", "This session has been revoked.")
    if not user.is_active:
        raise UnauthorizedError("ACCOUNT_DISABLED", "This account is disabled.")

    request.state.user_id = str(user.id)
    return user


def require_active_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_active:
        raise ForbiddenError("ACCOUNT_DISABLED", "This account is disabled.")
    return user


def require_roles(*roles: UserRole):
    allowed = set(roles)

    def dependency(user: User = Depends(require_active_user)) -> User:
        if user.role not in allowed:
            raise ForbiddenError("FORBIDDEN", "You do not have permission to perform this action.")
        return user

    return dependency


def require_ticket_access(
    ticket_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
) -> Ticket:
    from app.services import ticket_service

    return ticket_service.get_ticket(db, ticket_id, user=user)