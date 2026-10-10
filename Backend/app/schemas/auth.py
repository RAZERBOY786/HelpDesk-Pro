from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import EmailAddress


class LoginRequest(BaseModel):
    email: EmailAddress
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class PasswordChange(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8, max_length=255)


class ForgotPasswordRequest(BaseModel):
    email: EmailAddress


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=10)
    new_password: str = Field(min_length=8, max_length=255)