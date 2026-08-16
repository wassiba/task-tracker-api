# Repository Instructions

## Project and Current Phase

- This repository contains the Task Tracker API course project.
- The application baseline was completed through Module 4.
- Module 5 added security, governance, architecture, AI-review, and
  personal-playbook evidence.
- The current phase is the Final Project: release verification, documentation
  alignment, and ownership evidence on the `final-project` branch.
- Treat existing application behavior as frozen unless a specific,
  evidence-backed fix receives separate approval.
- Keep the project course-scoped; do not infer production readiness.

## Architecture Map

- `app/` contains the FastAPI and Pydantic backend.
  - `app/main.py` defines the application, routes, and CORS configuration.
  - `app/models.py` defines request, response, status, and priority models.
  - `app/business_rules.py` enforces status-transition rules.
  - `app/storage.py` implements the in-memory task store and filtering.
- `frontend/index.html` is a standalone HTML and JavaScript Kanban frontend.
- `tests/` contains the pytest suite and its fixtures.
- `.github/workflows/ci.yml` defines test-only GitHub Actions CI.
- `Dockerfile` defines a multi-stage Python 3.11 container build.
- `docs/` contains current records and historical course documentation.
- Treat `docs/midcourse/` as Module 3 rationale, not current API authority.

## Authoritative Commands

Run commands from the repository root.

Full local regression suite:

```powershell
.\venv\Scripts\python.exe -m pytest -v
```

Quick pytest check:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Start the API:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Serve the frontend over HTTP:

```powershell
.\venv\Scripts\python.exe -m http.server 5500 --directory frontend
```

- Open the frontend through `http://localhost:5500/`.
- Do not open `frontend/index.html` through `file://`; that origin is not
  allowed by the backend CORS configuration.

## Verified Business Rules

- Allowed status transitions are `ToDo -> InProgress`,
  `InProgress -> Done`, and `Done -> InProgress`.
- Reject every other requested status transition, including same-status
  transitions, with HTTP 422.
- Strip titles and reject missing, non-string, empty, whitespace-only, or
  longer-than-200-character titles through request validation.
- Create and update requests forbid unknown fields.
- `id`, `created_at`, and `updated_at` are server-managed and are not accepted
  by create or update request models.
- A task is overdue when it has a due date earlier than today and its status
  is not `Done`; overdue state is computed rather than stored.
- Supplied task-list filters combine with AND logic.
- Search matches title or description by case-insensitive substring.
- Assignee matching is also a case-insensitive substring operation.
- Blank search and assignee filters are ignored.
- The backend filters but does not sort task results.
- The frontend owns display sorting: priority `High`, `Medium`, `Low`, then ID.
- Backend and frontend independently implement the overdue rule; keep both
  synchronized if an approved change alters that rule.

## Storage and Environment Constraints

- `app/storage.py` stores tasks in a module-level in-memory dictionary.
- All task data is lost when the application process restarts.
- The autouse fixture in `tests/conftest.py` resets storage around every test.
- Never read, display, modify, or commit `.env`.
- `.env.example` contains inspectable non-secret placeholders.
- `.env.example` declares `PORT` and `APP_ENV`, but application code does not
  currently consume either value.
- Python 3.11 is the project, CI, and container target.
- A local virtual environment may use another version; do not treat that as
  the project target or rebuild it without approval.
- `requirements.txt` intentionally declares `httpx2` for this project.
- Do not replace `httpx2` with `httpx` without separate evidence and approval.

## Final Project Working Boundaries

- Read relevant repository evidence before drawing conclusions.
- Default to read-only investigation.
- The Final Project is release- and documentation-first. Do not add product
  features.
- Do not change application code, tests, CI, Docker, dependencies,
  configuration, or unrelated documentation unless a bounded task explicitly
  authorizes a small evidence-backed bug fix, security correction, or required
  release-documentation change.
- Use one bounded objective per Codex task.
- Distinguish verified facts, architectural inference, historical evidence,
  and unverified assumptions.
- Report conflicting evidence instead of silently choosing or reconciling it.
- Do not expand the requested scope.
- Stop at edit approval and consequential-operation approval boundaries.

## Verification Expectations

- Before an approved edit, inspect the relevant files and current Git status.
- After an approved edit, inspect the diff and confirm the affected-file scope.
- Run relevant focused checks for the approved change.
- Run the full regression suite before an approved commit unless the user
  explicitly defines a different verified boundary.
- Report each verification command, exit code, test counts, warnings, and
  post-verification Git status.
- Do not claim browser, Docker, CI, external-service, or runtime verification
  without direct evidence from the current bounded task.

## Git and Approval Boundaries

- Check Git status before changes and review diffs before staging.
- Preserve unrelated user changes and stop if they overlap the requested work.
- Do not create or switch branches, change Git configuration, stage, commit,
  push, pull, fetch, tag, rewrite history, discard changes, or open a pull
  request without explicit approval.
- Stage exact approved file paths; never use broad staging when an exact list
  is available.
- Never force-push.
- Never disable TLS verification.
- Stop when the requested approval boundary is reached.
