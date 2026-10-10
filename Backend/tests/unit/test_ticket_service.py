from __future__ import annotations

import pytest

from app.core.exceptions import ForbiddenError, ValidationError
from app.models.enums import HistoryEventType, TicketPriority, TicketStatus, UserRole
from app.schemas.ticket import TicketCreate
from app.services import ticket_service


def _payload(**overrides) -> TicketCreate:
    data = {
        "title": "Laptop will not boot",
        "description": "The laptop shows a black screen after the update.",
        "category": "hardware",
        "priority": TicketPriority.HIGH,
    }
    data.update(overrides)
    return TicketCreate(**data)


def test_create_ticket_sets_deadlines_and_number(db, make_user):
    employee = make_user(email="emp@example.test", role=UserRole.EMPLOYEE)
    ticket = ticket_service.create_ticket(db, creator=employee, data=_payload())

    assert ticket.ticket_number.startswith("HD-")
    assert ticket.status == TicketStatus.OPEN
    assert ticket.response_due_at is not None
    assert ticket.resolution_due_at is not None
    assert ticket.resolution_due_at > ticket.response_due_at

    history = ticket_service.get_history(db, ticket)
    assert history[0].event_type == HistoryEventType.CREATED


def test_only_assigned_technician_can_resolve(db, make_user):
    employee = make_user(email="emp@example.test")
    other_tech = make_user(email="tech2@example.test", role=UserRole.TECHNICIAN)
    ticket = ticket_service.create_ticket(db, creator=employee, data=_payload())

    assert ticket_service.can_resolve(other_tech, ticket) is False

    with pytest.raises(ForbiddenError):
        ticket_service.resolve_ticket(
            db,
            actor=other_tech,
            ticket=ticket,
            resolution_summary="Fixed it by replacing the drive.",
        )


def test_assignment_to_non_technician_rejected(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    employee = make_user(email="emp@example.test")
    ticket = ticket_service.create_ticket(db, creator=employee, data=_payload())

    with pytest.raises(ValidationError):
        ticket_service.assign_ticket(
            db, actor=admin, ticket=ticket, technician_id=employee.id
        )


def test_assignment_transitions_open_to_assigned(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    employee = make_user(email="emp@example.test")
    technician = make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    ticket = ticket_service.create_ticket(db, creator=employee, data=_payload())

    ticket = ticket_service.assign_ticket(
        db, actor=admin, ticket=ticket, technician_id=technician.id
    )
    assert ticket.assigned_to_id == technician.id
    assert ticket.status == TicketStatus.ASSIGNED


def test_resolution_requires_assignment_and_summary(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    employee = make_user(email="emp@example.test")
    technician = make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    ticket = ticket_service.create_ticket(db, creator=employee, data=_payload())
    ticket = ticket_service.assign_ticket(
        db, actor=admin, ticket=ticket, technician_id=technician.id
    )
    ticket = ticket_service.resolve_ticket(
        db,
        actor=technician,
        ticket=ticket,
        resolution_summary="Replaced the SSD and restored the image.",
    )
    assert ticket.status == TicketStatus.RESOLVED
    assert ticket.resolved_at is not None
    assert ticket.resolution_summary


def test_reopen_preserves_resolution_history(db, make_user):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    employee = make_user(email="emp@example.test")
    technician = make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    ticket = ticket_service.create_ticket(db, creator=employee, data=_payload())
    ticket = ticket_service.assign_ticket(db, actor=admin, ticket=ticket, technician_id=technician.id)
    ticket = ticket_service.resolve_ticket(
        db, actor=technician, ticket=ticket, resolution_summary="Adjusted power settings."
    )
    ticket = ticket_service.reopen_ticket(db, actor=employee, ticket=ticket, note="Issue returned.")

    assert ticket.status == TicketStatus.REOPENED
    events = [h.event_type for h in ticket_service.get_history(db, ticket)]
    assert HistoryEventType.RESOLVED in events
    assert HistoryEventType.REOPENED in events