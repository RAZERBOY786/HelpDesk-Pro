from __future__ import annotations

from datetime import datetime, timedelta, timezone


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def ensure_utc(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def add_minutes(base: datetime, minutes: int) -> datetime:
    return ensure_utc(base) + timedelta(minutes=minutes)


def is_past(value: datetime | None, *, now: datetime | None = None) -> bool:
    value = ensure_utc(value)
    if value is None:
        return False
    return value < (now or utcnow())


def minutes_until(value: datetime | None, *, now: datetime | None = None) -> float | None:
    value = ensure_utc(value)
    if value is None:
        return None
    return (value - (now or utcnow())).total_seconds() / 60.0