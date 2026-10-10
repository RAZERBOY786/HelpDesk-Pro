# HelpDesk Pro

> A full-stack IT support / help desk platform with a modern glassmorphism UI
> and a production-grade FastAPI backend.

HelpDesk Pro is an end-to-end IT service-management app. Employees submit and
track support tickets, technicians manage the queue and resolve incidents, and
administrators control users, assets, SLA policies, reports, and audit logs.
The frontend is a React + Vite + Tailwind CSS v4 SPA; the backend is a
FastAPI + SQLAlchemy + PostgreSQL service with role-based access control,
token-based authentication, an SLA engine, secure file attachments, and
background scheduling.

---

## ✨ Features

### Frontend (React SPA)

- **Glassmorphism design system** — frosted cards, ambient gradient orbs, and a
  blue → purple light theme with full dark-mode support and a `system` option.
- **Interactive dashboard** — stat cards, SLA health, open/out-of-SLA tickets,
  assigned assets, and technician workload at a glance.
- **Ticket queue** — filterable, searchable All Tickets table with status, SLA,
  priority, category, assignee, and due columns.
- **Ticket intake flow** — guided incident submission with impact/category
  selection, file attachments, and priority hints with SLA estimates.
- **Self-service knowledge base** — asset management, telemetry, and support
  articles with search and category filtering.
- **Full settings suite** — profile, appearance (theme / density / navigation /
  reduced motion / help tips), notifications, security, workspace, SLA, and
  integrations.
- **Preloader & page transitions** — branded card-free glass preloader and
  staggered route animations (respects `prefers-reduced-motion`).
- **Analytics telemetry** — OS/device/browser detection used for render tuning.

### Backend (FastAPI)

- **Authentication & session management** — access + refresh tokens (JWT),
  Argon2 password hashing, session revocation via token-version counters.
- **Role-based access control (RBAC)** — Employee, Technician, Admin with
  field-limited mutation and `404`-style resource hiding.
- **Ticket lifecycle** — Open → Assigned → In Progress → Pending → Resolved →
  Closed with full audit history on every transition.
- **SLA engine** — independent first-response and resolution deadlines per
  priority, idempotent breach/warning tracking, and a scheduled monitor.
- **Asset inventory** — assignment to employees, ticket history, maintenance
  records.
- **Knowledge base articles** for self-help documentation.
- **Secure attachments** — magic-byte verified uploads (PNG/JPEG/GIF/PDF/TXT/LOG)
  stored outside the web root, download requires ticket access.
- **Notifications** — per-user in-app notifications.
- **Reports** — overview, tickets, technicians, and SLA metrics (staff only),
  with CSV export.
- **Audit logs** — full admin audit trail.
- **Health endpoints** — liveness/readiness for orchestrators.

---

## 🏗️ Tech Stack

| Layer            | Technology                          |
| ---------------- | ----------------------------------- |
| Frontend         | React 19, Vite 8, Tailwind CSS v4   |
| Routing          | React Router 7                      |
| Animations       | GSAP (interactive dot-grid)         |
| Backend          | FastAPI (API under `/api/v1`)       |
| ORM              | SQLAlchemy 2.0 + Alembic migrations |
| Database         | PostgreSQL (SQLite for dev/tests)   |
| Validation       | Pydantic v2 + pydantic-settings     |
| Auth             | PyJWT (access + refresh), Argon2    |
| Background tasks | APScheduler / standalone worker     |
| Containerization | Docker, docker-compose              |

---

## 📁 Project Structure

```
HelpDesk Pro/
├── src/                        # React frontend
│   ├── components/             # AppShell, DotBackground/DotGrid, shared UI kit
│   ├── data/                   # dashboard, tickets, knowledge, settings, nav
│   ├── pages/                  # Dashboard, AllTickets, KnowledgeBase,
│   │                           #   SubmitTicket, Settings, Placeholder
│   ├── theme/                  # ThemeProvider (light/dark/system)
│   ├── settings/               # SettingsProvider
│   ├── App.jsx                 # Routes + app shell
│   ├── index.css               # Design tokens, glass system, animations
│   └── main.jsx                # Entry point
├── Backend/                    # FastAPI backend (see Backend/README.md)
│   ├── app/
│   │   ├── api/v1/endpoints/   # Route modules
│   │   ├── core/               # config, security, logging, exceptions
│   │   ├── db/                 # session, base metadata, seed
│   │   ├── models/             # SQLAlchemy tables
│   │   ├── schemas/            # Pydantic models
│   │   ├── services/           # Business rules
│   │   ├── repositories/       # Query encapsulation
│   │   ├── tasks/              # SLA monitor, notification worker, scheduler
│   │   └── utils/
│   ├── alembic/                # Migrations
│   ├── tests/                  # unit / integration / security
│   └── Dockerfile, docker-compose.yml
├── public/                     # favicon, symbol icons
├── q/                          # UI/UX design mockups & design notes (HTML)
├── index.html                  # Shell + card-free glass preloader
├── package.json
└── vite.config.js
```

---

## 🚀 Getting Started

### Prerequisites

- Node.js 20+ and npm
- Python 3.11+ and pip
- PostgreSQL (optional — SQLite works out of the box for local dev)
- Docker (optional — for containerized backend)

### 1. Run the frontend

```bash
npm install
npm run dev
```

Open <http://localhost:5173>.

### 2. Run the backend (local)

```powershell
cd Backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

Copy-Item .env.example .env
# generate a strong JWT secret:
python -c "import secrets; print(secrets.token_urlsafe(64))"

alembic upgrade head
python -m app.db.seed          # SLA policies, admin, demo data (dev only)
uvicorn app.main:app --reload
```

Interactive API docs: <http://localhost:8000/docs> (non-production only).

