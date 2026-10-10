from __future__ import annotations

from app.models.enums import UserRole


def test_admin_can_create_asset(client, make_user, auth_headers):
    make_user(email="admin@example.test", role=UserRole.ADMIN)
    headers = auth_headers("admin@example.test")

    response = client.post(
        "/api/v1/assets",
        headers=headers,
        json={"asset_tag": "LAP-9001", "name": "ThinkPad X1", "serial_number": "SN-9001"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "available"


def test_employee_cannot_create_asset(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")

    response = client.post(
        "/api/v1/assets",
        headers=headers,
        json={"asset_tag": "LAP-9002", "name": "Unauthorized"},
    )
    assert response.status_code == 403


def test_duplicate_asset_tag_conflict(client, make_user, auth_headers):
    make_user(email="admin@example.test", role=UserRole.ADMIN)
    headers = auth_headers("admin@example.test")
    payload = {"asset_tag": "LAP-9003", "name": "Dup"}

    assert client.post("/api/v1/assets", headers=headers, json=payload).status_code == 201
    duplicate = client.post("/api/v1/assets", headers=headers, json=payload)
    assert duplicate.status_code == 409
    assert duplicate.json()["detail"]["code"] == "DUPLICATE_ASSET_TAG"


def test_asset_tickets_link(client, make_user, auth_headers):
    admin = make_user(email="admin@example.test", role=UserRole.ADMIN)
    employee = make_user(email="emp@example.test")
    admin_headers = auth_headers("admin@example.test")
    emp_headers = auth_headers("emp@example.test")

    asset = client.post(
        "/api/v1/assets",
        headers=admin_headers,
        json={
            "asset_tag": "LAP-9004",
            "name": "MacBook Air",
            "assigned_user_id": str(employee.id),
        },
    ).json()

    client.post(
        "/api/v1/tickets",
        headers=emp_headers,
        json={
            "title": "Battery draining fast",
            "description": "The battery no longer lasts more than an hour.",
            "category": "hardware",
            "priority": "low",
            "asset_id": asset["id"],
        },
    )

    linked = client.get(f"/api/v1/assets/{asset['id']}/tickets", headers=admin_headers)
    assert linked.status_code == 200
    assert len(linked.json()) == 1