from __future__ import annotations


def _create_ticket(client, headers, title="Cannot print documents"):
    response = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "title": title,
            "description": "Printer shows offline even though it is powered on.",
            "category": "hardware",
            "priority": "medium",
        },
    )
    assert response.status_code == 201
    return response.json()


def test_employee_cannot_read_another_employees_ticket(client, make_user, auth_headers):
    make_user(email="alice@example.test")
    make_user(email="bob@example.test")

    alice_headers = auth_headers("alice@example.test")
    bob_headers = auth_headers("bob@example.test")

    ticket = _create_ticket(client, alice_headers)

    response = client.get(f"/api/v1/tickets/{ticket['id']}", headers=bob_headers)
    assert response.status_code == 404


def test_employee_list_only_contains_own_tickets(client, make_user, auth_headers):
    make_user(email="alice@example.test")
    make_user(email="bob@example.test")

    alice_headers = auth_headers("alice@example.test")
    bob_headers = auth_headers("bob@example.test")

    alice_ticket = _create_ticket(client, alice_headers, title="Alice ticket one")
    bob_ticket = _create_ticket(client, bob_headers, title="Bob ticket one")

    response = client.get("/api/v1/tickets", headers=alice_headers)
    assert response.status_code == 200
    ids = {t["id"] for t in response.json()}
    assert alice_ticket["id"] in ids
    assert bob_ticket["id"] not in ids


def test_employee_cannot_read_others_history(client, make_user, auth_headers):
    make_user(email="alice@example.test")
    make_user(email="bob@example.test")
    alice_headers = auth_headers("alice@example.test")
    bob_headers = auth_headers("bob@example.test")

    ticket = _create_ticket(client, alice_headers)
    response = client.get(f"/api/v1/tickets/{ticket['id']}/history", headers=bob_headers)
    assert response.status_code == 404