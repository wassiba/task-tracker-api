# Architecture C — Targeted Context Draft

## 1. System behavior visible from the three files

The system is a FastAPI task-management API. It exposes:

- `GET /health`, returning `"ok"` and a current UTC timestamp.
- `POST /tasks`, creating a task and returning HTTP 201.
- `GET /tasks`, listing tasks with optional status, priority, search, assignee, and overdue filters.
- `GET /tasks/{task_id}`, returning one task or HTTP 404.
- `PATCH /tasks/{task_id}`, partially updating a task or returning HTTP 404.
- `DELETE /tasks/{task_id}`, deleting a task with HTTP 204 or returning HTTP 404.

List filters are combined with AND logic. Search checks title and description using case-insensitive substring matching. Assignee filtering also uses case-insensitive substring matching. Blank search and assignee values are ignored. `overdue=true` selects tasks with a due date before the current date and a status other than `Done`. Results are returned in dictionary order without sorting.

CORS permits four local origins on ports 5500 and 3000, allows all methods and headers, and disables credentials.

## 2. Data model and important fields

Statuses are `ToDo`, `InProgress`, and `Done`. Priorities are `Low`, `Medium`, and `High`.

Creation accepts:

- Required `title`
- Optional `description`, defaulting to an empty string
- `status`, defaulting to `ToDo`
- `priority`, defaulting to `Medium`
- Optional `assignee`
- Optional `due_date`

Responses additionally contain server-managed `id`, `created_at`, and `updated_at`. Updates make all editable fields optional. Unknown request fields are forbidden.

## 3. Create-task flow visible from the three files

1. `POST /tasks` receives a `TaskCreate` payload.
2. The request model validates and strips the title.
3. The route passes the validated payload to `storage.add_task`.
4. Storage generates a UUID4 string and the current UTC time.
5. Storage constructs a `TaskResponse`, using the same timestamp for creation and update.
6. The task is placed in the module-level dictionary under its ID.
7. The route returns the created task with HTTP 201.

## 4. The three inspected files and their roles

- `app/main.py`: Creates the FastAPI application, configures CORS, declares the health and task routes, delegates persistence operations, and invokes an imported status-transition validator.
- `app/models.py`: Defines status and priority enums plus create, update, and response models and title validation.
- `app/storage.py`: Maintains the in-memory task dictionary and implements create, retrieve, filter, update, delete, and reset operations.

## 5. Visible validation, storage, and error behavior

Titles must be strings, are stripped, and cannot be empty, whitespace-only, or longer than 200 characters. Create and update models reject unknown fields. Update applies only explicitly supplied fields. An empty update leaves the task and timestamp unchanged; a non-empty update refreshes `updated_at`.

Storage is process-local memory. IDs are UUID4 strings. Missing IDs produce HTTP 404 in retrieve, update, and delete routes. A supplied non-null status update invokes an imported transition validator before storage is changed. The implementation of that validator is outside the inspected evidence.

## 6. Not visible from the files I read

- Permitted status transitions: Not visible from the files I read.
- Frontend behavior: Not visible from the files I read.
- Test coverage and results: Not visible from the files I read.
- CI and container behavior: Not visible from the files I read.
- Authentication and authorization: Not visible from the files I read.
- Deployment and production readiness: Not visible from the files I read.

## 7. Questions required for a complete onboarding document

- Which status transitions are permitted, and why?
- How is the API started and configured in supported environments?
- Which client consumes the API?
- What automated verification exists?
- How are builds, containers, and deployment handled?
- Are authentication or authorization intended?
- What operational and production constraints apply?
