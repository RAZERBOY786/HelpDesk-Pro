"""Attachment validation and private storage.

Files are stored outside any publicly served directory and only metadata is
kept in the database. Content is verified by magic bytes rather than trusting
the client-supplied filename or MIME type.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import NotFoundError, ValidationError
from app.models.attachment import Attachment
from app.models.ticket import Ticket
from app.models.user import User
from app.services import audit_service

SIGNATURES: dict[str, bytes] = {
    ".png": b"\x89PNG\r\n\x1a\n",
    ".jpg": b"\xff\xd8\xff",
    ".jpeg": b"\xff\xd8\xff",
    ".gif": b"GIF89a",
    ".pdf": b"%PDF",
}
TEXT_EXTENSIONS = {".txt", ".log"}
ALLOWED_EXTENSIONS = set(SIGNATURES) | TEXT_EXTENSIONS


def _extension(filename: str) -> str:
    return Path(filename or "").suffix.lower()


def _verify_content(ext: str, data: bytes) -> None:
    if ext in SIGNATURES:
        if not data.startswith(SIGNATURES[ext]):
            raise ValidationError("INVALID_FILE_CONTENT", "File content does not match its type.")
    elif ext in TEXT_EXTENSIONS:
        if b"\x00" in data:
            raise ValidationError("INVALID_FILE_CONTENT", "Text files must not contain binary data.")
        try:
            data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationError("INVALID_FILE_CONTENT", "Text files must be UTF-8.") from exc


def _storage_dir() -> Path:
    directory = settings.upload_path
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def validate_and_store(
    db: Session,
    *,
    ticket: Ticket,
    uploader: User,
    upload: UploadFile,
) -> Attachment:
    ext = _extension(upload.filename or "")
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            "UNSUPPORTED_FILE_TYPE",
            "Only PNG, JPEG, GIF, PDF, TXT, and LOG files are allowed.",
        )

    max_bytes = settings.max_upload_size_bytes
    data = upload.file.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ValidationError("FILE_TOO_LARGE", f"File exceeds {settings.max_upload_size_mb} MB.")
    if not data:
        raise ValidationError("FILE_TOO_LARGE", "The uploaded file is empty.")

    _verify_content(ext, data)

    storage_key = f"{uuid.uuid4().hex}{ext}"
    destination = _storage_dir() / storage_key
    destination.write_bytes(data)

    attachment = Attachment(
        ticket_id=ticket.id,
        uploaded_by_id=uploader.id,
        storage_key=storage_key,
        original_name=Path(upload.filename or "upload").name,
        content_type=upload.content_type or "application/octet-stream",
        size_bytes=len(data),
    )
    db.add(attachment)
    audit_service.record(
        db,
        actor_id=uploader.id,
        action="attachment.uploaded",
        entity_type="attachment",
        entity_id=str(ticket.id),
    )
    db.commit()
    db.refresh(attachment)
    return attachment


def get_attachment(db: Session, attachment_id) -> Attachment:
    attachment = db.get(Attachment, attachment_id)
    if attachment is None:
        raise NotFoundError("ATTACHMENT_NOT_FOUND", "The requested attachment was not found.")
    return attachment


def path_for(attachment: Attachment) -> Path:
    path = settings.upload_path / attachment.storage_key
    if not path.exists():
        raise NotFoundError("ATTACHMENT_NOT_FOUND", "The attachment file is no longer available.")
    return path


def record_download(db: Session, attachment: Attachment, *, actor_id=None) -> None:
    audit_service.record(
        db,
        actor_id=actor_id,
        action="attachment.downloaded",
        entity_type="attachment",
        entity_id=str(attachment.id),
    )
    db.commit()