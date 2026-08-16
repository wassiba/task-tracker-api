"""Pydantic request/response models for tasks.

Defines the ``TaskStatus``/``TaskPriority`` enums and the
create/update/response models used by the ``/tasks`` endpoints.
"""
from datetime import date, datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator


class TaskStatus(str, Enum):
    """A task's lifecycle status.

    Not every transition between these values is permitted; see
    `validate_status_transition` in `app/business_rules.py` for the
    allowed transitions.
    """

    TODO = "ToDo"
    IN_PROGRESS = "InProgress"
    DONE = "Done"


class TaskPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


def _validate_title(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("Title cannot be empty or whitespace-only")
    if len(stripped) > 200:
        raise ValueError("Title must be at most 200 characters")
    return stripped


class TaskCreate(BaseModel):
    """Request body for creating a task.

    Server-managed fields (``id``, ``created_at``, ``updated_at``) are
    intentionally absent from this model; supplying them is rejected as
    an unknown field because of ``extra="forbid"``. ``status`` defaults
    to ``ToDo`` and ``priority`` defaults to ``Medium`` when omitted.
    """

    model_config = ConfigDict(extra="forbid")

    title: str
    description: Optional[str] = ""
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Reject a non-string title, then apply the shared title rule.

        Delegates to the module-level ``_validate_title`` helper: the
        title is stripped, then rejected if empty/whitespace-only or
        longer than 200 characters.
        """
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        return _validate_title(value)


class TaskUpdate(BaseModel):
    """Request body for partially updating a task.

    All fields are optional; only fields explicitly set are applied by
    `update_task` in `app/storage.py` (unset fields are left unchanged).
    Server-managed fields (``id``, ``created_at``, ``updated_at``) are
    not accepted, and unknown fields are rejected because of
    ``extra="forbid"``.
    """

    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value: Optional[str]) -> str:
        """Validate an optional title update.

        An explicitly supplied ``None`` or any other non-string value is
        rejected. A string value is passed to the module-level
        ``_validate_title`` helper (stripped, then rejected if
        empty/whitespace-only or longer than 200 characters). Omitting
        ``title`` remains valid for a partial update.
        """
        if value is None:
            raise ValueError("Title must be a string")
        if not isinstance(value, str):
            raise ValueError("Title must be a string")
        return _validate_title(value)


class TaskResponse(BaseModel):
    """Server-managed representation of a task returned by the API.

    Unlike `TaskCreate`/`TaskUpdate`, this model includes the
    server-generated ``id``, ``created_at``, and ``updated_at`` fields.
    """

    model_config = ConfigDict(extra="forbid")

    id: str
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assignee: Optional[str]
    due_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
