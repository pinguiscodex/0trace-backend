# 0trace API

RESTful backend for **0trace**, a browser-based fictional operating-system/economy simulation game.

> **⚠️ Disclaimer:** All hacking, cracking, mining, networking, and security mechanics are **purely fictional game mechanics**. No real system commands, real networking, real cryptocurrency, or real security工具 are involved.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | Django 6.0 |
| API | Django REST Framework 3.17 |
| Auth | Session-based (custom `HandleOrEmailBackend`, bcrypt) |
| Task Queue | Celery 5.6 (Redis broker/result backend) |
| Database | MariaDB (production), SQLite (development/test) |
| Server | Gunicorn 23.0 (WSGI), Django ASGI |
| API Docs | drf-spectacular 0.29 (OpenAPI 3.0) |

## Architecture

The API is organized into **11 domain apps** under `apps/api/apps/`:

| App | Purpose |
|-----|---------|
| `accounts` | User signup, login/logout, session, bootstrap |
| `machines` | Virtual machines, OS installs, app installs |
| `filesystem` | Simulated file trees, permissions, read/write |
| `software` | Software files, skill definitions & progression |
| `hardware` | Hardware catalog, inventory, equipment, deliveries |
| `jobs` | Persistent async jobs (mining, cracking, delivery) |
| `economy` | Coins, wallets, mining, transactions |
| `networking` | Simulated SSH, cracking, terminal, security events |
| `browser` | In-game web, domains, certificates, search |
| `marketplace` | Player-to-player marketplace listings |
| `progression` | Tutorials, achievements, XP, skill trees |
| `telemetry` | Audit logs, security event streams |

### API Style

- All responses wrapped in `{"data": ...}` envelope
- Errors returned as `{"error": {"code": ..., "message": ..., "request_id": ...}}`
- Standard pagination for list endpoints
- CSRF-protected session auth

## API Documentation

Interactive API docs are served by the running API:

- **Swagger UI:** `/api/v1/api/docs/swagger/`
- **ReDoc:** `/api/v1/api/docs/redoc/`
- **OpenAPI Schema:** `/api/v1/api/schema/`

## Quick Start (Docker Compose)

```bash
docker compose up
```

Starts MariaDB, Redis, the API (Gunicorn on `:8000`), and a Celery worker. Migrations and core game data seeding run automatically.

## Manual Local Development

```bash
cd apps/api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.lock

# Use SQLite for local dev (no external DB needed)
export DJANGO_USE_SQLITE=1

# Run migrations and seed core game data
python manage.py migrate
python manage.py seed_core

# Start development server
python manage.py runserver
```

### Celery Worker (for async jobs)

```bash
celery -A config.celery worker --loglevel=info
```

Set `CELERY_TASK_ALWAYS_EAGER=1` to run tasks synchronously without Redis.

## Running Tests

```bash
cd apps/api
pytest
```

Tests use an in-memory SQLite database and eager Celery execution.

## Project Structure

```
0trace-backend/
├── docker-compose.yml
└── apps/api/
    ├── config/          # Django settings (base, local, test, production)
    ├── apps/            # Domain apps (see table above)
    ├── docker/          # Dockerfile, entrypoint, gunicorn config
    ├── tests/           # Pytest test suite
    ├── openapi/         # Generated OpenAPI schema
    ├── manage.py
    └── pyproject.toml
```

## Environment Variables

See `apps/api/.env.example` for all available configuration:

- `DJANGO_USE_SQLITE` — use SQLite instead of MariaDB
- `DATABASE_URL` — MariaDB connection string (production)
- `REDIS_URL` — Redis connection string
- `SECRET_KEY` — Django secret key
- `DJANGO_SETTINGS_MODULE` — settings variant (`config.settings.local`, `config.settings.production`)
- `CELERY_TASK_ALWAYS_EAGER` — run Celery tasks synchronously
- `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `CORS_ALLOWED_ORIGINS`

## Contributing

This is a proprietary project. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute.

## Licence

This project is proprietary. All rights reserved. See [LICENCE.md](LICENCE.md) for details.
