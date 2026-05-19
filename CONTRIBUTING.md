# Contributing to 0trace Backend

Thank you for your interest in contributing to 0trace. This document provides guidelines and instructions for contributing to the backend repository.

> **Note:** This is a proprietary project. All contributions are subject to the terms outlined in [LICENCE.md](LICENCE.md). By contributing, you agree that your contributions will be licensed under the same proprietary terms.

## Code of Conduct

- Treat all team members with respect.
- Keep discussions focused and constructive.
- Do not share proprietary code or project details outside the team.

## Getting Started

1. Read the [README.md](README.md) for an overview of the project and setup instructions.
2. Read `apps/api/AGENTS.md` for detailed coding conventions and patterns.
3. Set up your local development environment following the Quick Start guide.

## Development Workflow

### Branching

- Create feature branches from `main` using the naming convention: `feature/<description>`, `fix/<description>`, or `refactor/<description>`.
- Keep branches focused on a single task or feature.

### Commit Messages

Use conventional commit format:

```
<type>: <description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
- `feat: add password cracking job endpoint`
- `fix: resolve CSRF token rotation issue`
- `docs: update API documentation for marketplace app`

### Code Style

- Follow PEP 8 for Python code.
- Views should be thin — place business logic in `services/` and read composition in `selectors/`.
- Use `@transaction.atomic` and `select_for_update()` for state-changing operations.
- All API responses must use the `{"data": ...}` envelope.
- Errors must follow the `{"error": {"code": ..., "message": ...}}` format.

### Before Submitting

Run the following checks before committing:

```bash
cd apps/api
pytest
python manage.py check
python manage.py makemigrations --check --dry-run
```

Ensure:
- All tests pass.
- No migration files are missing.
- OpenAPI spec is regenerated if API behavior changed.

## Architecture Guidelines

- All gameplay state is stored in the database (MariaDB). Redis is only for Celery coordination.
- All game mechanics are fictional — no real hacking, networking, or crypto.
- Use generated types and avoid inventing DTOs.

## Reporting Issues

- Use the issue tracker to report bugs or request features.
- Include steps to reproduce, expected behavior, and actual behavior for bugs.
- Reference relevant files and line numbers when possible.
