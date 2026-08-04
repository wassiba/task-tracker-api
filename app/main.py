"""FastAPI application entry point for the Task Tracker API.

Defines the HTTP interface for task management: a health check endpoint
and CRUD endpoints for tasks, including server-side search/filtering and
backend-authoritative status-transition validation. CORS is restricted to
a fixed set of local development origins (see `allowed_origins` below).
"""
from datetime import datetime, timezone

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from app import storage
from app.business_rules import validate_status_transition
from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

# Load environment variables from .env if present
load_dotenv()

app = FastAPI(
    title="Task Tracker API",
    version="0.1.0",
    description=(
        "Task Tracker REST API: create, read, update, and delete tasks, "
        "with search/filtering and backend-enforced status transitions."
    )
)

allowed_origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Health check endpoint.

    Responds with HTTP 200.

    Returns:
        dict[str, str]: A mapping containing `status` (always "ok")
        and `timestamp` (the current UTC time as an ISO 8601 string,
        from `datetime.now(timezone.utc).isoformat()`).
    """
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["tasks"],
)
def create_task(payload: TaskCreate) -> TaskResponse:
    """Create a new task.

    Args:
        payload: Task fields to create. Server-managed fields such as
            `id`, `created_at`, and `updated_at` are not accepted (see
            `TaskCreate`).

    Returns:
        TaskResponse: The newly created task (HTTP 201), including its
        generated `id` and timestamps.
    """
    return storage.add_task(payload)


@app.get(
    "/tasks",
    response_model=list[TaskResponse],
    tags=["tasks"],
)
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    search: str | None = None,
    assignee: str | None = None,
    overdue: bool | None = None,
) -> list[TaskResponse]:
    """List tasks, optionally filtered.

    Supplied filters are combined using AND logic: each active filter
    narrows the result of the others (see `get_all_tasks` in
    `app/storage.py`). Blank or whitespace-only `search`/`assignee`
    values are ignored.

    Args:
        status: Restrict results to this status.
        priority: Restrict results to this priority.
        search: Case-insensitive substring match against title or
            description.
        assignee: Case-insensitive substring match against assignee.
        overdue: If true, restrict results to tasks with a past
            `due_date` and a status other than `Done`.

    Returns:
        list[TaskResponse]: Matching tasks (HTTP 200). Results are not
        sorted by this endpoint.
    """
    return storage.get_all_tasks(
        status=status,
        priority=priority,
        search=search,
        assignee=assignee,
        overdue=overdue,
    )


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def get_task(task_id: str) -> TaskResponse:
    """Retrieve a single task by ID.

    Args:
        task_id: The task's unique identifier.

    Returns:
        TaskResponse: The matching task (HTTP 200).

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
    """
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.patch(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["tasks"],
)
def update_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    """Partially update an existing task.

    Only fields explicitly supplied on `payload` are applied; omitted
    fields are left unchanged (see `update_task` in `app/storage.py`).
    When `payload` supplies a non-null `status` value, the transition
    from the task's current status to that value is validated against
    the allowed state machine (see `validate_status_transition` in
    `app/business_rules.py`) before the update is applied.

    Args:
        task_id: The task's unique identifier.
        payload: Fields to update. Fields not explicitly supplied are
            left unchanged.

    Returns:
        TaskResponse: The updated task (HTTP 200).

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
        HTTPException: 422 if `payload` supplies a non-null `status`
            value that is not a valid transition from the task's
            current status. Malformed request bodies (e.g. invalid
            field types or unknown fields) are rejected by request
            validation before this handler runs and are not raised
            here.
    """
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(
                status_code=404,
                detail=f"Task with id {task_id} not found",
            )
        validate_status_transition(existing.status, payload.status)

    task = storage.update_task(task_id, payload)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["tasks"],
)
def delete_task(task_id: str) -> Response:
    """Delete a task by ID.

    Args:
        task_id: The task's unique identifier.

    Returns:
        Response: An empty HTTP 204 response on success.

    Raises:
        HTTPException: 404 if no task with `task_id` exists.
    """
    if storage.delete_task(task_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {task_id} not found",
    )

