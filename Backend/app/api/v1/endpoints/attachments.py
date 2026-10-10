from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, File, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import require_active_user
from app.schemas.attachment import AttachmentRead
from app.services import attachment_service, ticket_service

router = APIRouter(tags=["Attachments"])


@router.post("/tickets/{ticket_id}/attachments", response_model=AttachmentRead, status_code=201)
def upload_attachment(
    ticket_id: uuid.UUID,
    file: UploadFile = File(...),
    user=Depends(require_active_user),
    db: Session = Depends(get_db),
):
    ticket = ticket_service.get_ticket(db, ticket_id, user=user)
    return attachment_service.validate_and_store(
        db, ticket=ticket, uploader=user, upload=file
    )


@router.get("/attachments/{attachment_id}")
def download_attachment(
    attachment_id: uuid.UUID,
    user=Depends(require_active_user),
    db: Session = Depends(get_db),
):
    attachment = attachment_service.get_attachment(db, attachment_id)
    ticket_service.get_ticket(db, attachment.ticket_id, user=user)
    path = attachment_service.path_for(attachment)
    attachment_service.record_download(db, attachment, actor_id=user.id)
    return FileResponse(
        path,
        filename=attachment.original_name,
        media_type=attachment.content_type,
    )