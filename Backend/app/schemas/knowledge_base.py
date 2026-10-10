from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class KnowledgeArticleBase(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    category: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1, max_length=20000)
    is_published: bool = True


class KnowledgeArticleCreate(KnowledgeArticleBase):
    pass


class KnowledgeArticleUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=160)
    category: str | None = Field(default=None, min_length=1, max_length=80)
    content: str | None = Field(default=None, min_length=1, max_length=20000)
    is_published: bool | None = None


class KnowledgeArticleRead(KnowledgeArticleBase):
    id: UUID
    author_id: UUID
    published_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)