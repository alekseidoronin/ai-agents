# AGENTS.md

## Cursor Cloud specific instructions

### Overview

This is a Python/FastAPI application — an AI Agents Platform with Telegram Bot interface. The codebase uses PostgreSQL for data storage, Redis for Celery task queue / caching, and external AI APIs (OpenAI, Anthropic).

### Services

| Service | How to start | Port |
|---|---|---|
| FastAPI app | `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` | 8000 |
| PostgreSQL | `sudo pg_ctlcluster 16 main start` | 5432 |
| Redis | `sudo service redis-server start` | 6379 |

### Dev commands

- **Lint:** `ruff check .`
- **Tests:** `python3 -m pytest tests/ -v`
- **Run app (dev):** `python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **OpenAPI docs:** http://localhost:8000/docs

### Important notes

- PostgreSQL and Redis must be running before starting the app. The app will fail to start if the database is unreachable.
- The `.env` file must exist at the project root with at least `DATABASE_URL` and `REDIS_URL`. API keys (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`) are optional for local dev — core API endpoints work without them.
- The database schema is auto-created by SQLAlchemy's `Base.metadata.create_all()` in `app/main.py` on startup. No manual migration step is needed for basic dev.
- `ruff` and `pytest` are installed as user-level packages (via `pip install --user`). Ensure `~/.local/bin` is on `PATH`.
