# 0trace Backend — Agent Instructions

This project is **0trace**, a browser-based hacking/economy/operating-system simulation game. All game mechanics are fictional and exist only within the game environment.

Read **[PLAN.md](PLAN.md)** for the full product specification — operating systems, applications, game mechanics, pre-defined websites, and the complete end-product vision.

## Product Overview

0trace is a browser-based game where players log in, receive a virtual machine running a chosen OS, and interact with a simulated desktop environment. The game features:

- **Three fictional OSes** — FruitOS (macOS-like, paid, polished), DoorsOS (Windows 10-like, default free starter), ArcticOS (Linux/Arch-like, free, customizable with Fruitly/Carpened window managers). Each OS has unique terminal commands, visual themes, and performance buffs/debuffs.
- **Desktop environment** — Movable, resizable windows with close/maximize/minimize buttons, taskbar/dock/panel shell, app launching, and OS-specific shutdown/restart/logout animations.
- **GUI Applications** — Firewall, Waterwall, Cracker, Miner, Mail, Browser, Webserver, Resources (hardware management), Settings, App Store, Terminal, and Skills.
- **Pre-defined in-game websites** — Searchable (search engine), Microhard (DoorsOS company), Pear (FruitOS company), Arctic (ArcticOS community), TechHub (hardware retailer), SecondLife (player marketplace), CryptFront (crypto trading), Domania (domains/certificates), Deliveries (shipping/express delivery).
- **Game mechanics** — Skill & software leveling with XP, money system, hardware trading with delivery times (2h default, 20min express), hardware slot management, crypto mining, password cracking (fictional), player-to-player marketplace.
- **Terminal** — OS-specific commands inspired by real-world equivalents (macOS/Unix for FruitOS, Windows 10 for DoorsOS, Linux/Arch for ArcticOS), including `sudo` privilege system, `ssh` for simulated machine login, and file/directory management.
- **Browser** — In-game web with real HTML/CSS/JS websites (all fictional, no external access), sandboxed user-created content, URL bar defaulting to HTTPS.

All software (Firewalls, Waterwalls, Crackers, Miners, etc.) are stored as files in the simulated filesystem. Leveling software means leveling those specific files, which can then be sold on SecondLife.

## Getting Started

Read **`apps/api/AGENTS.md`** for the detailed, authoritative rulebook covering coding conventions, patterns, and the pre-commit checklist. This file is a high-level project overview.

## Project Structure

```
0trace-backend/
├── apps/
│   └── api/                      # Django application (package: 0trace-api)
│       ├── config/               # Django settings (base, local, production, test)
│       ├── apps/                 # 14 domain Django apps
│       │   ├── common/           # Shared utilities, base models, API helpers
│       │   ├── accounts/         # Auth, signup, login, session, bootstrap
│       │   ├── machines/         # VMs, OS installs, app installs
│       │   ├── filesystem/       # Simulated file trees, permissions
│       │   ├── software/         # Software files, skills, progression
│       │   ├── hardware/         # Hardware catalog, inventory, deliveries
│       │   ├── jobs/             # Async jobs (mining, cracking, delivery)
│       │   ├── economy/          # Coins, wallets, mining, transactions
│       │   ├── networking/       # Simulated SSH, cracking, terminal
│       │   ├── browser/          # In-game web, domains, certificates
│       │   ├── marketplace/      # Player-to-player listings
│       │   ├── communications/   # Mail, messaging
│       │   ├── progression/      # Tutorials, achievements, XP
│       │   └── telemetry/        # Audit logs, security events
│       ├── tests/                # pytest suite (api, schema, seeds, transactions, unit)
│       ├── fixtures/seed/        # YAML seed data definitions
│       ├── openapi/              # Auto-generated OpenAPI spec
│       └── docker/               # Docker entrypoint & gunicorn config
├── docker-compose.yml            # Full stack: mariadb, redis, api, worker
└── .gitignore
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.14+ |
| Framework | Django 6.0 |
| API | Django REST Framework 3.17 |
| Database | MariaDB 11 (production), SQLite (dev/test) |
| Task Queue | Celery 5.6 + Redis 7 |
| API Docs | drf-spectacular 0.29 (OpenAPI 3.0) |
| Testing | pytest 9 + factory-boy + freezegun |
| Server | Gunicorn 23.0 (WSGI) |

## Key Commands

```bash
# All commands run from apps/api/

# Development
python manage.py migrate
python manage.py seed_core
python manage.py runserver

# Docker Compose (from repo root)
docker-compose up

# Testing
pytest

# Checks
python manage.py check
python manage.py makemigrations --check --dry-run
```

## Architecture Overview

- **Views are thin** — business logic in `services/`, read composition in `selectors/`
- **State ownership** — all gameplay state in MariaDB; Redis only coordinates Celery work
- **Atomicity** — `@transaction.atomic` + `select_for_update()` for economy, inventory, marketplace, wallet, domains, certificates, and job state changes
- **Response envelope** — all responses wrapped in `{"data": ...}`; errors as `{"error": {"code": ..., "message": ...}}`
- **All game mechanics are fictional** — no real hacking, SSH, shell execution, crypto, or external network access
- **OpenAPI** — regenerate `openapi/openapi.yaml` when API behavior changes

## API Documentation

When the API is running:
- **Swagger UI:** `/api/v1/api/docs/swagger/`
- **ReDoc:** `/api/v1/api/docs/redoc/`
- **OpenAPI Schema:** `/api/v1/api/schema/`
