# Task Tracker API

## Overview

This project is a course-scoped implementation (Module 4 of an AI Assisted Coding course) of a Task Tracker REST API, built with:

- **FastAPI** and **Pydantic v2** for the backend
- A standalone, vanilla HTML/JavaScript Kanban frontend (no build step, no framework)

Task storage is **in-memory**. The backend is authoritative for stored task data and status-transition decisions: the frontend sends changes to the API and displays whatever state the API returns, rather than deciding task state on its own. The frontend remains responsible for display sorting, and both the backend and frontend independently implement the overdue-display rule (see [Search and Filtering](#search-and-filtering)) - the two must be kept synchronized if that rule changes. There is no database, no authentication, and no deployment workflow - this project is not intended for production use.

## Features

- Task create, read, update (partial), and delete (CRUD)
- Server-side search and filtering (`status`, `priority`, `search`, `assignee`, `overdue`)
- Overdue-task filtering, computed on read
- Backend-enforced status-transition rules (invalid transitions rejected with HTTP 422)
- Drag-and-drop Kanban frontend backed by the API
- Automated test suite (`pytest`, via FastAPI's `TestClient`)
- Continuous integration via GitHub Actions
- Docker container support (multi-stage build, non-root runtime user)

## Prerequisites

- **Python 3.11** - the project's target version: both the Docker image (`python:3.11-slim` in `Dockerfile`) and the CI workflow (`python-version: '3.11'` in `.github/workflows/ci.yml`) use it. This repository does not pin a Python version for local development, so confirm your own `python --version` reports 3.11 before creating the virtual environment below.
- **PowerShell** for the commands in this README (Windows).
- **Docker Engine** - optional. Only needed if you want to build/run the container image described below; ordinary local Python development (API, frontend, tests) does not require it.

## Local Setup

From the repository root:

```powershell
python --version
python -m venv venv
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```

Confirm `python --version` reports Python 3.11 before creating `venv\`. Activation (`.\venv\Scripts\Activate.ps1`) is not required for anything in this README: every command below invokes `.\venv\Scripts\python.exe` directly. The `pip install --upgrade pip` / `pip install -r requirements.txt` steps mirror the same two steps `.github/workflows/ci.yml` runs against this repository.

A `.env` file is **not required** to run the API or the tests: `app/main.py` calls `load_dotenv()`, but no application code currently reads the `PORT` or `APP_ENV` values it would provide (see [Environment Variables](#environment-variables)).

## Run the API

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

- API base URL: `http://127.0.0.1:8000`
- Health check: `http://127.0.0.1:8000/health`
- Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`
- Raw OpenAPI document: `http://127.0.0.1:8000/openapi.json`

## Run the Frontend

The frontend is a static HTML/JS file, but it must be **served over HTTP** - do not open `frontend/index.html` directly as a `file://` path. `app/main.py`'s CORS configuration (`allowed_origins`) permits requests only from these four origins:

- `http://localhost:5500`
- `http://127.0.0.1:5500`
- `http://localhost:3000`
- `http://127.0.0.1:3000`

A `file://` page isn't on that list, so the browser blocks the frontend's `fetch()` calls to the API when opened directly.

With the API already running (previous section), serve `frontend/` over HTTP on port 5500 using Python's standard library - no extra install required:

```powershell
.\venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

Then open `http://localhost:5500/` in a browser. The frontend calls the API at a hardcoded `http://localhost:8000` (`API_BASE_URL` in `frontend/index.html`), so the backend must be reachable at that exact address for the board to load tasks.

Display sorting (priority High -> Medium -> Low, then ID) is owned entirely by the frontend; the backend does not sort results. The frontend also evaluates the overdue-display rule on task cards independently of the backend's `?overdue=true` filter - the two implementations must stay synchronized if the rule changes.

## Tests

```powershell
.\venv\Scripts\python.exe -m pytest -v
```

Verified Part 4.4 baseline: **37 passed, 0 failed, 0 skipped**. This is the result of the most recent verification pass against this repository state, not a permanent guarantee - re-run the suite after any change.

## API Reference

| Method | Path | Success | Notable errors |
|---|---|---|---|
| GET | `/health` | 200 | (none) |
| POST | `/tasks` | 201 | 422 - request validation only (e.g. blank/missing title, invalid `due_date`, unknown field) |
| GET | `/tasks` | 200 (including an empty list) | 422 - invalid query value, such as an invalid `status`, `priority`, or `overdue` value |
| GET | `/tasks/{task_id}` | 200 | 404 - no task with that ID |
| PATCH | `/tasks/{task_id}` | 200 | 404 - no task with that ID; 422 - request validation, or a disallowed status transition (see below) |
| DELETE | `/tasks/{task_id}` | 204 (empty body) | 404 - no task with that ID |

HTTP 422 has two distinct causes, and they are not both available on every endpoint:

- `POST /tasks` and `PATCH /tasks/{task_id}` can both return a **framework/Pydantic request-validation** 422 (malformed JSON, wrong field types, an unknown field, or an invalid `due_date`). This response's `detail` is a list of validation-error objects.
- `PATCH /tasks/{task_id}` can additionally return a **business-rule** 422 when `status` is not one of the allowed transitions listed below (`app/business_rules.py`). This response's `detail` is a single descriptive string, not a list.
- `POST /tasks` never produces the business-rule 422 shape - status-transition validation only runs on `PATCH`, because only `PATCH` can change an existing task's status.

The source code and tests establish the complete current behavior; this README summarizes that verified behavior. OpenAPI alone does not currently expose every runtime error response: the current OpenAPI document (`/openapi.json`, `/docs`) declares only the request-validation 422 shape and does not declare 404 at all, even though 404 is real, tested runtime behavior (`tests/test_tasks.py`). Route and model descriptions shown in `/docs` and `/openapi.json` come from the docstrings in `app/main.py` and `app/models.py`.

## Search and Filtering

`GET /tasks` accepts these optional query parameters (`app/storage.py::get_all_tasks`):

- `status` - exact match (`ToDo`, `InProgress`, `Done`)
- `priority` - exact match (`Low`, `Medium`, `High`)
- `search` - case-insensitive substring match against title **or** description
- `assignee` - case-insensitive substring match against assignee
- `overdue` - when `true`, restricts to tasks whose `due_date` is earlier than today **and** whose status is not `Done`

All supplied filters combine using **AND logic**: each active filter narrows the result set further. Blank or whitespace-only `search`/`assignee` values are ignored (treated as not supplied). The backend does **not** sort results - display ordering (priority High -> Medium -> Low, then ID) is owned by the frontend.

## Status-Transition Rules

Only these status transitions are allowed:

| From | To |
|---|---|
| `ToDo` | `InProgress` |
| `InProgress` | `Done` |
| `Done` | `InProgress` |

Any other transition - including `ToDo` to `Done`, `Done` to `ToDo`, and any same-status `PATCH` (e.g. `ToDo` to `ToDo`) - is rejected with **HTTP 422**. This check runs when the `PATCH` body supplies a non-null `status` value.

## Docker

Build the image and run a container, using the image tag and container name established during Part 4.3:

```powershell
docker build --tag task-tracker:dev .
docker run --detach --name tt-dev --publish 8000:8000 task-tracker:dev
```

Verify the container is running and healthy:

```powershell
docker ps --filter "name=tt-dev"
curl.exe --fail --show-error http://localhost:8000/health
docker logs tt-dev
docker inspect --format "{{json .State.Health}}" tt-dev
```

Stop and remove the container when done:

```powershell
docker stop tt-dev
docker rm tt-dev
```

- The container runs as a non-root user (`app`, created in the runtime stage of `Dockerfile`).
- Port 8000 is published, matching the image's `EXPOSE 8000` and the `--port 8000` in its `CMD`.
- The image's `HEALTHCHECK` calls `http://127.0.0.1:8000/health` inside the container every 30 seconds.
- `docker rm tt-dev` removes only the container; the `task-tracker:dev` image is retained on the host afterward.
- `.env` is excluded from the build context (`.dockerignore`: `.env`, `.env.*`), and the application does not currently consume `PORT`/`APP_ENV` in any case (see [Environment Variables](#environment-variables)).

These commands (image tag `task-tracker:dev`, container name `tt-dev`) were successfully exercised during Part 4.3. They were not re-executed during this documentation pass.

## Continuous Integration

`.github/workflows/ci.yml` defines a single `CI` workflow that runs on every `push` and `pull_request`:

1. Check out the repository (`actions/checkout@v7`)
2. Set up **Python 3.11** with pip caching keyed to `requirements.txt` (`actions/setup-python@v7`)
3. Upgrade `pip`
4. Install `requirements.txt`
5. Run `python -m pytest -v`

This workflow only runs the test suite; it does not deploy, publish, measure coverage, or run a linter.

## Environment Variables

`.env.example` declares two placeholder values:

```text
PORT=8000
APP_ENV=development
```

`app/main.py` calls `load_dotenv()`, but **no application code currently reads `PORT` or `APP_ENV`** - they are not functioning configuration today. The API's port (`8000`) comes from the `--port` flag on the `uvicorn` command above; the Docker image's port (`8000`) comes from `EXPOSE 8000` and the `--port 8000` in `Dockerfile`'s `CMD` - independently of these variables.

## Project Structure

```text
app/                          FastAPI backend
  main.py                     Routes, CORS, FastAPI app instance
  models.py                   Pydantic request/response models
  business_rules.py           Status-transition validation
  storage.py                  In-memory task store

frontend/
  index.html                  Standalone Kanban board (vanilla JS, drag-and-drop)

tests/
  test_tasks.py                pytest suite (FastAPI TestClient)
  conftest.py                  Fixtures, storage reset
  verify_a.py                  Manual smoke script (not pytest-collected)

.github/workflows/ci.yml      GitHub Actions CI (Python 3.11, pytest)

docs/decisions/
  in-memory-task-storage.md   Module 4 Part 4.6 storage decision note

docs/documentation/
  claim-vs-reality.md         Module 4 Part 4.4 claim-vs-reality audit

docs/midcourse/                Historical Module 3 course artifacts
                                (design rationale, not current API authority)

docs/reflections/
  module-4-tool-fit-reflection.md   Module 4 tool-fit reflection

Dockerfile                    Multi-stage build; python:3.11-slim runtime
.dockerignore                  Build-context exclusions (env files, docs, tests, frontend, etc.)
```

## Limitations

- All task data is **in-memory** and is lost on every restart.
- No database or persistence layer.
- See [In-Memory Task Storage Decision](docs/decisions/in-memory-task-storage.md) for the rationale, trade-offs, consequences, and open questions behind this design.
- No authentication or authorization.
- No deployment workflow - CI runs tests only.
- The backend does not sort results; sorting is a frontend-only concern.
- CORS allows a fixed, small set of local development origins only (`app/main.py`).
- The OpenAPI document does not currently declare runtime `404` responses, and represents only the framework-validation shape for `422` (see [API Reference](#api-reference)).
- `.env.example`'s `PORT`/`APP_ENV` values are not currently consumed by any application code (see [Environment Variables](#environment-variables)).
