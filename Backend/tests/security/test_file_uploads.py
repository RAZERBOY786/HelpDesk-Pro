from __future__ import annotations

import pytest

from app.core.config import settings

PNG_BYTES = b"\x89PNG\r\n\x1a\n" + b"fake-png-body"


@pytest.fixture()
def ticket(client, make_user, auth_headers):
    make_user(email="emp@example.test")
    headers = auth_headers("emp@example.test")
    response = client.post(
        "/api/v1/tickets",
        headers=headers,
        json={
            "title": "Screenshot needed",
            "description": "Attaching a screenshot of the error dialog.",
            "category": "software",
            "priority": "low",
        },
    )
    return response.json(), headers


@pytest.fixture(autouse=True)
def _upload_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "upload_dir", str(tmp_path / "uploads"))


def test_valid_png_upload_and_download(client, ticket):
    t, headers = ticket
    upload = client.post(
        f"/api/v1/tickets/{t['id']}/attachments",
        headers=headers,
        files={"file": ("screenshot.png", PNG_BYTES, "image/png")},
    )
    assert upload.status_code == 201
    attachment = upload.json()

    download = client.get(f"/api/v1/attachments/{attachment['id']}", headers=headers)
    assert download.status_code == 200
    assert download.content == PNG_BYTES


def test_executable_upload_rejected(client, ticket):
    t, headers = ticket
    response = client.post(
        f"/api/v1/tickets/{t['id']}/attachments",
        headers=headers,
        files={"file": ("malware.exe", b"MZ\x90\x00", "application/octet-stream")},
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "UNSUPPORTED_FILE_TYPE"


def test_spoofed_content_rejected(client, ticket):
    t, headers = ticket
    response = client.post(
        f"/api/v1/tickets/{t['id']}/attachments",
        headers=headers,
        files={"file": ("fake.png", b"this is not a real png", "image/png")},
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "INVALID_FILE_CONTENT"


def test_oversized_upload_rejected(client, ticket, monkeypatch):
    monkeypatch.setattr(settings, "max_upload_size_mb", 0)
    t, headers = ticket
    response = client.post(
        f"/api/v1/tickets/{t['id']}/attachments",
        headers=headers,
        files={"file": ("big.txt", b"x" * 1024, "text/plain")},
    )
    assert response.status_code == 422
    assert response.json()["detail"]["code"] == "FILE_TOO_LARGE"


def test_download_requires_authentication(client, ticket):
    t, headers = ticket
    upload = client.post(
        f"/api/v1/tickets/{t['id']}/attachments",
        headers=headers,
        files={"file": ("log.txt", b"application log line\n", "text/plain")},
    )
    attachment_id = upload.json()["id"]
    assert client.get(f"/api/v1/attachments/{attachment_id}").status_code == 401


def test_download_requires_ticket_access(client, ticket, make_user, auth_headers):
    t, headers = ticket
    make_user(email="intruder@example.test")
    intruder_headers = auth_headers("intruder@example.test")

    upload = client.post(
        f"/api/v1/tickets/{t['id']}/attachments",
        headers=headers,
        files={"file": ("log.txt", b"application log line\n", "text/plain")},
    )
    attachment_id = upload.json()["id"]

    response = client.get(f"/api/v1/attachments/{attachment_id}", headers=intruder_headers)
    assert response.status_code == 404