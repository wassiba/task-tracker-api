"""
This is the entry point of your FastAPI application.

It currently does only one thing:

Creates the FastAPI application.
Defines one endpoint:
GET /health

Nothing else.

This follows the Module 1 requirement exactly.

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
    description="Learning-focused Task Tracker REST API for Module 1."
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
    """
    Health check endpoint.
    Returns HTTP 200 with the current UTC timestamp.
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
    if storage.delete_task(task_id):
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(
        status_code=404,
        detail=f"Task with id {task_id} not found",
    )

