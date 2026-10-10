"""Safe development demo data.

Run with ``python -m app.db.seed``. Idempotent: existing records are reused so
the script can be run repeatedly.
"""

from __future__ import annotations

from app.core import security
from app.core.config import settings
from app.core.logging import get_logger
from app.db.session import SessionLocal
from app.models.asset import Asset
from app.models.enums import AssetStatus, TicketCategory, TicketPriority, TicketStatus, UserRole
from app.models.sla import SLAPolicy
from app.models.ticket import Ticket
from app.models.user import User
from app.services import sla_service
from app.utils.ticket_number import generate_ticket_number

logger = get_logger("app.db.seed")


def ensure_sla_policies(db) -> None:
    existing = {p.priority for p in db.query(SLAPolicy).all()}
    for priority, (response, resolution) in sla_service.DEFAULT_SLA_MINUTES.items():
        if priority not in existing:
            db.add(
                SLAPolicy(
                    priority=priority,
                    response_minutes=response,
                    resolution_minutes=resolution,
                    is_active=True,
                )
            )
    db.commit()


def ensure_admin(db) -> User:
    admin = db.query(User).filter(User.email == settings.seed_admin_email.lower()).first()
    if admin is None:
        admin = User(
            name=settings.seed_admin_name,
            email=settings.seed_admin_email.lower(),
            password_hash=security.hash_password(settings.seed_admin_password),
            role=UserRole.ADMIN,
            department="IT",
            is_active=True,
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)
        logger.info("Created administrator %s", admin.email)
    return admin


def ensure_demo_users(db) -> tuple[User, User]:
    technician = db.query(User).filter(User.email == "tech@example.test").first()
    if technician is None:
        technician = User(
            name="Tina Technician",
            email="tech@example.test",
            password_hash=security.hash_password("Password123!"),
            role=UserRole.TECHNICIAN,
            department="IT Support",
            is_active=True,
        )
        db.add(technician)

    employee = db.query(User).filter(User.email == "employee@example.test").first()
    if employee is None:
        employee = User(
            name="Evan Employee",
            email="employee@example.test",
            password_hash=security.hash_password("Password123!"),
            role=UserRole.EMPLOYEE,
            department="Sales",
            is_active=True,
        )
        db.add(employee)

    db.commit()
    db.refresh(technician)
    db.refresh(employee)
    return technician, employee


def ensure_demo_asset(db, employee: User) -> Asset:
    asset = db.query(Asset).filter(Asset.asset_tag == "LAP-0001").first()
    if asset is None:
        asset = Asset(
            asset_tag="LAP-0001",
            serial_number="SN-EXAMPLE-0001",
            name="MacBook Pro 14",
            model="MacBookPro18,3",
            category="laptop",
            status=AssetStatus.IN_USE,
            assigned_user_id=employee.id,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)
    return asset


def ensure_demo_ticket(db, employee: User, asset: Asset) -> Ticket:
    ticket = db.query(Ticket).filter(Ticket.title == "VPN not connecting").first()
    if ticket is not None:
        return ticket

    from datetime import datetime, timezone

    now = datetime.now(timezone.utc)
    response, resolution = sla_service.get_policy_for_priority(db, TicketPriority.HIGH)
    due_resp, due_res = sla_service.calculate_deadlines(
        now, response_minutes=response, resolution_minutes=resolution
    )
    ticket = Ticket(
        ticket_number=generate_ticket_number(db, when=now),
        title="VPN not connecting",
        description="I cannot connect to the corporate VPN from home since this morning.",
        category=TicketCategory.NETWORK,
        priority=TicketPriority.HIGH,
        status=TicketStatus.OPEN,
        created_by_id=employee.id,
        asset_id=asset.id,
        response_due_at=due_resp,
        resolution_due_at=due_res,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket


def main() -> None:
    db = SessionLocal()
    try:
        ensure_sla_policies(db)
        ensure_admin(db)
        if settings.environment == "development":
            technician, employee = ensure_demo_users(db)
            asset = ensure_demo_asset(db, employee)
            ensure_demo_ticket(db, employee, asset)
            logger.info("Seeded demo data (users, asset, ticket)")
        logger.info("Seed complete")
    finally:
        db.close()


if __name__ == "__main__":
    main()