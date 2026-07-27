# Mini Architecture Decision Record (Mini-ADR)

## Project

Task Tracker Mid-Course Project

## Selected Features

1. Due Dates and Overdue Indication
2. Search and Combined Filters

---

# Decision 1 - Due Date Representation

## Decision

Implement an optional `due_date` field using the ISO-8601 date format (`YYYY-MM-DD`).

The backend will store the value as an optional date and expose it through the existing Task API.

## Alternatives Considered

- Store full timestamps.
- Store due dates as strings.
- Add reminder scheduling.

## Rejected

Timestamp storage and reminder functionality were rejected because they introduce unnecessary complexity and are outside the scope of the mid-course project.

---

# Decision 2 - Overdue Calculation

## Decision

The backend defines and applies the overdue rule when processing the overdue query parameter. The frontend applies the same rule when displaying overdue task-card indicators. An overdue flag is not persisted because it could become stale.

A task is considered overdue when:

- a due date exists,
- the due date is earlier than the current date,
- the task status is not `Done`.

The frontend will display the result as a visible indicator on overdue task cards. A frontend overdue-filter control is not required because the project brief permits either filtering or visual identification.

## Alternatives Considered

- Compute overdue in the frontend.
- Persist an `is_overdue` field.

## Rejected

Persisting an overdue flag was rejected because it can become stale over time.

Frontend-only computation was rejected to avoid duplicating business rules.

---

# Decision 3 - Search and Filtering

## Decision

Filtering will be implemented by extending the existing `GET /tasks` endpoint with optional query parameters.

Supported filters:

- search
- status
- priority
- assignee
- overdue

Filters may be combined using AND logic.

Search and filtering remain server-side. Backend sorting will not be introduced; the existing frontend sorting behavior remains responsible for display order.

## Alternatives Considered

- Frontend-only filtering.
- Separate endpoint for every filter.
- Saved filter presets.

## Rejected

Frontend-only filtering was rejected because filtering belongs to backend query behavior.

Separate endpoints were rejected because query parameters provide a simpler REST design.

Saved presets were rejected because they exceed the intended project scope.

---

# Decision 4 - Frontend Architecture

## Decision

The existing Kanban board architecture will be preserved.

The frontend will continue to:

- obtain tasks from the backend,
- sort tasks locally,
- render the board using the existing rendering pipeline.

No optimistic UI updates will be introduced.

## Alternatives Considered

- Local filtering without backend refresh.
- Optimistic DOM updates.

## Rejected

The backend-authoritative architecture implemented in Version 0.4 will remain unchanged because it already provides predictable and testable behavior.

---

# AI Suggestions Reviewed

During implementation planning, AI proposed several larger enhancements including:

- reminder notifications,
- saved filter views,
- persistent UI preferences,
- additional filtering mechanisms.

These ideas were intentionally rejected because they increase complexity without improving the competencies assessed by the mid-course project.

The implementation remains intentionally small, testable, and aligned with the project brief.
