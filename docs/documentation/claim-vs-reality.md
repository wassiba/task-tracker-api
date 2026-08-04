# Module 4 Part 4.4 - Claim-versus-Reality Audit

**Date:** 2026-08-04
**Project:** Task Tracker API
**Branch:** `mid-course-project`
**Baseline commit before Part 4.4:** `10ec331` ("Add Docker container configuration")

No Part 4.4 commit hash is recorded here because no commit has been made yet as of this audit.

## Purpose and Scope

This document records a systematic comparison between the documentation produced or revised during Module 4 Part 4.4 (DOC1: source docstrings; DOC2: `README.md`) and the actual repository/runtime behavior, as established by source code, the automated test suite, and live HTTP/CORS checks performed against locally-run instances during this Part 4.4 session.

Scope covers: `README.md`, the four `app/` source files touched by DOC1 (`main.py`, `business_rules.py`, `storage.py`, `models.py`), and the claims those files make about routes, validation, storage, filtering, CORS, Docker, CI, and environment variables. `CHANGELOG.md`, `API_SUMMARY_CHECKLIST.md`, and `docs/midcourse/*.md` are treated as historical, point-in-time records and are referenced but not re-validated as current API authority.

## Evidence-Source Classification

| Evidence type | What counts | Example in this audit |
|---|---|---|
| Repository evidence | Source files and tests as committed/present in the working tree | `app/business_rules.py`, `tests/test_tasks.py` |
| Execution evidence | Output of commands actually run this session (pytest, `TestClient` calls, live HTTP requests) | `37 passed in 1.00s`; live `/health` response |
| User-confirmed visual evidence | Browser rendering the user directly observed and reported | `/docs` and `http://localhost:5500/` rendering correctly |
| Prior-session evidence | Facts asserted about work completed in an earlier session, not reproducible from files in this repository | Part 4.3 Docker command verification (`task-tracker:dev` / `tt-dev`) |

Where a claim's evidence is prior-session or user-supplied rather than independently retrieved from a repository file in this audit, that is stated explicitly in the table below - it is not presented as independently repository-verified.

## Audit Methodology

1. Read the current working-tree content of `README.md` and all four DOC1-touched `app/` files in full.
2. Cross-referenced every material claim against: the exact source line(s) implementing it, the named test(s) covering it (where one exists), `CLAUDE.md`, `.env.example`, `requirements.txt`, `Dockerfile`, `.dockerignore`, `.github/workflows/ci.yml`, and `frontend/index.html`.
3. Re-ran the full automated test suite this session (`pytest -v`) to confirm the currently-documented baseline.
4. Where a claim was plausible from the code but not covered by an existing named test (the `GET /tasks?overdue=<invalid>` -> 422 case), verified it directly via an in-process `TestClient` call - the same mechanism the existing test suite already uses, not a running server.
5. Reused this session's earlier live-server evidence (health, OpenAPI, `/docs`, frontend, CORS) rather than re-starting servers for this audit stage.
6. Flagged, rather than silently accepted, any claim whose evidence originates outside this repository (Docker/Part 4.3).

## Claim-versus-Reality Table

