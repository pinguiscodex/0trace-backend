# 0trace Backend — Detailed Agent Instructions

This is the authoritative rulebook for all backend work on 0trace. Read this file before making any changes.

Read **[PLAN.md](../../PLAN.md)** for the full product specification — operating systems, applications, game mechanics, pre-defined websites, and the complete end-product vision.

## Product Overview

0trace is a browser-based game where players log in, receive a virtual machine running a chosen OS, and interact with a simulated desktop environment. The backend must support:

- **Three fictional OSes** — FruitOS (macOS-like, paid, -20% crack resistance for attackers), DoorsOS (Windows 10-like, default free starter, -20% processing speed), ArcticOS (Linux/Arch-like, free, +20% processing speed, Fruitly/Carpened window managers).
- **Desktop environment** — Machines, OS installs, app installs, window state (managed by frontend, persisted by backend).
- **GUI Applications** — Firewall, Waterwall, Cracker, Miner, Mail, Browser, Webserver, Resources (hardware management), Settings, App Store, Terminal, Skills. All are files in the simulated filesystem.
- **Pre-defined in-game websites** — Searchable, Microhard, Pear, Arctic, TechHub, SecondLife, CryptFront, Domania, Deliveries. All fictional, no external access.
- **Game mechanics** — Skill & software leveling with XP, money system, hardware trading with delivery times (2h default, 20min express), hardware slot management, crypto mining, password cracking (fictional), player-to-player marketplace.
- **Terminal** — OS-specific commands, `sudo` privilege system, simulated `ssh` login, file/directory management.
- **Browser** — In-game web with real HTML/CSS/JS, sandboxed user-created content, domains, HTTPS certificates.

**Key backend responsibilities:**
- All gameplay state stored in MariaDB (nothing cached except session cookies).
- Session-based auth with bcrypt password encryption.
- REST API with Swagger/OpenAPI documentation.
- Celery async jobs for mining, cracking, delivery, and other time-based operations.
- Atomicity for economy, inventory, marketplace, wallet, domains, certificates, and job state changes.
- All game mechanics are fictional — no real hacking, SSH, crypto, or external network access.

## Framework Rules

