from __future__ import annotations

from app.models.enums import UserRole


def test_employee_cannot_list_users(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    assert client.get("/api/v1/users", headers=headers).status_code == 403


def test_employee_cannot_change_roles(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    target = make_user(email="other@example.test")
    headers = auth_headers("emp@example.test")
    response = client.patch(
        f"/api/v1/users/{target.id}/role",
        headers=headers,
        params={"role": "admin"},
    )
    assert response.status_code == 403


def test_admin_cannot_disable_last_admin(client, make_user, auth_headers):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    headers = auth_headers("admin@example.test")
    response = client.patch(
        f"/api/v1/users/{admin.id}/status",
        headers=headers,
        params={"is_active": False},
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "LAST_ADMIN"


def test_technician_cannot_access_audit_logs(client, make_user, auth_headers):
    make_user(email="tech@example.test", role=UserRole.TECHNICIAN)
    headers = auth_headers("tech@example.test")
    assert client.get("/api/v1/admin/audit-logs", headers=headers).status_code == 403


def test_admin_can_access_audit_logs(client, make_user, auth_headers):
    make_user(email="admin@example.test", role=UserRole.ADMIN)
    headers = auth_headers("admin@example.test")
    response = client.get("/api/v1/admin/audit-logs", headers=headers)
    assert response.status_code == 200


def test_employee_cannot_change_ticket_priority(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    ticket = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "title": "Monitor flickering",
            "description": "The external monitor flickers whenever the dock is used.",
            "category": "hardware",
            "priority": "low",
        },
    ).json()

    response = client.patch(
        f"/api/v1/tickets/{ticket['id']}",
        headers=headers,
        json={"priority": "critical"},
    )
    assert response.status_code == 200
    assert response.json()["priority"] == "low"