from __future__ import annotations

from math import ceil

from sqlalchemy import func, select
from sqlalchemy.orm import Session


def paginate(
    db: Session,
    stmt,
    *,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list, int]:
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)

    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    rows = (
        db.execute(stmt.offset((page - 1) * page_size).limit(page_size))
        .scalars()
        .all()
    )
    return list(rows), int(total)


def page_meta(total: int, page: int, page_size: int) -> dict:
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": ceil(total / page_size) if page_size else 0,
        "has_next": page * page_size < total,
        "has_prev": page > 1,
    }