| ID | Origin | Claim | Repository/runtime reality | Evidence | Status | Resolution |
|---|---|---|---|---|---|---|
| C-01 | Pre-existing | Backend built with FastAPI + Pydantic v2 | `requirements.txt` lists `fastapi`, `pydantic`; `app/models.py` uses Pydantic v2 `field_validator`/`ConfigDict` | Repository evidence | Verified accurate | none needed |
| C-02 | Pre-existing | Task storage is in-memory, lost on restart | `app/storage.py`: module-level `_tasks: dict[str, TaskResponse] = {}`, no DB/ORM import anywhere in `app/` | Repository evidence | Verified accurate | none needed |
| C-03 | Pre-existing | `app/main.py` module docstring and `FastAPI(description=...)` described the app as a Module 1, `/health`-only service | Repository now implements full CRUD, filtering, CORS, and status-transition validation across 5 additional routes | Repository evidence (pre-Part-4.4 file content vs. current) | **Corrected** (DOC1) | Module docstring and `description=` rewritten to describe current scope |
| C-04 | Pre-existing | README instructed opening `frontend/index.html` directly via `file://` | `app/main.py`'s `allowed_origins` CORS list contains no `file://` entry; a `file://` page's `fetch()` calls are blocked by the browser | Repository evidence (CORS list) + execution evidence (this session's CORS check) | **Corrected** (DOC2) | README's "Run the Frontend" section rewritten to require serving over HTTP on an allowed origin |
| C-05 | DOC2 | CORS permits exactly 4 origins (`localhost`/`127.0.0.1` on 5500 and 3000) | `app/main.py::allowed_origins`, 4 entries, matches README list exactly | Repository evidence | Verified accurate | none needed |
| C-06 | Pre-existing/DOC2 | Frontend calls a hardcoded `http://localhost:8000` | `frontend/index.html:733`: `const API_BASE_URL = "http://localhost:8000";` | Repository evidence + execution evidence (live frontend fetch confirmed against running API) | Verified accurate | none needed |
| C-07 | DOC2 | Backend is authoritative for stored data/status decisions; frontend sends changes and displays returned state rather than deciding locally | `frontend/index.html:795-803` (and other fetch sites): each mutating action `await fetch(...)`, checks `response.ok`, then re-renders from the response/refetch | Repository evidence | Verified accurate | none needed |
| C-08 | Pre-existing/DOC2 | Backend does not sort; display sorting is frontend-owned | `app/storage.py::get_all_tasks` has no `sorted()`/`.sort()` call | Repository evidence | Verified accurate (also see C-13, Known limitation) | none needed |
| C-09 | DOC2 | Backend and frontend independently implement the overdue-display rule; must stay synchronized | `app/storage.py:97-107` (`due_date < today and status != Done`) and `frontend/index.html:988-991` (`isTaskOverdue`: `!task.due_date \|\| task.status === "Done"` -> not overdue) are two separate implementations of the same rule | Repository evidence | Verified accurate | none needed |
| C-10 | DOC1/DOC2 | `GET /tasks` filters combine with AND logic | `app/storage.py::get_all_tasks` applies each filter as a sequential list-comprehension narrowing; tests `test_list_tasks_status_and_priority_combine_with_and_logic`, `test_list_tasks_all_filters_combine_with_and_logic` (both passed this session) | Repository evidence + execution evidence | Verified accurate | none needed |
| C-11 | DOC1/DOC2 | Blank/whitespace `search`/`assignee` are ignored | `app/storage.py:79,88`: `search.strip().casefold()` truthiness gate; tests `test_list_tasks_blank_or_whitespace_search_is_ignored`, `test_list_tasks_blank_or_whitespace_assignee_is_ignored` (passed) | Repository evidence + execution evidence | Verified accurate | none needed |
| C-12 | DOC1/DOC2 | Overdue = `due_date` earlier than today AND status not `Done` | `app/storage.py:97-107`; test `test_list_tasks_overdue_returns_only_overdue_unfinished_tasks` (passed) | Repository evidence + execution evidence | Verified accurate | none needed |
| C-13 | Current accepted limitation | Backend does not sort results | Same evidence as C-08 | Repository evidence | Known limitation | Documented in README Limitations; not something to "fix" |
| C-14 | Current accepted limitation | OpenAPI does not declare runtime 404 responses | Live `/openapi.json` this session: `GET/PATCH/DELETE /tasks/{task_id}` response-code sets are `{200,422}`/`{200,422}`/`{204,422}` - no `404` anywhere, while `tests/test_tasks.py` has three passing tests that assert real 404 responses | Execution evidence (live OpenAPI dump, this session) | Known limitation | Documented in README API Reference and Limitations |
| C-15 | Current accepted limitation | OpenAPI documents only the framework-validation 422 shape, not the business-rule string-detail shape | Live `/openapi.json`: `PATCH /tasks/{task_id}`'s only declared `422` references `#/components/schemas/HTTPValidationError`; `app/business_rules.py` raises `HTTPException(422, detail=<f-string>)`, a single string, not a `HTTPValidationError`-shaped list | Execution evidence (live OpenAPI dump) + repository evidence | Known limitation | Documented in README API Reference and Limitations |
| C-16 | Current accepted limitation | `.env.example` declares `PORT`/`APP_ENV`, which the app does not consume | Exhaustive search of `app/` this session and prior sessions found no `os.getenv`/`os.environ` reference to either name; `app/main.py` only calls `load_dotenv()` | Repository evidence | Known limitation | Documented in README Environment Variables and Limitations |
| C-17 | Historical record intentionally left unchanged | `docs/midcourse/*.md`, `CHANGELOG.md`, `API_SUMMARY_CHECKLIST.md` describe earlier module milestones | Not re-validated against current code as if they were live API docs; `CHANGELOG.md` stops at v0.4 (pre-CI/Docker), `API_SUMMARY_CHECKLIST.md` predates `due_date`/search/filter fields | Repository evidence | Out of scope (by design) | None proposed; explicitly excluded from Part 4.4 edits per prior-stage scope decision |
| C-18 | DOC1/DOC2 | Success codes 200 (health/get/list/patch), 201 (create), 204 (delete) are correct per route | `app/main.py` decorators' `status_code=` values; live OpenAPI dump this session confirms each route's success code matches | Repository evidence + execution evidence | Verified accurate | none needed |
| C-19 | DOC1/DOC2 | 404 is real, tested runtime behavior for get/patch/delete-by-id | `tests/test_tasks.py`: `test_get_task_by_id_not_found_returns_404_with_detail`, `test_patch_not_found_returns_404`, `test_delete_missing_returns_404` - all passed this session | Execution evidence | Verified accurate | none needed |
| C-20 | DOC2 | `POST` can only return the framework-validation 422; only `PATCH` can return the business-rule 422 | `app/main.py::create_task` body is a single line with no call to `validate_status_transition`; only `update_task` calls it | Repository evidence | Verified accurate | none needed |
| C-21 | DOC2 (this-session correction) | The status-transition check runs when `PATCH` supplies a non-null `status` value (not merely "includes a status field") | `app/main.py:183`: `if payload.status is not None:` | Repository evidence | **Corrected** (README + `update_task` docstring wording, applied this session) | Wording aligned to the exact condition |
| C-22 | DOC2 | CI runs on every `push`/`pull_request`, uses Python 3.11, runs `python -m pytest -v` | `.github/workflows/ci.yml`: `on: push, pull_request`; `python-version: '3.11'`; final step `run: python -m pytest -v` | Repository evidence | Verified accurate | none needed |
| C-23 | DOC2 | API/Docker both fix port 8000 independently of `.env.example`'s `PORT` | `uvicorn ... --port 8000` (README, CLAUDE.md); `Dockerfile`: `EXPOSE 8000` and `CMD [...,"--port","8000"]` | Repository evidence | Verified accurate | none needed |
| C-24 | DOC1 | Component-schema `description` fields for `TaskCreate`/`TaskUpdate`/`TaskResponse`/`TaskStatus` were populated by the DOC1 class docstrings, as a documentation-only effect (no field/type/required change) | Live `/openapi.json` this session: those four schemas' `description` matches the DOC1 docstrings verbatim; `required`/`properties`/`enum` values match `app/models.py` unchanged; `TaskPriority`/`HTTPValidationError`/`ValidationError` remain without descriptions | Execution evidence (live OpenAPI dump) | Verified accurate | none needed - explicitly not a schema-field or behavioral change |
| C-25 | DOC2 | Docker commands (`docker build --tag task-tracker:dev .`, `docker run --detach --name tt-dev --publish 8000:8000 ...`, health/log/stop/remove) are consistent with `Dockerfile` and were exercised successfully in Part 4.3 | Command syntax matches `Dockerfile`'s `EXPOSE 8000`, non-root `app` user, and `HEALTHCHECK` target exactly; **execution** of these commands was **not** performed in this Part 4.4 session and is not recorded in any repository file (`CHANGELOG.md`/`docs/midcourse/` have no Part 4.3 verification log) | Repository evidence (syntax only) + prior-session/user-asserted evidence (execution) | Verified accurate (syntax); execution evidence is prior-session, not repository-embedded | None - already stated transparently in README/prior DOC2 report |
| C-26 | DOC2 | `GET /tasks` 422 covers invalid `status`, `priority`, or `overdue` query values (non-exhaustive "such as" wording) | `status`/`priority` covered by passing named tests; `overdue` was **not** covered by an existing named test, so verified this session via a direct `TestClient` call: `GET /tasks?overdue=not-a-boolean` -> `422`, `bool_parsing` validation error | Execution evidence (this session's `TestClient` check; not from an existing named test) | Verified accurate | none needed - noted here that the `overdue` case relied on an ad hoc check, not a named regression test |

## Corrected Inaccuracies

Two genuine, independently-assessed pre-Part-4.4 inaccuracies were found and corrected:

1. **`app/main.py`'s module docstring and `FastAPI(description=...)`** described the application as implementing only a Module 1 `/health` endpoint ("It currently does only one thing... Nothing else... This follows the Module 1 requirement exactly"). By the time of Part 4.4, the file implemented a full CRUD API with search/filter/overdue support and status-transition enforcement across six routes. **Corrected in DOC1** by rewriting both the module docstring and the `description=` string to describe the current scope, verified live via `/openapi.json`'s `info.description` this session.
2. **The former `README.md`** instructed: "Open `frontend/index.html` in a browser while the API is running" - a `file://` origin is not on `app/main.py`'s CORS allowlist, so this would silently fail the frontend's `fetch()` calls. **Corrected in DOC2** by rewriting the "Run the Frontend" section to require serving `frontend/` over HTTP on an allowed origin (port 5500), which was then live-verified this session (HTTP 200, correct content, user-confirmed visual rendering, and a successful CORS check from that exact origin).

No additional inaccuracies were invented to inflate this count; the audit in the table above found the remaining documentation (post-DOC1/DOC2) to be accurate against current repository and runtime evidence, with the known, intentionally-retained limitations listed below.

## Verified Accurate Documentation

The following areas were checked line-by-line against source/tests/live evidence and found accurate, requiring no correction: FastAPI/Pydantic v2 backend description; in-memory storage description; CORS origin list; frontend's hardcoded API address; backend-authoritative/frontend-displays-returned-state wording; frontend-owned display sorting; independently-implemented overdue rule on both sides; AND-logic filter combination; blank search/assignee handling; the overdue computation rule; all six routes' success codes; runtime 404 behavior; the POST-vs-PATCH 422-source distinction; the non-null-status-transition condition wording; CI triggers/Python version/test command; the environment-variable non-consumption claim; and the DOC1 component-schema-description effect. See rows C-01, C-02, C-05 through C-12, C-18 through C-24, and C-26 above for the specific evidence behind each.

## Known Limitations and Accepted Gaps

These are documented, intentional characteristics of the current implementation - not defects "fixed" by Part 4.4 and not scheduled for correction here:

- The backend does not sort results; sorting is a frontend-only concern (C-13).
- OpenAPI does not currently declare runtime `404` responses for any route (C-14).
- OpenAPI represents only the framework-validation `422` schema; the business-rule string-detail `422` shape is undocumented in the schema (C-15).
- `.env.example` declares `PORT`/`APP_ENV`, which no application code currently reads (C-16).
- `docs/midcourse/*.md`, `CHANGELOG.md`, and `API_SUMMARY_CHECKLIST.md` remain unchanged, point-in-time historical records and are not treated as current API authority (C-17).
- Backend and frontend independently implement the overdue-display rule; keeping them synchronized is a manual discipline, not an enforced invariant (C-09).
- Docker command *execution* evidence (Part 4.3) is prior-session/user-asserted, not reproducible from a file in this repository (C-25).

## Docstring Spot-Check

| Function/method | Docstring claim | Verified against | Result |
|---|---|---|---|
| `app/business_rules.py::validate_status_transition` | Raises 422 iff `(current, new)` not in `VALID_TRANSITIONS`; detail lists allowed transitions as `"From->To"` strings | Source lines 39-50 | Matches exactly |
| `app/main.py::create_task` | Server-managed fields not accepted; returns `TaskResponse` at HTTP 201 | `TaskCreate` field list + `extra="forbid"`; decorator `status_code=status.HTTP_201_CREATED` | Matches exactly |
| `app/main.py::update_task` | 404 if task missing; 422 if non-null `status` is an invalid transition; malformed bodies rejected by request validation before the handler runs (not raised here) | Source lines 183-198: `if payload.status is not None` gate, then 404 checks, then `validate_status_transition` call | Matches exactly (including this session's non-null-status wording correction) |
| `app/storage.py::get_all_tasks` | Filters combine with AND logic; blank search/assignee ignored; overdue = `due_date < today` and `status != Done`; does not sort | Source lines 74-108 | Matches exactly |
| `app/storage.py::update_task` | Only explicitly-supplied fields applied via `exclude_unset=True`; `updated_at` refreshed whenever at least one field is supplied, regardless of whether the value differs; returns `None`/unchanged task/updated task in that precedence | Source lines 144-156 | Matches exactly |
| `app/models.py::TaskUpdate.validate_title` | `None` returned unchanged when received; non-`None`/non-string rejected; string delegated to `_validate_title` | Source lines 103-107 | Matches exactly; docstring deliberately avoids asserting whether `None` arises from an omitted vs. explicitly-`null` field (verified this distinction is not testable from within the validator itself) |

## README-Command Verification

| Command | Classification | Evidence |
|---|---|---|
| `python --version` / `python -m venv venv` | Verified from repository configuration (standard Python CLI usage; not repository-specific) | N/A - general tooling |
| `.\venv\Scripts\python.exe -m pip install --upgrade pip` / `... -m pip install -r requirements.txt` | Verified from repository configuration | Matches the "Upgrade pip" / "Install dependencies" steps in `.github/workflows/ci.yml` |
| `.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000` | Verified this session (executed) | Live-started this Part 4.4 session; `/health`, `/openapi.json`, `/docs` all returned 200 against it |
| `.\venv\Scripts\python.exe -m http.server 5500 --directory frontend` | Verified this session (executed) | Live-started this Part 4.4 session; served `frontend/index.html` (byte-identical content length), user-confirmed visual rendering |
| `.\venv\Scripts\python.exe -m pytest -v` | Verified this session (executed, repeatedly) | 37 passed, 0 failed - baseline, post-DOC1/DOC2 regression, and this audit's re-confirmation all agree |
| `docker build --tag task-tracker:dev .` / `docker run --detach --name tt-dev --publish 8000:8000 task-tracker:dev` | Verified from repository configuration (syntax); execution is prior-session/user-asserted (Part 4.3), not repeated this session | `Dockerfile` content matches (port, non-root user, healthcheck) |
| `docker ps` / `curl.exe --fail --show-error .../health` / `docker logs` / `docker inspect --format ...` / `docker stop` / `docker rm` | Same as above | Same as above |

## Test and Live-Verification Summary

- **Baseline** (before Part 4.4 documentation changes): 37 passed, 0 failed.
- **Regression** (after DOC1 + DOC2 changes): 37 passed, 0 failed.
- **This audit's re-confirmation**: 37 passed, 0 failed, in 1.00s.
- **Live `GET /health`**: HTTP 200; `status` == `"ok"`; `timestamp` present and ISO-8601-formatted (UTC).
- **Live `GET /openapi.json`**: HTTP 200; corrected `info.description`; all 6 operations present with non-empty descriptions; no `404` in any declared response-code set; `PATCH`'s sole `422` references only `HTTPValidationError`.
- **Live `GET /docs`**: HTTP 200, confirmed to be the FastAPI-generated Swagger UI HTML shell; actual visual rendering was **user-confirmed in a browser**, not inferred from the HTTP response alone.
- **Live `GET http://localhost:5500/`**: HTTP 200; content length matched `frontend/index.html` exactly; contained `API_BASE_URL = "http://localhost:8000"` and the actual board/task-modal identifiers; visual rendering **user-confirmed**.
- **CORS**: a request with `Origin: http://localhost:5500` received `Access-Control-Allow-Origin: http://localhost:5500` (exact origin echoed, not a wildcard); a CORS preflight (`OPTIONS /tasks`) succeeded with the expected allowed methods.
- **Cleanup**: both temporary verification server process trees were confirmed terminated; ports 8000 and 5500 confirmed to have no listener; both endpoints confirmed unreachable post-cleanup.

## Files Changed by Part 4.4

Modified (working tree, not yet committed):
- `README.md`
- `app/business_rules.py`
- `app/main.py`
- `app/models.py`
- `app/storage.py`

Created:
- `docs/documentation/claim-vs-reality.md`

No repository file outside these six approved Part 4.4 paths was modified, created, or deleted.

## No Application Behavior Was Intentionally Changed

Every DOC1 and DOC2 edit was verified, at the time it was made, to be documentation-only:

- For `app/business_rules.py`, `app/storage.py`, and `app/models.py`: an AST comparison with all docstrings stripped showed **zero non-docstring differences** between the pre-Part-4.4 committed version and the edited working-tree version.
- For `app/main.py`: the same AST comparison showed **exactly one** non-docstring difference across all of DOC1 - the `FastAPI(description=...)` string literal - and this session's additional docstring wording correction (non-null-status wording) introduced **zero** further non-docstring differences.
- The full test suite passed identically (37/0) before and after every documentation edit.
- Live OpenAPI inspection confirmed: route paths, methods, summaries, tags, success codes, response-code sets, model fields, required lists, enum values, field types, and validation constraints all remained unchanged before and after DOC1. Operation `description` fields, the top-level `info.description`, and the component-schema `description` metadata for `TaskCreate`, `TaskUpdate`, `TaskResponse`, and `TaskStatus` changed as intended. `TaskPriority`, `HTTPValidationError`, and `ValidationError` remain without added descriptions. These are documentation-metadata changes, not runtime behavior changes.

## Remaining Risks or Pending Evidence

- Docker build/run *execution* for this repository state has not been independently re-verified within Part 4.4; the README's Docker section relies on your Part 4.3 assertion, which is not recorded in any repository file.
- `tests/verify_a.py` (the manual smoke script) was not executed during Part 4.4; CLAUDE.md already flags this as unverified against the current repository state.
- The `GET /tasks?overdue=<invalid>` -> 422 behavior (C-26) is confirmed correct but is not backed by a named regression test in `tests/test_tasks.py` - a future test addition would close this gap, though no such change is proposed here (out of scope for a documentation audit).
- Browser visual confirmation of `/docs` and the frontend board is user-supplied evidence for this session; it is not something this audit can independently re-derive from a repository file.

## Acceptance Checklist

- [x] Baseline test suite passed (37/0) before Part 4.4 documentation changes.
- [x] Regression test suite passed (37/0) after DOC1 and DOC2 changes.
- [x] Live API, OpenAPI, `/docs`, frontend, and CORS checks passed.
- [x] `/docs` and frontend visual rendering user-confirmed in a browser.
- [x] No application behavior was changed (AST-verified, documentation-only diffs).
- [x] README and docstrings re-audited against repository/runtime evidence in this pass; no remaining inaccuracies found.
- [x] Both genuine pre-Part-4.4 inaccuracies (stale Module 1 wording; `file://` frontend instruction) confirmed corrected.
- [x] Known limitations (404/422 OpenAPI gaps, unused env vars, no backend sorting, dual overdue implementations, historical docs) documented rather than silently "fixed."
- [x] Docker Part 4.3 execution evidence explicitly flagged as prior-session/user-asserted, not repository-embedded.
- [x] Claim-versus-reality audit created at `docs/documentation/claim-vs-reality.md`.
- [x] Git staging and commit were withheld throughout documentation generation until explicit user approval.
