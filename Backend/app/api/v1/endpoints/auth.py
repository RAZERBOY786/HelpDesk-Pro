from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies import require_active_user
from app.models.user import User
from app.schemas.auth import (
    ForgotPasswordRequest,
    LoginRequest,
    RefreshRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.schemas.common import Message
from app.services import auth_service, email_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, request: Request, db: Session = Depends(get_db)):
    ip = request.client.host if request.client else None
    _user, access, refresh = auth_service.login(
        db, email=payload.email, password=payload.password, ip=ip
    )
    return TokenResponse(access_token=access, refresh_token=refresh)


@router.post("/refresh", response_model=TokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    _user, access, new_refresh = auth_service.refresh(db, refresh_token=payload.refresh_token)
    return TokenResponse(access_token=access, refresh_token=new_refresh)


@router.post("/logout", response_model=Message)
def logout(user: User = Depends(require_active_user), db: Session = Depends(get_db)):
    auth_service.logout(db, user)
    return Message(message="Signed out.")


@router.post("/forgot-password", response_model=Message)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    raw_token = auth_service.request_password_reset(db, email=payload.email)
    if raw_token:
        email_service.send_email(
            to=payload.email,
            subject="Reset your HelpDesk Pro password",
            body=(
                "Use the following token to reset your password. "
                f"It expires in 30 minutes:\n\n{raw_token}"
            ),
        )
    return Message(
        message="If an account exists for that email, password reset instructions have been sent."
    )


@router.post("/reset-password", response_model=Message)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    auth_service.reset_password(db, raw_token=payload.token, new_password=payload.new_password)
    return Message(message="Password has been reset. You can now sign in.")