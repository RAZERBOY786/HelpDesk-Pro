from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import UserRole
from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, user_id: UUID) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        return self.db.execute(
            select(User).where(func.lower(User.email) == email.lower())
        ).scalar_one_or_none()

    def list(
        self,
        *,
        role: UserRole | None = None,
        is_active: bool | None = None,
        search: str | None = None,
    ):
        stmt = select(User)
        if role is not None:
            stmt = stmt.where(User.role == role)
        if is_active is not None:
            stmt = stmt.where(User.is_active.is_(is_active))
        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(
                func.lower(User.name).like(like) | func.lower(User.email).like(like)
            )
        return stmt.order_by(User.created_at.desc())

    def count_active_admins(self) -> int:
        return self.db.execute(
            select(func.count())
            .select_from(User)
            .where(User.role == UserRole.ADMIN, User.is_active.is_(True))
        ).scalar_one()

    def add(self, user: User) -> User:
        self.db.add(user)
        return user