"""Email delivery.

In development (``EMAIL_ENABLED=false``) messages are logged instead of sent so
the workflow can be exercised without an SMTP server. Failures are swallowed on
purpose: an email problem must never roll back an already-committed ticket
change.
"""

from __future__ import annotations

import smtplib
from email.message import EmailMessage

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("app.email")


def send_email(*, to: str, subject: str, body: str) -> bool:
    if not settings.email_enabled:
        logger.info("Email disabled; would send to=%s subject=%s", to, subject)
        return True

    message = EmailMessage()
    message["From"] = settings.email_from
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=10) as smtp:
            if settings.smtp_username:
                message_login = message
                smtp.starttls()
                smtp.login(settings.smtp_username, settings.smtp_password)
            smtp.send_message(message)
        logger.info("Sent email to=%s subject=%s", to, subject)
        return True
    except Exception:
        logger.exception("Failed to send email to=%s", to)
        return False