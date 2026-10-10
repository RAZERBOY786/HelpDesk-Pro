from __future__ import annotations


def test_short_title_rejected(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    response = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "title": "Hi",
            "description": "A sufficiently long description for validation.",
            "category": "software",
            "priority": "low",
        },
    )
    assert response.status_code == 422


def test_invalid_enum_rejected(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    response = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "title": "Valid title here",
            "description": "A sufficiently long description for validation.",
            "category": "not-a-category",
            "priority": "low",
        },
    )
    assert response.status_code == 422


def test_unknown_ticket_returns_404(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    response = client.get(
        "/api/v1/tickets/00000000-0000-0000-0000-000000000000", headers=headers
    )
    assert response.status_code == 404


def test_unknown_route_returns_404(client):
    assert client.get("/api/v1/does-not-exist").status_code == 404


def test_created_by_cannot_be_spoofed(client, make_user, auth_headers):
    actor = make_user(email="emp@example.test")
    other = make_user(email="other@example.test")
    headers = auth_headers("emp@example.test")

    response = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "title": "Spending claim issue",
            "description": "Trying to submit another user's identifier.",
            "category": "software",
            "priority": "low",
            "created_by_id": str(other.id),
            "status": "closed",
        },
    )
    assert response.status_code == 201
    body = response.json()
    assert body["created_by_id"] == str(actor.id)
    assert body["status"] == "open"