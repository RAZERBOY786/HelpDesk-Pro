from __future__ import annotations

import hashlib


def test_login_returns_tokens(client, make_user):
    make_user(email="emp@example.test")
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "emp@example.test", "password": "Password123!"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["access_token"]
    assert body["refresh_token"]


def test_login_failure_is_generic(client, make_user):
    make_user(email="emp@example.test")
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "emp@example.test", "password": "nope"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "INVALID_CREDENTIALS"


def test_login_unknown_email_has_same_error(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "ghost@example.test", "password": "nope"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "INVALID_CREDENTIALS"


def test_inactive_user_cannot_login(client, make_user):
    make_user(email="off@example.test", is_active=False)
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "off@example.test", "password": "Password123!"},
    )
    assert response.status_code == 401
    assert response.json()["detail"]["code"] == "ACCOUNT_DISABLED"


def test_me_requires_authentication(client):
    assert client.get("/api/v1/users/me").status_code == 401


def test_me_returns_profile(client, make_user, auth_headers):
    make_user(email="emp@example.test", name="Emp")
    headers = auth_headers("emp@example.test")
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "emp@example.test"


def test_logout_revokes_session(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "emp@example.test", "password": "Password123!"},
    )
    refresh_token = login.json()["refresh_token"]

    assert client.post("/api/v1/auth/logout", headers=headers).status_code == 200

    refreshed = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert refreshed.status_code == 401
    assert client.get("/api/v1/users/me", headers=headers).status_code == 401


def test_refresh_issues_new_access_token(client, make_user):
    make_user(email="emp@example.test")
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "emp@example.test", "password": "Password123!"},
    )
    refresh_token = login.json()["refresh_token"]
    response = client.post("/api/v1/auth/refresh", json={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert response.json()["access_token"]


def test_password_reset_flow(client, make_user, db):
    make_user(email="emp@example.test")
    response = client.post("/api/v1/auth/forgot-password", json={"email": "emp@example.test"})
    assert response.status_code == 200

    from app.models.user import PasswordResetToken

    token = db.query(PasswordResetToken).one()

    # Re-issue a raw token we control by hashing a known value.
    raw = "known-token-value-for-testing-1234567890"
    token.token_hash = hashlib.sha256(raw.encode()).hexdigest()
    db.commit()

    reset = client.post(
        "/api/v1/auth/reset-password",
        json={"token": raw, "new_password": "FreshPass123!"},
    )
    assert reset.status_code == 200

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "emp@example.test", "password": "FreshPass123!"},
    )
    assert login.status_code == 200