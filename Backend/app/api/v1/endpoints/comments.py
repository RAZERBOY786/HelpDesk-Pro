from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import require_active_user
from app.models.comment import Comment
from app.models.enums import CommentVisibility, UserRole
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead
from app.services import ticket_service

router = APIRouter(prefix="/tickets", tags=["Comments"])


@router.post("/{ticket_id}/comments", response_model=CommentRead, status_code=201)
def add_comment(
    ticket_id: uuid.UUID,
    payload: CommentCreate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    return ticket_service.add_comment(
        db, author=user, ticket=ticket, body=payload.body, visibility=payload.visibility
    )


@router.get("/{ticket_id}/comments", response_model=list[CommentRead])
def list_comments(
    ticket_id: uuid.UUID,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    stmt = (
        select(Comment)
        .where(Comment.ticket_id == ticket.id)
        .order_by(Comment.created_at.asc())
    )
    if user.role == UserRole.EMPLOYEE:
        stmt = stmt.where(Comment.visibility == CommentVisibility.PUBLIC)
    return list(db.execute(stmt).scalars())