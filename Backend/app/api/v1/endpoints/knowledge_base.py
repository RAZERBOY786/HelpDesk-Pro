from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, NotFoundError
from app.db.session import get_db
from app.dependencies import require_active_user
from app.models.knowledge_base import KnowledgeArticle
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.knowledge_base import (
    KnowledgeArticleCreate,
    KnowledgeArticleRead,
    KnowledgeArticleUpdate,
)
from app.services import audit_service

router = APIRouter(prefix="/knowledge-base", tags=["Knowledge Base"])

PUBLISHERS = (UserRole.ADMIN, UserRole.TECHNICIAN)


@router.get("/articles", response_model=list[KnowledgeArticleRead])
def list_articles(
    category: str | None = None,
    search: str | None = None,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    stmt = select(KnowledgeArticle)
    if user.role not in PUBLISHERS:
        stmt = stmt.where(KnowledgeArticle.is_published.is_(True))
    if category:
        stmt = stmt.where(KnowledgeArticle.category == category)
    if search:
        like = f"%{search.lower()}%"
        stmt = stmt.where(KnowledgeArticle.title.ilike(like))
    return list(db.execute(stmt.order_by(KnowledgeArticle.created_at.desc())).scalars())


@router.post("/articles", response_model=KnowledgeArticleRead, status_code=201)
def create_article(
    payload: KnowledgeArticleCreate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    if user.role not in PUBLISHERS:
        raise ForbiddenError("FORBIDDEN", "Only staff can publish articles.")
    article = KnowledgeArticle(
        **payload.model_dump(),
        author_id=user.id,
        published_at=datetime.now(timezone.utc) if payload.is_published else None,
    )
    db.add(article)
    db.flush()
    audit_service.record(
        db,
        actor_id=user.id,
        action="knowledge.article_created",
        entity_type="knowledge_article",
        entity_id=str(article.id),
    )
    db.commit()
    db.refresh(article)
    return article


@router.patch("/articles/{article_id}", response_model=KnowledgeArticleRead)
def update_article(
    article_id: uuid.UUID,
    payload: KnowledgeArticleUpdate,
    user: User = Depends(require_active_user),
    db: Session = Depends(get_db),
):
    if user.role not in PUBLISHERS:
        raise ForbiddenError("FORBIDDEN", "Only staff can edit articles.")
    article = db.get(KnowledgeArticle, article_id)
    if article is None:
        raise NotFoundError("ARTICLE_NOT_FOUND", "The requested article was not found.")
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(article, field, value)
    if data.get("is_published") and article.published_at is None:
        article.published_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(article)
    return article