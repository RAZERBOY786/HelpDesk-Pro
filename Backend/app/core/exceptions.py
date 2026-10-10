from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application error with a stable machine-readable code."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class NotFoundError(AppError):
    def __init__(self, code: str = "NOT_FOUND", message: str = "Resource not found.") -> None:
        super().__init__(code=code, message=message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedError(AppError):
    def __init__(self, code: str = "UNAUTHORIZED", message: str = "Authentication required.") -> None:
        super().__init__(code=code, message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenError(AppError):
    def __init__(self, code: str = "FORBIDDEN", message: str = "You are not permitted to do this.") -> None:
        super().__init__(code=code, message=message, status_code=status.HTTP_403_FORBIDDEN)


class ConflictError(AppError):
    def __init__(self, code: str = "CONFLICT", message: str = "The request conflicts with current state.") -> None:
        super().__init__(code=code, message=message, status_code=status.HTTP_409_CONFLICT)


class ValidationError(AppError):
    def __init__(self, code: str = "VALIDATION_ERROR", message: str = "Invalid input.") -> None:
        super().__init__(code=code, message=message, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


def error_response(*, code: str, message: str) -> dict:
    return {"detail": {"code": code, "message": message}}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(code=exc.code, message=exc.message),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=error_response(code="VALIDATION_ERROR", message=str(exc.errors()[:5])),
        )

    @app.exception_handler(Exception)
    async def unhandled_handler(request: Request, exc: Exception) -> JSONResponse:
        from app.core.logging import get_logger

        get_logger().exception("Unhandled server error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=error_response(code="INTERNAL_ERROR", message="An unexpected error occurred."),
        )