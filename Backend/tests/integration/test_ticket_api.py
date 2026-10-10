from __future__ import annotations

from app.models.enums import UserRole


def _new_ticket(client, headers, **overrides):
    body = {
        "title": "Cannot access shared drive",
        "description": "Getting access denied when opening the finance shared drive.",
        "category": "network",
        "priority": "medium",
    }
    body.update(overrides)
    return client.post("/api/v1/tickets", headers=headers, json=body)


def test_create_and_fetch_ticket(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")

    created = _new_ticket(client, headers)
    assert created.status_code == 201
    ticket = created.json()
    assert ticket["ticket_number"].startswith("HD-")
    assert ticket["status"] == "open"

    fetched = client.get(f"/api/v1/tickets/{ticket['id']}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["id"] == ticket["id"]


def test_history_recorded_on_create(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    ticket_id = _new_ticket(client, headers).json()["id"]

    history = client.get(f"/api/v1/tickets/{ticket_id}/history", headers=headers)
    assert history.status_code == 200
    assert history.json()[0]["event_type"] == "created"


def test_assign_then_resolve_flow(client, make_user, auth_headers):
    technician = make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    make_user(email="admin@example.test", role=UserRole.ADMIN)
    make_user(email="emp@example.test")

    emp_headers = auth_headers("emp@example.test")
    tech_headers = auth_headers("tech@example.test")
    admin_headers = auth_headers("admin@example.test")

    ticket_id = _new_ticket(client, emp_headers).json()["id"]

    assigned = client.post(
        f"/api/v1/tickets/{ticket_id}/assign",
        headers=admin_headers,
        json={"assigned_to_id": str(technician.id)},
    )
    assert assigned.status_code == 200
    assert assigned.json()["status"] == "assigned"

    comment = client.post(
        f"/api/v1/tickets/{ticket_id}/comments",
        headers=tech_headers,
        json={"body": "Looking into it now.", "visibility": "public"},
    )
    assert comment.status_code == 201

    resolved = client.post(
        f"/api/v1/tickets/{ticket_id}/resolve",
        headers=tech_headers,
        json={"resolution_summary": "Re-applied share permissions on the file server."},
    )
    assert resolved.status_code == 200
    assert resolved.json()["status"] == "resolved"

    closed = client.post(
        f"/api/v1/tickets/{ticket_id}/close",
        headers=admin_headers,
        json={"note": "Confirmed with user."},
    )
    assert closed.status_code == 200
    assert closed.json()["status"] == "closed"


def test_technician_cannot_resolve_unassigned(client, make_user, auth_headers):
    make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    make_user(email="emp@example.test")

    emp_headers = auth_headers("emp@example.test")
    tech_headers = auth_headers("tech@example.test")

    ticket_id = _new_ticket(client, emp_headers).json()["id"]

    response = client.post(
        f"/api/v1/tickets/{ticket_id}/resolve",
        headers=tech_headers,
        json={"resolution_summary": "Attempting to resolve without assignment."},
    )
    assert response.status_code == 403


def test_list_filters_by_status(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    _new_ticket(client, headers)

    response = client.get("/api/v1/tickets", headers=headers, params={"status": "open"})
    assert response.status_code == 200
    assert all(t["status"] == "open" for t in response.json())