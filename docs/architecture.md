# Task Tracker Architecture

## System overview

The repository is a course-scoped task tracker complete through Module 4, with Module 5 focused on security, governance, and advanced workflows. It combines a synchronous FastAPI/Pydantic backend with a standalone HTML/JavaScript Kanban frontend and is not presented as production-ready (`AGENTS.md`; `README.md`).

The API provides a health endpoint and create, list, retrieve, partial-update, and delete task operations (`app/main.py`). Task data is process-local memory and disappears when the process terminates (`app/storage.py`).

## Backend structure

- `app/main.py` creates the application, configures four local CORS origins, declares routes, and invokes transition validation.
- `app/models.py` defines task status and priority enums plus create, update, and response models. Create and update requests reject unknown fields.
- `app/business_rules.py` permits only `ToDo -> InProgress`, `InProgress -> Done`, and `Done -> InProgress`; every other supplied transition is rejected with HTTP 422.
- `app/storage.py` stores `TaskResponse` objects in a module-level dictionary and implements CRUD and filtering.

List filters combine with AND logic. Search matches title or description, and assignee matching uses a case-insensitive substring. Blank search and assignee values are ignored. Overdue means a due date earlier than today and a status other than `Done`. Backend results are not sorted (`app/storage.py`).

## Frontend structure

`frontend/index.html` is a static Kanban board with create/edit forms, filters, deletion, and drag-and-drop status changes. It calls the hardcoded `http://localhost:8000` API and must be served from an allowed HTTP origin.

The frontend refreshes tasks after mutations, displays request errors, sorts cards by High, Medium, Low priority and then ID, and independently computes overdue presentation (`frontend/index.html`). Backend and frontend overdue rules must remain synchronized.

## Create-task data flow

1. The frontend trims the form values and rejects a blank title.
2. It sends JSON to `POST /tasks`.
3. FastAPI parses the body as `TaskCreate`; Pydantic applies defaults, strips and validates the title, parses enums and dates, and rejects unknown fields.
4. The route delegates to `storage.add_task`.
5. Storage generates a UUID4 string and one UTC timestamp, constructs a `TaskResponse`, and inserts it into the dictionary.
6. FastAPI returns HTTP 201.
7. The frontend closes the modal and issues `GET /tasks`; the GET response, not the earlier POST body, becomes the rendered board state.

## Testing and verification

`tests/conftest.py` supplies FastAPI's `TestClient` and resets storage before and after each test. `tests/test_tasks.py` contains 37 test functions covering CRUD, validation, filtering, overdue behavior, and selected transition rules. GitHub Actions installs dependencies under Python 3.11 and runs `python -m pytest -v` on pushes and pull requests (`.github/workflows/ci.yml`). The Dockerfile uses a multi-stage Python 3.11 build and a non-root runtime user.

No pytest, browser, CI, or Docker execution was performed during the comparison and drafting phase.

## Known limits

There is no database, persistence, authentication, authorization, or deployment workflow (`README.md`). CORS and the frontend API address are fixed for local development. Dependencies are unpinned, and `.env.example` values are loaded but not consumed by application code.

Static evidence also exposes a contract conflict: `TaskUpdate` permits null `title` and `description`, while `TaskResponse` declares both as strings; storage applies updates through `model_copy`. Existing tests do not cover these null updates, so their runtime API outcome remains unverified (`app/models.py`; `app/storage.py`; `tests/test_tasks.py`).

## Comparison log

### Initial Verdict

Strategy C was provisionally judged most trustworthy for security and correctness-sensitive work because it limited claims to a narrow evidence set and exposed unknowns. Strategy B appeared most complete and fastest for onboarding; Strategy A appeared to offer the best balance of breadth, labels, and practical flow.

### Fact-checked findings

C retained the best file-level accuracy and honesty. B retained the completeness and onboarding advantages, but its Module 4/5 "inconsistency" was not real and its create-flow wording was ambiguous. A was broadly accurate but overstated title and description type guarantees for partial updates.

### Final verdict

Use C's scoped-evidence discipline as the foundation. Add A's end-to-end flow and B's repository-wide onboarding detail only after each expanded claim is checked against the relevant files.

### Two-sentence context rule

For correctness-sensitive, security, or narrowly bounded review tasks, I use Strategy C because targeted evidence and explicit unknowns reduce unsupported claims. For onboarding or cross-cutting planning, I expand toward Strategy B only after verifying each additional claim against the relevant repository files.
