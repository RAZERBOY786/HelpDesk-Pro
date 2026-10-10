from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field


def _validate_email(value: str) -> str:
    from email_validator import EmailNotValidError, validate_email

    try:
        result = validate_email(
            value,
            check_deliverability=False,
            test_environment=True,
        )
    except EmailNotValidError as exc:
        raise ValueError(str(exc)) from exc
    return result.normalized


EmailAddress = Annotated[str, AfterValidator(_validate_email)]


class CommonQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=20, ge=1, le=100)
    search: str | None = None

    model_config = ConfigDict(extra="forbid")


class Message(BaseModel):
    message: str


class CountedResponse(BaseModel):
    total: int
    items: list


class Pagination(BaseModel):
    total: int
    page: int
    size: int
    has_next: bool
    has_prev: bool


class PageResponse(BaseModel):
    items: list
    pagination: Pagination