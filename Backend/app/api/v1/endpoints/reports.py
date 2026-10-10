from __future__ import annotations

import csv
from io import StringIO

from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import require_roles
from app.models.enums import UserRole
from app.models.ticket import Ticket
from app.models.user import User
from app.schemas.report import ReportOverview, TicketMetrics
from app.services import report_service

router = APIRouter(prefix="/reports", tags=["Reports"])

staff = require_roles(UserRole.ADMIN, UserRole.TECHNICIAN)


@router.get("/overview", response_model=ReportOverview)
def overview(_user: User = Depends(staff), db: Session = Depends(get_db)):
    return report_service.overview(db)


@router.get("/tickets", response_model=TicketMetrics)
def tickets(_user: User = Depends(staff), db: Session = Depends(get_db)):
    return report_service.ticket_metrics(db)


@router.get("/technicians")
def technicians(_user: User = Depends(staff), db: Session = Depends(get_db)):
    return report_service.technician_metrics(db)


@router.get("/sla")
def sla(_user: User = Depends(staff), db: Session = Depends(get_db)):
    return report_service.sla_metrics(db)


@router.get("/tickets.csv")
def tickets_csv(_user: User = Depends(staff), db: Session = Depends(get_db)):
    rows = db.execute(select(Ticket).order_by(Ticket.created_at.desc())).scalars().all()
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        ["ticket_number", "title", "status", "priority", "category", "created_at", "resolved_at"]
    )
    for t in rows:
        writer.writerow(
            [
                t.ticket_number,
                t.title,
                t.status.value,
                t.priority.value,
                t.category.value,
                t.created_at.isoformat() if t.created_at else "",
                t.resolved_at.isoformat() if t.resolved_at else "",
            ]
        )
    return Response(content=buffer.getvalue(), media_type="text/csv")