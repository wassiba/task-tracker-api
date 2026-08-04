"""In-memory task storage.

Tasks are held in a module-level dict (``_tasks``) keyed by task ID;
there is no persistence, and all data is lost when the process exits.
Tests reset this state between cases via ``_reset`` (see the autouse
fixture in ``tests/conftest.py``).
"""
from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def add_task(payload: TaskCreate) -> TaskResponse:
    """Create and store a new task.

    Generates a new ``id`` (UUID4 string) and sets ``created_at`` and
    ``updated_at`` to the current UTC time.

    Args:
        payload: Validated task-creation data.

    Returns:
        TaskResponse: The newly stored task.
    """
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=payload.description or "",
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return task


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    search: Optional[str] = None,
    assignee: Optional[str] = None,
    overdue: Optional[bool] = None,
) -> list[TaskResponse]:
    """Return stored tasks, optionally filtered.

    Supplied filters are combined using AND logic: each filter narrows
    the result of the previous one. ``search`` and ``assignee`` perform
    case-insensitive substring matching and are ignored when blank or
    whitespace-only. ``overdue=True`` restricts results to tasks whose
    ``due_date`` is earlier than today and whose status is not
    ``Done``.

    Args:
        status: Restrict to this status.
        priority: Restrict to this priority.
        search: Case-insensitive substring match against title or
            description.
        assignee: Case-insensitive substring match against assignee.
        overdue: If true, restrict to overdue, unfinished tasks.

    Returns:
        list[TaskResponse]: Matching tasks, in underlying dict order.
        This function does not sort results.
    """
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [task for task in tasks if task.status == status]
    if priority is not None:
        tasks = [task for task in tasks if task.priority == priority]
    if search is not None and (search_text := search.strip().casefold()):
        tasks = [
            task
            for task in tasks
            if (
                search_text in task.title.casefold()
                or search_text in task.description.casefold()
            )
        ]
    if assignee is not None and (assignee_text := assignee.strip().casefold()):
        tasks = [
            task
            for task in tasks
            if (
                task.assignee is not None
                and assignee_text in task.assignee.casefold()
            )
        ]
    if overdue:
        today = date.today()
        tasks = [
            task
            for task in tasks
            if (
                task.due_date is not None
                and task.due_date < today
                and task.status != TaskStatus.DONE
            )
        ]
    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    """Look up a task by ID.

    Args:
        task_id: The task's unique identifier.

    Returns:
        Optional[TaskResponse]: The matching task, or ``None`` if no
        task with ``task_id`` exists.
    """
    return _tasks.get(task_id)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    """Apply a partial update to a stored task.

    Only fields explicitly supplied on ``payload`` are applied (via
    ``payload.model_dump(exclude_unset=True)``); fields left unset are
    not touched. ``updated_at`` is refreshed to the current UTC time
    whenever at least one field is explicitly supplied, regardless of
    whether the supplied value differs from the field's current value.

    Args:
        task_id: The task's unique identifier.
        payload: Fields to update. Fields not explicitly supplied are
            left unchanged.

    Returns:
        Optional[TaskResponse]: ``None`` if no task with ``task_id``
        exists; the task unchanged (no ``updated_at`` refresh) if no
        fields were explicitly supplied; otherwise the updated task
        with a refreshed ``updated_at``.
    """
    task = _tasks.get(task_id)
    if task is None:
        return None

    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return task

    updated_task = task.model_copy(
        update={**updates, "updated_at": datetime.now(timezone.utc)}
    )
    _tasks[task_id] = updated_task
    return updated_task


def delete_task(task_id: str) -> bool:
    """Delete a stored task by ID.

    Args:
        task_id: The task's unique identifier.

    Returns:
        bool: True if a task was deleted, False if no task with
        ``task_id`` existed.
    """
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()