The seeded administrator comes from `.env`
(`SEED_ADMIN_EMAIL` / `SEED_ADMIN_PASSWORD`). Change it before real use.

### 3. Run the backend with Docker

```powershell
$env:JWT_SECRET_KEY = python -c "import secrets; print(secrets.token_urlsafe(64))"
docker compose up --build
```

Services: `backend` (migrations on start, then serves), `db` (PostgreSQL with a
persistent volume), `worker` (SLA + notification scheduler).

---

## ⚙️ Configuration

All backend settings load from environment variables or `.env` (see
`Backend/.env.example`):

| Variable | Purpose |
| -------- | ------- |
| `DATABASE_URL` | SQLAlchemy DSN (PostgreSQL for prod, SQLite for dev) |
| `JWT_SECRET_KEY` | Token signing key — generate randomly |
| `ACCESS_TOKEN_MINUTES` / `REFRESH_TOKEN_DAYS` | Token lifetimes |
| `FRONTEND_ORIGIN` | CORS origin |
| `UPLOAD_DIR` / `MAX_UPLOAD_SIZE_MB` | Private attachment storage |
| `SMTP_*` / `EMAIL_ENABLED` | Email delivery (falls back to console logs) |
| `SEED_ADMIN_*` | First administrator created by the seed script |

Secrets are never committed — `.env` is git-ignored.

---

## 🔌 API Overview

All endpoints live under `/api/v1`. See `Backend/README.md` for the full table.

| Area | Key endpoints |
| ---- | ------------- |
| Auth  | `POST /auth/login`, `/auth/refresh`, `/auth/logout`, `/auth/forgot-password`, `/auth/reset-password` |
| Users | `GET/POST /users`, `GET/PATCH /users/{id}`, `PATCH /users/{id}/role`, `/status` |
| Tickets | `POST /tickets`, `GET /tickets`, `GET/PATCH /tickets/{id}`, `/assign`, `/comments`, `/history`, `/resolve`, `/close`, `/reopen`, `/attachments` |
| SLA    | `GET/POST /sla/policies`, `PATCH /sla/policies/{id}`, `POST /sla/scan` |
| Assets | `GET/POST /assets`, `GET/PATCH /assets/{id}`, `/assign`, `/tickets`, `/maintenance` |
| Notifications | `GET /notifications`, `PATCH /notifications/{id}/read`, `POST /notifications/read-all` |
| Reports | `GET /reports/overview\|tickets\|technicians\|sla\|tickets.csv` (staff) |
| Knowledge base | `GET/POST /knowledge-base/articles`, `PATCH /knowledge-base/articles/{id}` |
| Admin | `GET /admin/audit-logs` |
| Health | `GET /health/live`, `GET /health/ready` |

---

## 🔐 Roles & Authorization

| Role | Permissions |
| ---- | ----------- |
| **Employee** | Own tickets and assigned assets only |
| **Technician** | All tickets, assignments, staff endpoints, resolution |
| **Admin** | Full administration, SLA policies, audit, reports |

- Reusable dependencies in `app/dependencies.py`:
  `get_current_user`, `require_active_user`, `require_roles`, `require_ticket_access`.
- Rules are enforced in services (`can_view`, `can_resolve`, …), not just routes;
  unauthorized access returns `404` rather than `403` to avoid leaking existence.
- The last active administrator cannot be demoted or disabled.

---

## 🔄 Ticket Lifecycle

```
Open -> Assigned -> In Progress -> Pending -> Resolved -> Closed
                         ^                       |
                         |                       v
                      Reopened <----------------+
```

Every transition records actor, previous/new status, and timestamp in
`ticket_history`. Resolving requires a resolution summary; reopening preserves
the original resolution history.

---

## ⏱️ SLA Engine

- Two independent deadlines per ticket: **first response** and **resolution**.
- Policies live in `sla_policies` (per priority) and are applied at creation.
- `sla_service.scan_ticket_deadlines` records warnings/breaches idempotently
  (one event per `(ticket, type, deadline)`), so the scheduler can run each
  minute. Trigger a manual scan with `POST /api/v1/sla/scan`.

---

## 🧪 Testing

```powershell
# Backend
cd Backend
python -m pytest -q
```

The suite covers unit business rules, integration APIs, and security checks
(ownership, RBAC, file upload, input validation) against an isolated SQLite DB.

```bash
# Frontend lint/build
npm run lint
npm run build
```

---

## ☁️ Deployment / Operations

1. Configure environment variables and a strong `JWT_SECRET_KEY`.
2. Start services: `docker compose up -d` (or a reverse-proxied uvicorn).
3. Run migrations: `alembic upgrade head` (the container does this on start).
4. Create the first administrator securely (seed script or `POST /users`).
5. Logs: `docker compose logs -f backend worker`.
6. Backup: `docker compose exec db pg_dump -U helpdesk helpdesk_db > backup.sql`.
7. Restore: `docker compose exec -T db psql -U helpdesk helpdesk_db < backup.sql`.
8. Roll back: `alembic downgrade -1`, then redeploy the previous image.

Run behind a TLS-terminating reverse proxy, keep containers non-root, and load
secrets from a secret manager in production.

---

## 🛡️ Security Notes

- Generic login errors; passwords hashed with Argon2.
- Short-lived access tokens + refresh tokens; logout revokes sessions via a
  token-version counter.
- Password-reset tokens hashed at rest, single-use, time-limited.
- No plaintext secrets, tokens, or passwords are logged or returned.
- Users cannot set `created_by`, `status`, `assigned_to`, or SLA deadlines via
  create/update payloads.
- Attachments validated by magic bytes (not extension/MIME) and stored private.

---

## 📄 License

Private / internal project.