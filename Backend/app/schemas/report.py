from __future__ import annotations

from pydantic import BaseModel


class ReportOverview(BaseModel):
    open_tickets: int
    in_progress_tickets: int
    resolved_tickets: int
    closed_tickets: int
    sla_breached: int
    unassigned_tickets: int
    technicians: int
    assets: int


class TicketMetrics(BaseModel):
    total: int
    by_status: dict[str, int]
    by_priority: dict[str, int]
    by_category: dict[str, int]


class TechnicianMetrics(BaseModel):
    technician_id: str
    technician_name: str
    assigned: int
    resolved: int
    overdue: int
    average_resolution_hours: float | None


class ReportsResponse(BaseModel):
    overview: ReportOverview
    ticket_metrics: TicketMetrics
    technician_metrics: list[TechnicianMetrics]