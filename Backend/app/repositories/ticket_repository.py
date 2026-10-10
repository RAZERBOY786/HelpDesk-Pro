from __future__ import annotations

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import TicketPriority, TicketStatus
from app.models.ticket import Ticket


class TicketRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get(self, ticket_id: UUID) -> Ticket | None:
        return self.db.get(Ticket, ticket_id)

    def get_by_number(self, ticket_number: str) -> Ticket | None:
        return self.db.execute(
            select(Ticket).where(Ticket.ticket_number == ticket_number)
        ).scalar_one_or_none()

    def list(
        self,
        *,
        created_by_id: UUID | None = None,
        assigned_to_id: UUID | None = None,
        status: str | None = None,
        priority: str | None = None,
        category: str | None = None,
        asset_id: UUID | None = None,
        unassigned: bool | None = None,
        search: str | None = None,
    ):
        stmt = select(Ticket)
        if created_by_id is not None:
            stmt = stmt.where(Ticket.created_by_id == created_by_id)
        if assigned_to_id is not None:
            stmt = stmt.where(Ticket.assigned_to_id == assigned_to_id)
        if status is not None:
            stmt = stmt.where(Ticket.status == status)
        if priority is not None:
            stmt = stmt.where(Ticket.priority == priority)
        if category is not None:
            stmt = stmt.where(Ticket.category == category)
        if asset_id is not None:
            stmt = stmt.where(Ticket.asset_id == asset_id)
        if unassigned:
            stmt = stmt.where(Ticket.assigned_to_id.is_(None))
        if search:
            like = f"%{search.lower()}%"
            stmt = stmt.where(
                func.lower(Ticket.title).like(like)
                | func.lower(Ticket.ticket_number).like(like)
            )
        return stmt.order_by(Ticket.created_at.desc())

    def count_by(self, **filters) -> int:
        stmt = self.list(**filters)
        return self.db.execute(
            select(func.count()).select_from(stmt.subquery())
        ).scalar_one()

    def add(self, ticket) -> object:
        self.db.add(ticket)
        return ticket