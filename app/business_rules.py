"""Business rules for task status transitions.

Enforces the allowed status state machine independently of request-body
validation: ``ToDo -> InProgress``, ``InProgress -> Done``, and
``Done -> InProgress``. Same-status and any other transition (e.g.
``ToDo -> Done``) are rejected.
"""
from fastapi import HTTPException, status

from app.models import TaskStatus


VALID_TRANSITIONS: frozenset[tuple[TaskStatus, TaskStatus]] = frozenset({
    (TaskStatus.TODO, TaskStatus.IN_PROGRESS),
    (TaskStatus.IN_PROGRESS, TaskStatus.DONE),
    (TaskStatus.DONE, TaskStatus.IN_PROGRESS),
})


def validate_status_transition(
    current: TaskStatus,
    new: TaskStatus,
) -> None:
    """Validate a task status transition.

    Args:
        current: The task's existing status.
        new: The requested new status.

    Returns:
        None: Returns normally when ``(current, new)`` is an allowed
        transition.

    Raises:
        HTTPException: 422 if ``(current, new)`` is not one of the
            transitions in ``VALID_TRANSITIONS``. The error detail
            lists the allowed transitions as ``"From->To"`` strings.
    """
    if (current, new) not in VALID_TRANSITIONS:
        allowed = sorted({
            f"{from_status.value}->{to_status.value}"
            for from_status, to_status in VALID_TRANSITIONS
        })
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=(
                f"Invalid status transition from {current.value} to {new.value}. "
                f"Allowed transitions: {allowed}"
            ),
        )
