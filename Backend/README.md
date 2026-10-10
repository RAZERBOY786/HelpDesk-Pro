# HelpDesk Pro — Backend

FastAPI + SQLAlchemy + PostgreSQL backend for the HelpDesk Pro IT support
platform. It powers authentication, employees/technician permissions, tickets,
SLA tracking, asset inventory, notifications, audit logs, reports, and secure
attachments.

The application is designed to run on PostgreSQL in production and on SQLite
for local development and tests.

## Stack

| Layer            | Technology                                   |
| ---------------- | -------------------------------------------- |
| API              | FastAPI (versioned under `/api/v1`)          |
| ORM              | SQLAlchemy 2.0 (typed models)                |
| Migrations       | Alembic                                      |
| Database         | PostgreSQL (`psycopg`), SQLite for dev/tests |
| Validation       | Pydantic v2 + pydantic-settings              |
| Passwords        | `pwdlib` with Argon2                         |
| Tokens           | PyJWT (access + refresh)                     |
| Background tasks | APScheduler / standalone worker              |

## Request flow

```
HTTP -> API routes -> authentication -> authorization (RBAC) -> schemas
     -> services (business rules) -> repositories (queries) -> models
     -> PostgreSQL
                       \-> background tasks (SLA monitor, notifications)
                       \-> audit logging
```

Business logic lives in `app/services`. Route handlers stay thin.

## Project structure

```
backend/
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── dependencies.py         # auth, RBAC, resource access
│   ├── core/                   # config, security, logging, exceptions
│   ├── db/                     # session, base metadata, seed
│   ├── models/                 # SQLAlchemy tables
│   ├── schemas/                # Pydantic request/response models
│   ├── api/v1/endpoints/       # route modules
│   ├── services/               # ticket, SLA, asset, notification, report...
│   ├── repositories/           # query encapsulation
│   ├── tasks/                  # SLA monitor, notification worker, scheduler
│   └── utils/                  # pagination, ticket numbers, datetime helpers
├── alembic/                    # migrations
├── tests/                      # unit / integration / security
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Getting started (local)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
# edit .env and generate a strong JWT secret:
python -c "import secrets; print(secrets.token_urlsafe(64))"

alembic upgrade head
python -m app.db.seed          # SLA policies, admin, demo data (dev only)
uvicorn app.main:app --reload
```

Then open http://localhost:8000/docs (non-production only).

The default seed administrator comes from `.env`
(`SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`). Change it before any real use.

## Configuration

All settings load from environment variables or `.env` (see `.env.example`):

| Variable                                  | Purpose                              |
| ----------------------------------------- | ------------------------------------ |
| `DATABASE_URL`                            | SQLAlchemy DSN                       |
| `JWT_SECRET_KEY`                          | Signing key (generate randomly)      |
| `ACCESS_TOKEN_MINUTES` / `REFRESH_TOKEN_DAYS` | Token lifetimes                  |
| `FRONTEND_ORIGIN`                         | CORS origin                          |
| `UPLOAD_DIR` / `MAX_UPLOAD_SIZE_MB`       | Private attachment storage           |
| `SMTP_*` / `EMAIL_ENABLED`                | Email delivery (disabled logs only)  |

Secrets are never committed. `.env` is git-ignored.

## API overview (all under `/api/v1`)

### Authentication

| Method | Endpoint                | Access              |
| ------ | ----------------------- | ------------------- |
| POST   | `/auth/login`           | Public              |
| POST   | `/auth/refresh`         | Valid refresh token |
| POST   | `/auth/logout`          | Authenticated       |
| POST   | `/auth/forgot-password` | Public              |
| POST   | `/auth/reset-password`  | Valid reset token   |
| GET    | `/users/me`             | Authenticated       |
| PATCH  | `/users/me`             | Authenticated       |
| POST   | `/users/me/password`    | Authenticated       |

### Users

| Method | Endpoint             | Access     |
| ------ | -------------------- | ---------- |
| GET    | `/users`             | Admin      |
| POST   | `/users`             | Admin      |
| GET    | `/users/{id}`        | Admin/self |
| PATCH  | `/users/{id}`        | Admin/self |
| PATCH  | `/users/{id}/role`   | Admin      |
| PATCH  | `/users/{id}/status` | Admin      |

The last active administrator cannot be demoted or disabled.

### Tickets