- Use **Django**, **DRF**, **Django ORM**, and **MariaDB**-compatible schema design.
- **Never introduce TypeORM** into this Django backend. If TypeORM is needed, it belongs in a separate Node/NestJS service.
- Read checked-in architecture, product, and API contract docs before changing behavior.
- Read official [DRF docs](https://www.django-rest-framework.org/) before changing API behavior.
- Read [drf-spectacular docs](https://drf-spectacular.readthedocs.io/) before changing OpenAPI behavior.
- Read [MariaDB docs](https://mariadb.com/kb/) before database-specific changes.

## Project Structure

Each domain app follows this layout:

```
apps/<domain>/
├── models.py           # Django models (UUIDModel base)
├── serializers.py      # DRF serializers
├── views.py            # Thin API views (APIView, not ViewSets)
├── urls.py             # URL routing
├── selectors.py        # Read composition functions
├── services/           # Business logic (plain functions)
│   ├── __init__.py
│   └── <feature>_service.py
└── migrations/
```

Exceptions: `accounts/` has `backends.py` and `bootstrap_views.py`; `jobs/` has `tasks.py` and `worker.py`; `common/` has sub-packages.

## Coding Conventions

### Models

- All models inherit from `UUIDModel` (which inherits from `TimeStampedModel`).
- UUID primary keys: `id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)`
- Auto-managed timestamps: `created_at`, `updated_at`
- Status fields use `models.TextChoices`
- Explicit `related_name` on all ForeignKey fields
- Define indexes and constraints in `class Meta`

### Services

- **Location:** `apps/<domain>/services/<feature>_service.py`
- Plain functions (not classes), keyword-only arguments with `*,` separator:
  ```python
  def create_wallet(*, user, label: str):
  ```
- Decorate with `@transaction.atomic` for state mutations
- Use `select_for_update()` for economy/inventory operations
- Raise `GameAPIException` with `code`, `status_code`, and optional `details` for business rule violations
- Call `audit(actor=..., event_type=..., request=..., metadata=...)` from telemetry for auditable actions

### Selectors

- **Location:** `apps/<domain>/selectors.py`
- Simple query functions, typically `<entity>_for_user(user)` pattern
- Purpose: read composition, reusable query building

### Views

- **Base class:** `APIView` (not ViewSets)
- One view class per endpoint/action
- Thin — delegate all business logic to services
- Decorated with `@extend_schema(tags=["domain"])` for OpenAPI

### Serializers

- Model serializers: `fields = "__all__"` or explicit field lists
- Input serializers: `serializers.Serializer` with explicit fields
- Custom `validate_<field>` methods or `validate()` for cross-field validation

### API Responses

Use helpers from `apps/common/api/responses.py`:

```python
ok(data, status_code=200)       # {"data": ...}
created(data)                   # {"data": ...} 201
accepted(data, request_id="")   # {"data": ..., "meta": {...}} 202
no_content()                    # 204
```

### Imports

- Standard library first, then Django, then DRF, then local apps
- Local imports use full path: `from apps.economy.models import Wallet`
- Service imports at view level: `from .services.wallet_service import create_wallet`
- Use `from __future__ import annotations` in newer files for type hints

### Naming

- **Files:** `snake_case.py` (e.g., `wallet_service.py`)
- **Classes:** `PascalCase` with role suffix (`...View`, `...Serializer`, `...Model`)
- **Functions:** `snake_case` with verb-first naming (`create_wallet`, `transfer`)
- **Services:** `<feature>_service.py`

## State Ownership

- **All authoritative gameplay state lives in MariaDB.**
- Redis/RabbitMQ may only coordinate Celery work — never own gameplay state.
- The backend is authoritative for: identity, machines, inventory, apps, jobs, wallets, domains, mail, achievements, notifications, and economy.

## Atomicity Rules

Use `@transaction.atomic` + `select_for_update()` for state changes in:
- Economy (wallets, balances, transfers, mining payouts)
- Inventory (hardware, software, equipment)
- Marketplace (listings, purchases)
- Domains and certificates
- Job state transitions

## Security Rules

All game mechanics are fictional. Do not implement:
- Real hacking, real password cracking, real SSH
- Shell execution or OS command execution
- Crypto/blockchain integrations or wallet providers
- Network scanning or malware-like behavior
- Arbitrary external website fetching

Terminal, SSH, IPs, wallets, mining, cracking, domains, certificates, webservers, and browsing are game records and service logic only.

## Testing

### Configuration

- Framework: pytest + pytest-django
- Settings: `config.settings.test` (SQLite in-memory, fast password hasher, eager Celery)
- Config: `pytest.ini` and `[tool.pytest.ini_options]` in `pyproject.toml`

### Test Organization

```
tests/
├── conftest.py           # Global fixtures (seeded, api_client)
├── api/                  # API endpoint integration tests
├── transactions/         # Cross-domain transactional tests
├── unit/                 # Pure unit tests
├── seeds/                # Seed data idempotency tests
└── schema/               # OpenAPI schema generation tests
```

### Test Conventions

- Markers: `@pytest.mark.django_db` or `@pytest.mark.django_db(transaction=True)`
- Naming: `test_<scenario_describes_behavior>()`
- Pattern: Arrange-Act-Assert with direct ORM setup and service calls
- Use `seeded` fixture for seed data, `User.objects.create_user()` for users
- Assertions: direct `assert` statements, `pytest.raises(Exception)` for expected failures

### Fixtures

```python
@pytest.fixture
def seeded(db):
    call_command("seed_core", verbosity=0)

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()
```

## Common Utilities

Located in `apps/common/services/`:

- `ids.py` — `new_uuid()`, `short_code(prefix)` for generating IDs
- `money.py` — `money(value)`, `require_non_negative(value)` for decimal handling
- `clocks.py` — `now()` wrapper for `timezone.now()`

## Docker

- **Dockerfile:** `python:3.14-slim` base, installs from `requirements.lock`
- **Entrypoint:** runs `migrate --noinput` then `seed_core` before starting the server
- **Gunicorn:** binds to `0.0.0.0:8000`, 3 sync workers, 60s timeout
- **docker-compose.yml:** mariadb:11, redis:7-alpine, api, worker services

## Pre-Commit Checklist

Before considering work complete, run all of the following:

```bash
# From apps/api/

# 1. Django checks
python manage.py check

# 2. Migration check (no uncommitted migrations)
python manage.py makemigrations --check --dry-run

# 3. Run migrations
python manage.py migrate

# 4. Run tests
pytest

# 5. Regenerate OpenAPI schema (if API behavior changed)
python manage.py spectacular --file openapi/openapi.yaml

# 6. Validate schema (if present)
python manage.py spectacular --validate

# 7. Seed idempotency
python manage.py seed_core
```

Also run lint/static checks when present.
