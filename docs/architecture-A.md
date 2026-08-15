# Task Tracker Architecture — Strategy A Draft

## 1. System purpose

**Verified:** The repository implements a course-scoped task-tracking application: a FastAPI REST backend and a standalone HTML/JavaScript Kanban board. It supports task creation, retrieval, filtering, partial updates, deletion, and controlled status transitions. It is not presented as production-ready.

## 2. Data model

**Verified:** A task contains:

- Server-managed `id`, `created_at`, and `updated_at`
- Required `title`
- `description`, defaulting to an empty string
- Status: `ToDo`, `InProgress`, or `Done`
- Priority: `Low`, `Medium`, or `High`
- Optional `assignee` and `due_date`

Create and update models exclude server-managed fields and reject unknown fields. Stored tasks use the response model. IDs are UUID4 strings; timestamps are UTC datetimes.

## 3. Create-task request and response flow

**Verified flow:**

1. The frontend reads and locally checks the task form.
2. It sends JSON in `POST /tasks`.
3. FastAPI parses the body as `TaskCreate`; Pydantic applies defaults and validation.
4. `create_task()` delegates to `storage.add_task()`.
5. Storage generates the UUID and timestamps, constructs a `TaskResponse`, and inserts it into the module-level task dictionary.
6. FastAPI returns the task with HTTP 201.
7. On success, the frontend closes the modal and refreshes the board with `GET /tasks`.

**Architectural inference:** Request handling is synchronous because the inspected route and storage functions are ordinary `def` functions.

## 4. Key files

- `app/main.py`: application, CORS, health check, and task routes
- `app/models.py`: enums and Pydantic request/response models
- `app/business_rules.py`: allowed status transitions
- `app/storage.py`: in-memory CRUD and filtering
- `frontend/index.html`: static Kanban UI and API client
- `tests/conftest.py`: API client and storage-reset fixtures
- `tests/test_tasks.py`: endpoint behavior tests
- `.github/workflows/ci.yml`: test-only CI
- `Dockerfile`: Python 3.11 multi-stage container

## 5. Validation, storage, and error-handling conventions

**Verified:** Titles are stripped and must be strings containing 1–200 non-whitespace characters. Model enums constrain status and priority; Pydantic parses dates and rejects unknown request fields. Invalid request data is tested as HTTP 422.

Storage is a module-level dictionary and is cleared when the process ends. Updates apply only explicitly supplied fields. Allowed status changes are `ToDo → InProgress`, `InProgress → Done`, and `Done → InProgress`; other transitions return 422. Missing task IDs return explicit 404 errors. Successful deletion returns an empty 204 response.

## 6. Frontend/backend interaction

**Verified:** The browser calls the hardcoded `http://localhost:8000` API using `fetch`. Backend CORS permits four local origins on ports 5500 and 3000. The frontend issues POST, GET, PATCH, and DELETE requests, displays server errors, and refreshes tasks after mutations. Server-side filters are encoded as query parameters. The frontend owns priority/ID display sorting and independently calculates overdue presentation.

## 7. Testing and verification

**Verified:** Pytest uses FastAPI’s `TestClient`. An autouse fixture clears storage before and after every test. The inspected suite covers creation, validation, filtering, retrieval, partial updates, transition rules, deletion, and error responses. CI uses Python 3.11, installs `requirements.txt`, and runs `python -m pytest -v`.

**Unverified in this task:** No tests, CI jobs, browser checks, or container commands were executed.

## 8. Known limits

- In-memory data disappears on restart.
- No database or persistence layer is visible.
- No authentication or authorization mechanism appears in the inspected application.
- CORS and the frontend API address are fixed for local development.
- Dependencies are not version-pinned.
- CI tests only; it does not deploy, lint, or report coverage.
- Backend and frontend overdue logic must remain synchronized.

## 9. Not visible or unverified assumptions

Database migration strategy, multi-process consistency, concurrent-write behavior, observability, rate limiting, secrets management, deployment topology, scaling, availability, and production security controls are not established by the inspected evidence.
