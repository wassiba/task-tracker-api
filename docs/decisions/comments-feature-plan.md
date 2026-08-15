# Decision Proposal: Comments on Tasks

**Module:** 5, Part 5.4 - Agent-Driven Feature Planning
**Status:** Approved planning decision; implementation requires separate approval
**Scope:** Plan and critique only. No comments implementation is authorized by this document.

## 1. Objective and Non-Goals

Plan a course-scoped comments feature associated with existing tasks while preserving the current FastAPI, Pydantic, in-memory storage, pytest, and standalone vanilla JavaScript architecture.

Each comment would contain:

- `id`: server-generated string UUID, extending the current task identifier convention.
- `task_id`: path-derived string reference to an existing task.
- `author`: required, unverified free-form display text containing 1-100 characters.
- `body`: required plain text containing 1-2000 characters.
- `created_at`: server-generated, timezone-aware UTC datetime.

The approved first-phase scope is limited to creating a comment and listing an existing task's comments.

The following are out of scope:

- Implementing comments during Module 5 Part 5.4.
- Retrieving one comment, editing comments, or deleting individual comments.
- Authentication, authorization, accounts, ownership, or trusted author identity.
- Database persistence, an ORM, migrations, or data survival across process restarts.
- Search, pagination, reactions, attachments, moderation, or rich text.
- A frontend framework or frontend automated-test framework.
- Changes to task status transitions, filtering, overdue behavior, or display sorting.
- Dependency, CI, Docker, environment, deployment, or production-readiness changes.

## 2. Verified Repository Context

The following facts are grounded in the current repository:

- `app/main.py` defines the FastAPI application, CORS configuration, `/health`, and task create/list/get/patch/delete routes.
- `app/models.py` defines Pydantic v2 request and response models. Task request models use `ConfigDict(extra="forbid")` and explicit title validation.
- `app/storage.py` stores tasks in the module-level `_tasks` dictionary. It generates task IDs with `str(uuid4())` and timestamps with `datetime.now(timezone.utc)`.
- `app/storage.py::get_all_tasks` does not sort; frontend display sorting remains a frontend responsibility.
- `app/storage.py::delete_task` currently deletes only a task, and `_reset()` currently clears only task state.
- `app/business_rules.py` contains task status-transition rules only.
- `tests/conftest.py::_reset_storage` calls `storage._reset()` before and after every test.
- `tests/test_tasks.py` uses FastAPI `TestClient` and descriptive `test_<operation>_<condition>_<result>` naming.
- `frontend/index.html` is one HTML/CSS/JavaScript file with a task form, modal state, browser `fetch`, and safe `textContent` rendering.
- `.github/workflows/ci.yml` targets Python 3.11 and runs `python -m pytest -v`.
- `requirements.txt` already contains the packages needed for the proposed backend pattern; no new dependency is justified.
- `docs/decisions/in-memory-task-storage.md` retains in-memory storage for this course and defers persistence to a separate decision.
- `README.md` describes a course-scoped, non-production project without authentication or database persistence.

Comments, comment routes, comment lifecycle rules, users, authentication, migrations, frontend comment behavior, and comment concurrency guarantees do not currently exist. Every such behavior below is an approved design decision, not a description of implemented behavior.

## 3. Generic and Repository-Grounded Plan Comparison

### Generic plan

The generic plan was useful for early discovery. It identified a plausible comment shape, nested routes, validation, ordering, task deletion, tests, frontend states, accessibility, and documentation. It correctly labeled its architectural choices as assumptions.

It was not safe to hand to an implementer because it discussed database indexes, migrations, pagination, custom error wrappers, possible 400/409 responses, and framework-neutral frontend work that do not reflect this repository.

### Repository-grounded plan

The grounded plan correctly identified the actual FastAPI/Pydantic architecture, module-level in-memory store, TestClient fixtures, strict request models, single-file frontend, Python 3.11 CI target, and absence of authentication, migrations, and frontend test infrastructure.

The tech-lead review found that it still required corrections for physical cascade-cleanup proof, direct reset testing, single-process concurrency limits, frontend form/state isolation, stale asynchronous responses, documentation obligations, and exact acceptance criteria.

### Three-line comparison

- **Biggest difference:** The generic plan explores possibilities; the grounded plan maps work to the actual repository and its limitations.
- **Safe teammate handoff:** Only this corrected repository-grounded plan is suitable because it preserves existing contracts and names repository-specific risks.
- **When generic planning is enough:** Generic planning is sufficient for early brainstorming when architecture is unknown and no implementation handoff is expected.

## 4. Tech-Lead Critique

