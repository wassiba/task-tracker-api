from pydantic import ValidationError

from app.models import TaskCreate, TaskPriority, TaskStatus, TaskUpdate
from app.storage import _reset, add_task, get_all_tasks, get_task_by_id, update_task, delete_task


def check(label: str, condition: bool) -> None:
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label}")


def expect_validation_error(label: str, factory) -> None:
    try:
        factory()
        print(f"FAIL: {label}")
    except ValidationError:
        print(f"PASS: {label}")


def main() -> None:
    _reset()

    expect_validation_error(
        "Whitespace title rejected",
        lambda: TaskCreate(title="   "),
    )

    expect_validation_error(
        "Empty title rejected",
        lambda: TaskCreate(title=""),
    )

    expect_validation_error(
        "Title over 200 characters rejected",
        lambda: TaskCreate(title="x" * 201),
    )

    task = TaskCreate(title="  My task  ")
    check("Defaults applied: status ToDo", task.status == TaskStatus.TODO)
    check("Defaults applied: priority Medium", task.priority == TaskPriority.MEDIUM)
    check("Defaults applied: empty description", task.description == "")

    expect_validation_error(
        "Extra field rejected on TaskCreate",
        lambda: TaskCreate(title="Task", unexpected="value"),
    )

    expect_validation_error(
        "id rejected on TaskCreate",
        lambda: TaskCreate(title="Task", id="client-id"),
    )

    expect_validation_error(
        "created_at rejected on TaskUpdate",
        lambda: TaskUpdate(created_at="2026-01-01T00:00:00Z"),
    )

    expect_validation_error(
        "Invalid status rejected",
        lambda: TaskCreate(title="Task", status="Blocked"),
    )

    created = add_task(TaskCreate(title="Stored task"))
    check("Storage add_task creates task", created.title == "Stored task")
    check("Storage get_task_by_id returns task", get_task_by_id(created.id) is not None)
    check("Storage get_all_tasks returns list", len(get_all_tasks()) == 1)

    updated = update_task(created.id, TaskUpdate(title="Updated task"))
    check("Storage update_task updates title", updated is not None and updated.title == "Updated task")

    deleted = delete_task(created.id)
    check("Storage delete_task returns True", deleted is True)
    check("Storage delete_task removes task", get_task_by_id(created.id) is None)


if __name__ == "__main__":
    main()