| Method | Endpoint                 | Access                    |
| ------ | ------------------------ | ------------------------- |
| POST   | `/tickets`               | Authenticated             |
| GET    | `/tickets`               | Permission-filtered       |
| GET    | `/tickets/{id}`          | Authorized viewer         |
| PATCH  | `/tickets/{id}`          | Authorized, field-limited |
| POST   | `/tickets/{id}/assign`   | Admin/technician          |
| POST   | `/tickets/{id}/comments` | Participant               |
| GET    | `/tickets/{id}/comments` | Participant               |
| GET    | `/tickets/{id}/history`  | Authorized viewer         |
| POST   | `/tickets/{id}/resolve`  | Assigned/authorized staff |
| POST   | `/tickets/{id}/close`    | Authorized staff          |
| POST   | `/tickets/{id}/reopen`   | Owner or staff            |

Status transitions are centralized in `app/services/ticket_service.py`.

### SLA, assets, and the rest

- `GET/POST /sla/policies`, `PATCH /sla/policies/{id}`, `POST /sla/scan`
- `GET/POST /assets`, `GET/PATCH /assets/{id}`, `/assets/{id}/assign`,
  `/assets/{id}/tickets`, `/assets/{id}/maintenance`
- `GET /notifications`, `PATCH /notifications/{id}/read`,
  `POST /notifications/read-all`
- `GET /reports/overview|tickets|technicians|sla|tickets.csv` (staff only)
- `GET/POST /knowledge-base/articles`, `PATCH /knowledge-base/articles/{id}`
- `POST /tickets/{id}/attachments`, `GET /attachments/{id}`
- `GET /admin/audit-logs` (admin only)
- `GET /health/live`, `GET /health/ready`

## Roles and authorization

- **Employee** — sees only their own tickets and assigned assets.
- **Technician** — sees all tickets, can be assigned, resolve, and access staff
  endpoints.
- **Admin** — full administration, SLA policy, audit, and reports.

Reusable dependencies in `app/dependencies.py`:
`get_current_user`, `require_active_user`, `require_roles`,
`require_ticket_access`.

Access checks are enforced in services (`can_view`, `can_resolve`, ...), not
just in the routes, and unauthorized records return `404` rather than `403` to
avoid leaking existence.

## Ticket lifecycle

```
Open -> Assigned -> In Progress -> Pending -> Resolved -> Closed
                         ^                       |
                         |                       v
                      Reopened <----------------+
```

Every transition records the actor, previous/new status, and timestamp in
`ticket_history`. Resolving requires a resolution summary; reopening preserves
the original resolution history.

## SLA engine

Two independent deadlines are tracked per ticket: first response and resolution.
Policies live in `sla_policies` (per priority) and are applied at creation time.
`sla_service.scan_ticket_deadlines` records warnings and breaches idempotently
(one event per `(ticket, type, deadline)`), so the scheduler can run every
minute. Run it manually with `POST /api/v1/sla/scan`.

## Attachments

Only PNG, JPEG, GIF, PDF, TXT, and LOG are accepted. Content is verified by
magic bytes (not extension/MIME), size is enforced, files are stored under
`UPLOAD_DIR` outside any public directory, and every download requires ticket
access. Metadata lives in PostgreSQL.

## Testing

```powershell
python -m pytest -q
```

The suite covers unit business rules, integration APIs, and security checks
(ownership, RBAC, file upload, input validation) using an isolated SQLite
database.

## Docker

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"
docker compose up --build
```

Services: `backend` (runs migrations then serves), `db` (PostgreSQL with a
persistent volume), `worker` (SLA + notification scheduler). An optional
`redis` service is stubbed for a future task queue.

## Deployment / operations

1. Configure environment variables and a strong `JWT_SECRET_KEY`.
2. Start services (`docker compose up -d`).
3. Run migrations: `alembic upgrade head` (the container does this on start).
4. Create the first administrator securely (seed script or `POST /users`).
5. Inspect logs: `docker compose logs -f backend worker`.
6. Backup: `docker compose exec db pg_dump -U helpdesk helpdesk_db > backup.sql`.
7. Restore: `docker compose exec -T db psql -U helpdesk helpdesk_db < backup.sql`.
8. Restart a service: `docker compose restart backend`.
9. Roll back: `alembic downgrade -1` then redeploy the previous image.

Run behind a TLS-terminating reverse proxy, keep containers non-root, and load
secrets from a secret manager in production.

## Security notes

- Generic login errors; passwords hashed with Argon2.
- Short-lived access tokens plus refresh tokens; logout revokes sessions via a
  token-version counter.
- Password-reset tokens are hashed at rest, single-use, and time-limited.
- No plaintext secrets, tokens, or passwords are logged or returned.
- Users cannot set `created_by`, `status`, `assigned_to`, or SLA deadlines
  through create/update payloads.
