from __future__ import annotations

import logging
import sys
from typing import Any

from app.core.config import settings

LOGGER_NAME = "helpdesk"


class RedactingFilter(logging.Filter):
    SENSITIVE = ("password", "authorization", "token", "secret", "cookie")

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            args = record.args
            if isinstance(args, dict):
                sanitized = {
                    k: ("[REDACTED]" if any(s in k.lower() for s in self.SENSITIVE) else v)
                    for k, v in args.items()
                }
                record.args = sanitized
            elif not args:
                record.args = None
        except Exception:
            pass
        return True


def _build_handler() -> logging.Handler:
    handler: logging.Handler
    if settings.environment == "production":
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                '{"time": "%(asctime)s", "level": "%(levelname)s", '
                '"logger": "%(name)s", "message": "%(message)s"}'
            )
        )
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
                datefmt="%Y-%m-%dT%H:%M:%S%z",
            )
        )
    return handler


def configure_logging() -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    root.setLevel(logging.INFO)
    handler = _build_handler()
    handler.addFilter(RedactingFilter())
    root.addHandler(handler)

    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str = LOGGER_NAME) -> logging.Logger:
    configure_logging()
    return logging.getLogger(name)


def log_error(event: Any = None, **fields: Any) -> None:
    get_logger().error(event, extra={"props": fields})