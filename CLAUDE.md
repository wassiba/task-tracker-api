# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Task Tracker API — a course project (AI Assisted Coding course). Baseline is completed through the Module 3 Mid-Course Project (drag-and-drop Kanban board, backend-authoritative status updates, search/filter/overdue support) and is now entering Module 4. Built with FastAPI + Pydantic v2, plus a standalone HTML/JS Kanban frontend. Backend-authoritative by design: scope is deliberately kept small (see `docs/midcourse/mini-adr.md`), and AI-suggested scope creep should be treated with suspicion unless the user asks for it.

## Architecture map

- `app/` — FastAPI backend: `main.py` (routes, CORS, entry point), `models.py` (Pydantic request/response models), `business_rules.py` (status-transition validation), `storage.py` (in-memory task store).
- `frontend/` — standalone `index.html` (Kanban board: vanilla JS, drag-and-drop, fetch calls to the API); `ui-reference/` holds design reference screenshots only, not app code.
- `tests/` — `test_tasks.py` (pytest suite via FastAPI `TestClient`), `conftest.py` (fixtures, storage reset), `verify_a.py` (standalone manual smoke script, not pytest-collected).
- `docs/midcourse/` — course artifacts for the Module 3 milestone: `mini-adr.md` (design decisions/scope boundary), `user-stories.md`, `verification.md`, `reflection.md`, `prompt-log.md`. Reference for rationale, not authoritative API docs.

## Run / Test

Course verification commands:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000   # API at http://127.0.0.1:8000, docs at /docs
.\venv\Scripts\python.exe -m pytest -v                                   # verbose test run (tests/test_tasks.py)
```

Concise alternative for a quick pass/fail check: `.\venv\Scripts\python.exe -m pytest -q`.

Manual smoke check (separate from pytest, not collected by it): `.\venv\Scripts\python.exe tests\verify_a.py`. [VERIFY] its output against the current repository state — not executed as part of this audit.

## Frontend

Do NOT open `frontend/index.html` directly via `file://`. The backend's CORS `allow_origins` (`app/main.py`) lists exactly these four development origins:

- `http://localhost:5500`
- `http://127.0.0.1:5500`
- `http://localhost:3000`
- `http://127.0.0.1:3000`

A `file://` origin isn't on that list, so the browser may block the frontend's `fetch()` calls to the API. Serve the frontend over HTTP from one of the origins above (port 5500 is the conventional choice) instead. [VERIFY] the exact serve command/tool — none is defined in this repo, and this has not been executed to confirm. The frontend itself is hardcoded to call the API at `http://localhost:8000` (`frontend/index.html`, `API_BASE_URL`).

## Known issue

`requirements.txt` lists `httpx2` (not `httpx`) — a suspected invalid dependency entry requiring separate verification, not confirmed as an intentional pin. Don't treat `requirements.txt` as necessarily correct/authoritative without checking. Do not modify `requirements.txt` as part of Part 4.1. Treat any correction as a separate, explicitly approved change that requires dependency-installation and test verification.

## Storage

`app/storage.py` is a pure in-memory module-level dict — no DB. All data is lost on restart. Tests rely on an autouse fixture in `tests/conftest.py` calling `storage._reset()` for isolation.

## Python version

The Module 4 course baseline targets Python 3.11. This repository does not currently contain a Python-version pin. The present local virtual environment reports Python 3.14.6 from `venv/pyvenv.cfg`. Treat Python 3.11 as the course target and Python 3.14.6 as the observed local environment. Verify compatibility and obtain explicit approval before rebuilding the environment or selecting Python versions for CI or Docker.

## Business rules (`app/business_rules.py`, `app/models.py`)

- Status transitions are restricted: only `ToDo→InProgress`, `InProgress→Done`, `Done→InProgress` are allowed. Direct `ToDo↔Done` and same-status transitions are rejected with HTTP 422. This check only fires when a PATCH includes `status`.
- The request models (`TaskCreate`/`TaskUpdate`) omit server-managed fields such as `id`, `created_at`, and `updated_at`, and `extra="forbid"` rejects unexpected input fields. `TaskResponse` contains the server-managed fields.
- Title: stripped, rejected if empty/whitespace-only, max 200 chars.
- Overdue is computed on read, never persisted: `due_date` in the past AND status != Done. Both backend (`?overdue=true`) and frontend independently implement this rule — keep them in sync if it changes.
- `GET /tasks` filters (`search`, `status`, `priority`, `assignee`, `overdue`) combine with AND logic; `search`/`assignee` are case-insensitive substring matches. The backend does not sort results — the frontend owns display sort order (priority High→Medium→Low, then ID).

## Env vars

`.env.example` defines non-secret placeholder values for `PORT` and `APP_ENV`. The inspected application code loads `.env` but does not currently consume either variable. Never assume or document that the real `.env` contains no secrets; do not display or commit it.

## Do not

- Do not add authentication, a database, deployment configuration, secrets, unrelated UI changes, dependencies, plugins, skills, hooks, or development tooling without explicit approval.
- Do not modify `.env` or expose its contents.
- Preserve backend-authoritative validation and existing verified behavior.

## Git workflow

- Check `git status` before changes; review `git diff` before staging.
- Stage only files belonging to the current logical milestone; keep each commit to one logical change.
- Commit subjects: descriptive, imperative, stating the engineering outcome (e.g. "Add X", "Refactor Y", "Fix Z").
- Run relevant browser/API/automated verification before committing.
- Confirm the working tree is clean after committing.
- Create milestone tags only after verification, diff review, and commit completion.
- Never create/switch branches, stage, commit, push, tag, or open PRs without explicit user approval.
- Never rewrite history or discard existing user changes without explicit approval.