| Section | Label | Required correction or retained decision |
|---|---|---|
| Objective and Non-Goals | Right | Describe UUID/UTC reuse as an extension of task conventions, not existing comment behavior. |
| Current Architecture | Right | Keep verified facts separate from inferred comment design. |
| Feature Scope | Missing | Freeze plain-text body, unverified author, duplicate policy, and concurrency boundary. |
| Data Models and Validation | Missing | Require aware UTC construction and preserve internal whitespace/newlines. |
| Storage and Referential Integrity | Missing | Distinguish missing parent from an existing empty collection; accept O(n) scans and single-process limitations. |
| API Contract | Missing | Use repository response conventions and define exact missing-task behavior and validation precedence. |
| Task Deletion and Comment Lifecycle | Right | Cascade cleanup belongs inside storage deletion, not duplicated in routes. |
| Backend Tests | Missing | Test `_reset()` directly and prove physical cascade cleanup in storage. |
| Frontend Design | Missing | Avoid nested forms; isolate comment state and guard stale asynchronous responses. |
| Frontend Verification | Missing | Add close/reopen, task-switch, focus, draft-retention, and stale-response checks. |
| Documentation | Missing | Define the exact current-document scope and delay `AGENTS.md` updates until verified implementation. |
| Sequencing | Needs-Resequencing | Settle decisions, preflight, models, storage, API, tests, frontend, verification, and documentation in that order. |
| Risks | Missing | Add nested-form, shared-state, stale-response, O(n), and create/delete concurrency risks. |
| Open Questions | Missing | Separate blocking decisions from deferred future ideas. |
| Acceptance Criteria | Missing | Replace vague frontend completion with explicit observable outcomes and final diff/status proof. |

## 5. Approved Feature Decisions

The following design choices are approved for a possible future implementation:

1. Phase one supports create and list only.
2. `author` is unverified free-form display text, not an authenticated identity.
3. `body` is plain text. It must be rendered safely and never interpreted as HTML.
4. Outer whitespace is trimmed before validation and storage; internal whitespace and line breaks are preserved.
5. Duplicate comment content is allowed.
6. Comments are ordered by `created_at` ascending, then `id` ascending.
7. Deleting a task physically cascade-deletes its comments.
8. Existing tasks with no comments return HTTP 200 and an empty list.
9. Missing tasks return HTTP 404 with the task ID in the detail, following current conventions.
10. Normal FastAPI validation precedence is retained: an invalid body may return 422 before handler-level missing-task logic runs.
11. In-memory O(n) comment scans are accepted for course scope.
12. The feature provides no multi-process or concurrent-mutation guarantee beyond the current in-memory architecture.
13. Focused tests may inspect private in-memory state when necessary to prove `_reset()` and cascade cleanup.
14. The frontend refetches comments after a successful creation, retains the author field, and clears the body field.
15. Frontend verification remains manual unless a separate task approves test infrastructure.
16. OpenAPI should use existing FastAPI/Pydantic validation behavior and ordinary route documentation; no custom error-schema system is introduced.
17. A future implementation may update `README.md`, relevant backend docstrings, this decision record, and an applicable AI/governance record. Updating `AGENTS.md` requires separate approval after behavior is implemented and verified.

## 6. Proposed Data Models and Validation

A future implementation would add `CommentCreate` and `CommentResponse` to `app/models.py`.

`CommentCreate` would contain only:

- `author: str`
- `body: str`

It would use `ConfigDict(extra="forbid")` and explicit before-validation to:

- Reject missing, null, and non-string values without coercion.
- Trim outer whitespace.
- Reject empty or whitespace-only values.
- Enforce stripped author length of 1-100 characters.
- Enforce stripped body length of 1-2000 characters.
- Preserve internal spaces and line breaks.

`CommentResponse` would contain `id`, `task_id`, `author`, `body`, and `created_at` and would also forbid unknown fields.

`id`, `task_id`, and `created_at` would be absent from `CommentCreate`. Supplying any of them would therefore return HTTP 422. The path supplies `task_id`; trusted storage supplies the UUID and `datetime.now(timezone.utc)` timestamp.

## 7. Proposed Storage and Referential Integrity

A future implementation would add `_comments: dict[str, CommentResponse]` to `app/storage.py`, keyed by comment ID.

The storage boundary would provide operations equivalent to:

- Add a comment only after confirming the parent task exists.
- Return a missing-parent sentinel such as `None` when the task does not exist.
- Return `[]` when the task exists but has no comments.
- Return only comments belonging to the requested task.
- Sort results by `created_at`, then `id`.
- Physically remove all matching comments inside `storage.delete_task` when the parent task is deleted.
- Clear both `_tasks` and `_comments` inside `_reset()`.

This design deliberately accepts O(n) listing and cleanup scans. Comments remain process-local, disappear on restart, and are not shared across workers or instances. Parent validation plus comment creation is not a durable transaction and does not claim concurrency safety.

## 8. Proposed API Contract

| Method | Path | Request | Response | Success |
|---|---|---|---|---|
| POST | `/tasks/{task_id}/comments` | `CommentCreate` | `CommentResponse` | 201 |
| GET | `/tasks/{task_id}/comments` | None | `list[CommentResponse]` | 200 |

### Create behavior

- Existing task and valid body: HTTP 201 with the complete server-created comment.
- Nonexistent task and otherwise valid body: HTTP 404 with the task ID in `detail`.
- Invalid, missing, null, wrong-type, unknown, or server-managed fields: HTTP 422.
- The path `task_id` is authoritative.

### List behavior

- Existing task without comments: HTTP 200 and `[]`.
- Existing task with comments: HTTP 200 and a bare array in defined order.
- Nonexistent task: HTTP 404 with the task ID in `detail`.

