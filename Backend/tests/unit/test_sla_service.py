from __future__ import annotations

from datetime import timedelta

from app.models.enums import SLAEventType, TicketPriority, TicketStatus
from app.models.sla import SLAPolicy
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from app.services import sla_service, ticket_service
from app.utils.datetime_utils import utcnow


def test_policy_fallback_when_none_configured(db):
    response, resolution = sla_service.get_policy_for_priority(db, TicketPriority.CRITICAL)
    assert response == sla_service.DEFAULT_SLA_MINUTES[TicketPriority.CRITICAL][0]
    assert resolution == sla_service.DEFAULT_SLA_MINUTES[TicketPriority.CRITICAL][1]


def test_policy_used_when_configured(db):
    db.add(
        SLAPolicy(
            priority=TicketPriority.LOW,
            response_minutes=30,
            resolution_minutes=120,
        )
    )
    db.commit()
    assert sla_service.get_policy_for_priority(db, TicketPriority.LOW) == (30, 120)


def test_calculate_deadlines():
    base = utcnow()
    response, resolution = sla_service.calculate_deadlines(
        base, response_minutes=30, resolution_minutes=120
    )
    assert response == base + timedelta(minutes=30)
    assert resolution == base + timedelta(minutes=120)


def test_scan_records_breach_once(db, make_user):
    employee = make_user(email="emp@example.test")
    ticket = ticket_service.create_ticket(
        db,
        creator=employee,
        data=TicketCreate(
            title="Server down",
            description="The production server is unreachable right now.",
            category="network",
            priority=TicketPriority.CRITICAL,
        ),
    )
    # Force the response deadline into the past.
    ticket.response_due_at = utcnow() - timedelta(minutes=5)
    db.commit()

    first = sla_service.scan_ticket_deadlines(db)
    assert ticket.ticket_number in first["breaches"]

    second = sla_service.scan_ticket_deadlines(db)
    assert second["breaches"] == []
    assert second["warnings"] == []


def test_warning_recorded_before_deadline(db):
    policy = SLAPolicy(
        priority=TicketPriority.MEDIUM,
        response_minutes=240,
        resolution_minutes=1440,
    )
    db.add(policy)
    db.commit()
    response, resolution = sla_service.get_policy_for_priority(db, TicketPriority.MEDIUM)
    assert response == 240