"""Scheduled task registration.

Uses APScheduler when available; otherwise falls back to a simple blocking
loop. Run as a standalone process (see the ``worker`` service in
``docker-compose.yml``) so scheduled jobs never block API workers.
"""

from __future__ import annotations

from app.core.logging import get_logger
from app.tasks import notification_worker, sla_monitor

logger = get_logger("app.tasks.scheduler")

SLA_INTERVAL_SECONDS = 60
NOTIFICATION_INTERVAL_SECONDS = 60


def _try_apscheduler():  # pragma: no cover - optional dependency
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except Exception:  # noqa: BLE001
        return None

    scheduler = BackgroundScheduler()
    scheduler.add_job(
        sla_monitor.run_once,
        "interval",
        seconds=SLA_INTERVAL_SECONDS,
        id="sla_monitor",
        max_instances=1,
        coalesce=True,
    )
    scheduler.add_job(
        notification_worker.process_once,
        "interval",
        seconds=NOTIFICATION_INTERVAL_SECONDS,
        id="notification_worker",
        max_instances=1,
        coalesce=True,
    )
    return scheduler


def run() -> None:  # pragma: no cover - runtime entry point
    scheduler = _try_apscheduler()
    if scheduler is not None:
        logger.info("Starting APScheduler worker")
        scheduler.start()
        import time

        try:
            while True:
                time.sleep(3600)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
        return

    logger.info("APScheduler not installed; running blocking loop")
    import time

    from app.db.session import SessionLocal

    while True:
        try:
            sla_monitor.run_once()
            db = SessionLocal()
            try:
                notification_worker.process_once(db)
            finally:
                db.close()
        except Exception:  # noqa: BLE001
            logger.exception("Scheduled iteration failed")
        time.sleep(SLA_INTERVAL_SECONDS)


if __name__ == "__main__":  # pragma: no cover
    run()