Get-one, patch, and individual comment deletion routes remain deferred and require a separate decision.

## 9. Proposed Backend Test Plan

Prefer a separate future `tests/test_comments.py`.

Required coverage includes:

- Valid creation returns HTTP 201 with all fields.
- ID parses as a UUID string.
- `created_at` is serialized as a timezone-aware UTC timestamp.
- Outer whitespace is stripped and internal whitespace/newlines are preserved.
- Author lengths 1 and 100 pass; 0 and 101 fail.
- Body lengths 1 and 2000 pass; 0 and 2001 fail.
- Missing, null, empty, whitespace-only, and non-string author/body values return 422.
- Unknown, `id`, `task_id`, and `created_at` request fields return 422.
- Malformed JSON follows the current FastAPI validation response.
- Valid creation for a missing task returns 404 with the expected detail.
- Invalid-body versus missing-task precedence is frozen in a named test.
- Existing task with zero comments returns 200 and `[]`.
- One and multiple comments are returned correctly.
- Comments for other tasks are excluded.
- Ordering is deterministic, including a controlled equal-timestamp case.
- `_reset()` directly clears both task and comment state.
- Task deletion physically removes stored comments, not merely hides them behind a parent 404.
- Task deletion without comments retains HTTP 204 and an empty body.
- All existing task tests continue to pass unchanged.

No feature tests are to be added or run during Part 5.4 because comments are not implemented.

## 10. Proposed Frontend Design

A future implementation would extend the existing edit-modal experience without introducing a framework.

- Comments appear only when editing an existing task.
- Comment controls must not be a form nested inside the existing task form.
- Comment submission must not trigger task creation or editing.
- Comment loading, submission, draft, and error state must be separate from task modal submission state.
- Opening an existing task fetches its comments.
- Loading, empty, populated, 404, 422, and network-error states are visible.
- Author, body, and time are rendered using safe text assignment.
- Comment submission is disabled while pending.
- Failed submissions preserve both author and body.
- Successful submissions refetch the server-authoritative list, retain author, and clear body.
- Closing the modal or switching tasks must invalidate or ignore stale comment requests.
- Accessible labels, focus behavior, error announcements, keyboard behavior, and modal scrolling must be preserved.

## 11. Correct Future Implementation Sequence

1. Reconfirm the approved scope and repository instructions.
2. Inspect Git status and run the approved baseline verification.
3. Add models and validation.
4. Add in-memory storage, missing-parent distinction, reset, ordering, and cascade behavior.
5. Add the nested create/list routes and error behavior.
6. Add focused backend tests for all approved behavior.
7. Run focused tests and the full regression suite.
8. Add isolated frontend comment state and modal behavior.
9. Perform approved manual API and browser verification.
10. Update only approved current documentation.
11. Inspect the full diff and exact affected-file scope; rerun appropriate checks.
12. Stop before staging, committing, pushing, tagging, branching, or opening a pull request unless separately approved.

## 12. Risks and Deferred Questions

### Accepted or mitigated risks

- All comments are lost on process restart.
- Multiple processes do not share comments.
- Listing and cascade cleanup use O(n) scans.
- Task existence validation and comment creation are not transactionally isolated.
- Shared storage deletion and reset functions create regression risk and require focused tests.
- The single-file frontend creates nested-form, shared-state, stale-response, and draft-loss risks that require explicit controls.
- `author` does not prove identity.

### Deferred questions

- Comment retrieval, editing, and individual deletion.
- `updated_at` for future editing.
- Authentication, authorization, and trusted author identity.
- Pagination, search, moderation, attachments, reactions, and rich text.
- Persistent storage and database migration.
- Frontend automated test infrastructure.
- Stronger concurrency or multi-worker guarantees.

## 13. Acceptance Criteria for a Future Implementation

A future comments implementation may be accepted only when:

- The approved two endpoints and response shapes are implemented.
- UUID, path-derived task reference, validation, UTC timestamp, ordering, empty-list, and missing-task contracts pass focused tests.
- `_reset()` and physical cascade cleanup are directly proven.
- Existing task behavior and the complete regression suite remain passing.
- The frontend avoids nested forms and uses independent comment state.
- Loading, empty, populated, 404, 422, and network states are manually verified.
- Safe rendering, draft retention, duplicate-submission prevention, stale-request handling, focus, keyboard behavior, and accessibility are verified.
- Only approved files are changed.
- Documentation describes implemented behavior rather than planned behavior.
- Verification evidence includes commands, exit codes, test counts, warnings, manual checks, exact diff scope, and final Git status.
- No database, authentication, dependency, CI, Docker, deployment, or Git expansion occurs without separate approval.

## 14. Part 5.4 Deliverable and Approval Boundary

This decision document is the Module 5 Part 5.4 deliverable. It records the generic plan, repository-grounded plan, tech-lead critique, corrected design decisions, proposed tests, implementation sequence, risks, and acceptance criteria.

Its creation does not authorize implementation. Before any future code, test, frontend, configuration, documentation, or consequential Git change, the user must approve a new bounded implementation task and its exact file scope.
