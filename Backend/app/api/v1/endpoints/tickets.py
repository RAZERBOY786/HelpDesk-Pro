from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError
from app.db.session import get_db
from app.dependencies import require_active_user
from app.models.enums import TicketCategory, TicketPriority, TicketStatus, UserRole
from app.models.user import User
from app.schemas.comment import TicketHistoryRead
from app.schemas.ticket import (
    TicketAssign,
    TicketClose,
    TicketCreate,
    TicketRead,
    TicketReopen,
    TicketResolve,
    TicketUpdate,
)
from app.repositories.ticket_repository import TicketRepository
from app.services import ticket_service
from app.utils.pagination import paginate

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.post("", response_model=TicketRead, status_code=201)
def create_ticket(
    payload: TicketCreate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    return ticket_service.create_ticket(db, creator=user, data=payload)


@router.get("", response_model=list[TicketRead])
def list_tickets(
    status: TicketStatus | None = None,
    priority: TicketPriority | None = None,
    category: TicketCategory | None = None,
    assigned_to: uuid.UUID | None = None,
    unassigned: bool = False,
    mine: bool = False,
    search: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    filters: dict = {
        "status": status.value if status else None,
        "priority": priority.value if priority else None,
        "category": category.value if category else None,
        "search": search,
        "unassigned": unassigned,
    }

    if user.role == UserRole.EMPLOYEE:
        filters["created_by_id"] = user.id
    elif mine:
        filters["assigned_to_id"] = user.id
    elif assigned_to is not None:
        filters["assigned_to_id"] = assigned_to

    stmt = TicketRepository(db).list(**filters)
    return paginate(db, stmt, page=page, page_size=page_size)[0]


@router.get("/{ticket_id}", response_model=TicketRead)
def read_ticket(
    ticket_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    return ticket_service.get_ticket(db, ticket_id, user=user)


@router.patch("/{ticket_id}", response_model=TicketRead)
def update_ticket(
    ticket_id: uuid.UUID,
    payload: TicketUpdate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    if user.role == UserRole.EMPLOYEE and ticket.created_by_id != user.id:
        raise ForbiddenError("FORBIDDEN", "You cannot update this ticket.")
    if ticket.status in (TicketStatus.CLOSED,):
        raise ForbiddenError("TICKET_CLOSED", "Closed tickets cannot be edited.")
    data = payload.model_dump(exclude_unset=True)
    return ticket_service.update_ticket(db, actor=user, ticket=ticket, data=data)


@router.post("/{ticket_id}/assign", response_model=TicketRead)
def assign_ticket(
    ticket_id: uuid.UUID,
    payload: TicketAssign,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    if not ticket_service.can_assign(user, ticket):
        raise ForbiddenError("FORBIDDEN", "You cannot assign tickets.")
    return ticket_service.assign_ticket(
        db, actor=user, ticket=ticket, technician_id=payload.assigned_to_id, note=payload.note
    )


@router.get("/{ticket_id}/history", response_model=list[TicketHistoryRead])
def read_history(
    ticket_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    return ticket_service.get_history(db, ticket)


@router.post("/{ticket_id}/resolve", response_model=TicketRead)
def resolve_ticket(
    ticket_id: uuid.UUID,
    payload: TicketResolve,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    if not ticket_service.can_resolve(user, ticket):
        raise ForbiddenError("FORBIDDEN", "You cannot resolve this ticket.")
    return ticket_service.resolve_ticket(
        db, actor=user, ticket=ticket, resolution_summary=payload.resolution_summary, note=payload.note
    )


@router.post("/{ticket_id}/close", response_model=TicketRead)
def close_ticket(
    ticket_id: uuid.UUID,
    payload: TicketClose,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    if not ticket_service.can_close(user, ticket):
        raise ForbiddenError("FORBIDDEN", "You cannot close this ticket.")
    return ticket_service.close_ticket(db, actor=user, ticket=ticket, note=payload.note)


@router.post("/{ticket_id}/reopen", response_model=TicketRead)
def reopen_ticket(
    ticket_id: uuid.UUID,
    payload: TicketReopen,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    if not ticket_service.can_reopen(user, ticket):
        raise ForbiddenError("FORBIDDEN", "You cannot reopen this ticket.")
    return ticket_service.reopen_ticket(db, actor=user, ticket=ticket, note=payload.note)