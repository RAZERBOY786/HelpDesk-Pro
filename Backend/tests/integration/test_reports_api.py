from __future__ import annotations

from app.models.enums import UserRole


def test_employee_forbidden_from_reports(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    assert client.get("/api/v1/reports/overview", headers=headers).status_code == 403


def test_admin_receives_overview(client, make_user, auth_headers):
    make_user(email="admin@example.test", role=UserRole.ADMIN)
    headers = auth_headers("admin@example.test")

    response = client.get("/api/v1/reports/overview", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert "open_tickets" in body
    assert "sla_breached" in body


def test_ticket_metrics_counts_created_tickets(client, make_user, auth_headers):
    make_user(email="admin@example.test", role=UserRole.ADMIN)
    make_user(email="emp@example.test")
    admin_headers = auth_headers("admin@example.test")
    emp_headers = auth_headers("emp@example.test")

    client.post(
        "/api/v1/tickets",
        headers=emp_headers,
        json={
            "title": "Keyboard not working",
            "description": "Several keys stopped responding after a spill.",
            "category": "hardware",
            "priority": "medium",
        },
    )

    response = client.get("/api/v1/reports/tickets", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["by_status"]["open"] == 1


def test_technician_receives_technician_metrics(client, make_user, auth_headers):
    make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    headers = auth_headers("tech@example.test")
    response = client.get("/api/v1/reports/technicians", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)