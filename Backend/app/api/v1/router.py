from fastapi import APIRouter

from app.api.v1.endpoints import (
    assets,
    attachments,
    audit_logs,
    auth,
    comments,
    health,
    knowledge_base,
    notifications,
    reports,
    sla,
    tickets,
    users,
)

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(tickets.router)
api_router.include_router(comments.router)
api_router.include_router(assets.router)
api_router.include_router(attachments.router)
api_router.include_router(sla.router)
api_router.include_router(notifications.router)
api_router.include_router(reports.router)
api_router.include_router(knowledge_base.router)
api_router.include_router(audit_logs.router)
api_router.include_router(health.router)