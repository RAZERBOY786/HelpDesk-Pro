from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/live")
def liveness() -> dict:
    return {"status": "ok"}


@router.get("/ready")
def readiness(db: Session = Depends(get_db)) -> dict:
    try:
        db.execute(text("SELECT 1"))
    except Exception:  # noqa: BLE001
        return {"status": "unavailable", "database": "down"}
    return {"status": "ok", "database": "up"}