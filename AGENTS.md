# Agent Guide

## Setup and Commands

- Use Python `3.13.x` and `uv`; install/sync dependencies with `uv sync`.
- The ASGI entrypoint is `main:app`; run locally with `uv run uvicorn main:app --reload`.
- There is no configured lint, formatter, or test runner in `pyproject.toml`; do not assume `pytest` is the project test command.
- A lightweight syntax check is `uv run python -m compileall apps core migrations main.py`.

## Configuration

- Settings load `.env` with case-sensitive names and forbid unknown variables. Development requires `ENVIRONMENT=development`, `DB__PASSWORD`, and `DB__NAME`; start from `.env.example`.
- `ENVIRONMENT=development` uses local file storage under `media/`; `ENVIRONMENT=production` requires all four `GCS_*` values in `.env.example` and converts literal `\\n` in `GCS_PRIVATE_KEY` to newlines.
- Do not commit `.env` or credentials. The default `SECRET_KEY` is a placeholder and must be replaced for real deployments.

## Structure

- `main.py` imports both feature routers, mounts `/static`, and loads models before creating the app. `apps/blog` and `apps/users` own feature routers, schemas, and models.
- `core/settings` selects development or production settings from `ENVIRONMENT`; `core/database` owns the SQLAlchemy engine/session/base and `load_models()` imports both model modules.
- Templates are loaded from `templates/` and static files from `static/`; these paths are required by the application at startup.

## Database

- Alembic is configured in `pyproject.toml` with scripts in `migrations/`; its environment derives the async PostgreSQL URL from application settings and loads models for autogeneration.
- With a reachable configured database, apply migrations using `uv run alembic upgrade head`; generate one with `uv run alembic revision --autogenerate -m "description"`, then inspect the revision before applying it.
