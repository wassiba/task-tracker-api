# Architecture B

## 1. System purpose

The Task Tracker is a course-scoped task-management system. A FastAPI backend provides task CRUD, filtering, and status-transition enforcement. A standalone HTML/JavaScript Kanban board consumes that API. It is not presented as production-ready.

## 2. Data model

A task contains:

- `id`: server-generated UUID string
- `title`: required string, trimmed, maximum 200 characters
- `description`: optional on creation; stored as a string
- `status`: `ToDo`, `InProgress`, or `Done`; defaults to `ToDo`
- `priority`: `Low`, `Medium`, or `High`; defaults to `Medium`
- `assignee`: optional string
- `due_date`: optional date
- `created_at` and `updated_at`: server-managed UTC timestamps

Create and update models exclude server-managed fields and reject unknown fields. Updates are partial.

## 3. Create-task request and response flow

1. The frontend sends JSON to `POST /tasks`.
2. FastAPI and Pydantic parse and validate the body as `TaskCreate`.
3. Validation strips the title and rejects missing, non-string, blank, or over-200-character titles. Enum and date validation also occur before route logic.
4. Storage generates a UUID and current UTC timestamp, creates a `TaskResponse`, and places it in the module-level dictionary.
5. The API returns HTTP 201 with the complete task, including ID, defaults, and timestamps.
6. The frontend reloads the task list and renders the returned backend state.

## 4. Key files

- `app/main.py`: application setup, local CORS, health check, and task routes
- `app/models.py`: request, update, response, status, and priority models
- `app/business_rules.py`: allowed status transitions
- `app/storage.py`: in-memory CRUD and filtering
- `frontend/index.html`: Kanban UI and API integration
- `tests/conftest.py`: client fixtures and automatic storage reset
- `tests/test_tasks.py`: 37 backend tests
- `.github/workflows/ci.yml`: Python 3.11 pytest workflow
- `Dockerfile`: multi-stage Python 3.11 container
- `requirements.txt`: declared dependencies

## 5. Validation, storage, and error-handling conventions

Pydantic rejects malformed bodies, invalid enum/date values, and unknown fields with HTTP 422. Status changes are separately checked against `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`; all other transitions, including same-status changes, return a business-rule HTTP 422.

Missing task IDs return HTTP 404. Successful deletion returns HTTP 204. Storage is an in-process dictionary, so data is lost when the process stops.

## 6. Frontend/backend interaction

The frontend calls the hardcoded API base `http://localhost:8000`. It must be served from an allowed local HTTP origin. It sends create, edit, delete, filter, and drag-and-drop status requests to the backend and displays request errors.

The backend filters but does not sort results. The frontend sorts each column by priority—High, Medium, Low—then ID. Backend filtering and frontend display independently calculate overdue as a due date before today with status other than `Done`.

## 7. Testing and verification

The pytest suite contains 37 tests covering CRUD, request validation, filtering, overdue behavior, and transitions. An autouse fixture clears storage before and after each test. CI installs dependencies under Python 3.11 and runs `python -m pytest -v` for pushes and pull requests.

This documentation pass inspected tests and configuration but did not execute pytest, CI, Docker, or browser behavior.

## 8. Known limits

Tasks are not persistent. The maintained README declares no database, authentication, authorization, or deployment workflow. CI runs tests only. CORS is limited to four local-development origins. `PORT` and `APP_ENV` appear in `.env.example`, but application code does not consume them.

## 9. Not visible or unverified assumptions

The permitted evidence does not establish production capacity, concurrent-write behavior, external hosting, security hardening, database migration plans, or browser/container behavior in the current environment.

One wording inconsistency remains: `README.md` describes a Module 4 implementation, while `AGENTS.md` says the project is complete through Module 4 and currently in Module 5. This draft treats that as a documentation-phase discrepancy rather than silently choosing one label.
