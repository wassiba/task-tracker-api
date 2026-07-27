from datetime import date, timedelta


MISSING_TASK_ID = "00000000-0000-0000-0000-000000000000"


def test_create_task_valid_returns_201_with_full_body(client):
    response = client.post("/tasks", json={"title": "My Task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "My Task"
    assert data["description"] == ""
    assert data["status"] == "ToDo"
    assert data["priority"] == "Medium"
    assert data["assignee"] is None
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_with_due_date(client):
    due_date = (date.today() + timedelta(days=7)).isoformat()

    response = client.post(
        "/tasks",
        json={"title": "Task with due date", "due_date": due_date},
    )

    assert response.status_code == 201
    assert response.json()["due_date"] == due_date


def test_create_task_without_due_date(client):
    response = client.post("/tasks", json={"title": "Task without due date"})

    assert response.status_code == 201
    assert response.json()["due_date"] is None


def test_create_task_invalid_due_date_returns_422(client):
    response = client.post(
        "/tasks",
        json={"title": "Task with invalid due date", "due_date": "not-a-date"},
    )

    assert response.status_code == 422


def test_create_task_missing_title_returns_422(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "priority": "Urgent"})
    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    response = client.post("/tasks", json={"title": "Task", "unknown": "value"})
    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "Active task"})
    response = client.get("/tasks", params={"status": "Done"})
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})
    response = client.get("/tasks", params={"priority": "Low"})
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Low task"
    assert tasks[0]["priority"] == "Low"


def test_list_tasks_overdue_returns_only_overdue_unfinished_tasks(client):
    today = date.today()
    task_payloads = [
        {
            "title": "Overdue unfinished task",
            "due_date": (today - timedelta(days=1)).isoformat(),
        },
        {
            "title": "Task due today",
            "due_date": today.isoformat(),
        },
        {
            "title": "Future task",
            "due_date": (today + timedelta(days=1)).isoformat(),
        },
        {
            "title": "Completed overdue task",
            "status": "Done",
            "due_date": (today - timedelta(days=1)).isoformat(),
        },
        {"title": "Task without due date"},
    ]
    for payload in task_payloads:
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201

    response = client.get("/tasks", params={"overdue": "true"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Overdue unfinished task"
    assert tasks[0]["due_date"] == (today - timedelta(days=1)).isoformat()
    assert tasks[0]["status"] == "ToDo"


def test_list_tasks_search_matches_title(client):
    client.post("/tasks", json={"title": "Prepare quarterly report"})
    client.post("/tasks", json={"title": "Schedule team meeting"})

    response = client.get("/tasks", params={"search": "quarterly"})

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {
        "Prepare quarterly report"
    }


def test_list_tasks_search_matches_description(client):
    client.post(
        "/tasks",
        json={
            "title": "Review notes",
            "description": "Contains the migration checklist",
        },
    )
    client.post(
        "/tasks",
        json={"title": "Review budget", "description": "Contains cost estimates"},
    )

    response = client.get("/tasks", params={"search": "migration"})

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {"Review notes"}


def test_list_tasks_search_is_case_insensitive_and_supports_partial_match(client):
    client.post("/tasks", json={"title": "Investigate Authentication Failure"})
    client.post("/tasks", json={"title": "Update dashboard colors"})

    response = client.get("/tasks", params={"search": "AUTHent"})

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {
        "Investigate Authentication Failure"
    }


def test_list_tasks_search_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "Document release process"})

    response = client.get("/tasks", params={"search": "nonexistent phrase"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_assignee_is_case_insensitive_and_supports_partial_match(client):
    client.post("/tasks", json={"title": "API review", "assignee": "Alex Morgan"})
    client.post("/tasks", json={"title": "UI review", "assignee": "Jamie Lee"})

    response = client.get("/tasks", params={"assignee": "LEX mor"})

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {"API review"}


def test_list_tasks_assignee_filter_excludes_unassigned_tasks(client):
    client.post("/tasks", json={"title": "Assigned task", "assignee": "Sam"})
    client.post("/tasks", json={"title": "Unassigned task", "assignee": None})

    response = client.get("/tasks", params={"assignee": "sam"})

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {"Assigned task"}


def test_list_tasks_status_and_priority_combine_with_and_logic(client):
    task_payloads = [
        {"title": "Matching task", "status": "InProgress", "priority": "High"},
        {"title": "Wrong status", "status": "ToDo", "priority": "High"},
        {"title": "Wrong priority", "status": "InProgress", "priority": "Low"},
    ]
    for payload in task_payloads:
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201

    response = client.get(
        "/tasks",
        params={"status": "InProgress", "priority": "High"},
    )

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {"Matching task"}


def test_list_tasks_search_and_assignee_combine_with_and_logic(client):
    task_payloads = [
        {
            "title": "Matching deployment task",
            "description": "Release preparation",
            "assignee": "Taylor Reed",
        },
        {
            "title": "Deployment assigned elsewhere",
            "description": "Release preparation",
            "assignee": "Jordan Kim",
        },
        {
            "title": "Different work for Taylor",
            "description": "Database maintenance",
            "assignee": "Taylor Reed",
        },
    ]
    for payload in task_payloads:
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201

    response = client.get(
        "/tasks",
        params={"search": "release", "assignee": "taylor"},
    )

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {
        "Matching deployment task"
    }


def test_list_tasks_all_filters_combine_with_and_logic(client):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    tomorrow = (date.today() + timedelta(days=1)).isoformat()
    task_payloads = [
        {
            "title": "Critical API migration",
            "description": "Move the billing endpoint",
            "status": "InProgress",
            "priority": "High",
            "assignee": "Morgan Chen",
            "due_date": yesterday,
        },
        {
            "title": "Future API migration",
            "status": "InProgress",
            "priority": "High",
            "assignee": "Morgan Chen",
            "due_date": tomorrow,
        },
        {
            "title": "Overdue API migration for another owner",
            "status": "InProgress",
            "priority": "High",
            "assignee": "Casey Jones",
            "due_date": yesterday,
        },
        {
            "title": "Overdue low-priority API migration",
            "status": "InProgress",
            "priority": "Low",
            "assignee": "Morgan Chen",
            "due_date": yesterday,
        },
    ]
    for payload in task_payloads:
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201

    response = client.get(
        "/tasks",
        params={
            "search": "billing",
            "status": "InProgress",
            "priority": "High",
            "assignee": "morgan",
            "overdue": "true",
        },
    )

    assert response.status_code == 200
    assert {task["title"] for task in response.json()} == {
        "Critical API migration"
    }


def test_list_tasks_blank_or_whitespace_search_is_ignored(client):
    expected_titles = {"First searchable task", "Second searchable task"}
    for title in expected_titles:
        response = client.post("/tasks", json={"title": title})
        assert response.status_code == 201

    for search_value in ("", "   "):
        response = client.get("/tasks", params={"search": search_value})
        assert response.status_code == 200
        assert {task["title"] for task in response.json()} == expected_titles


def test_list_tasks_blank_or_whitespace_assignee_is_ignored(client):
    task_payloads = [
        {"title": "Assigned filter task", "assignee": "Robin"},
        {"title": "Unassigned filter task", "assignee": None},
    ]
    for payload in task_payloads:
        response = client.post("/tasks", json=payload)
        assert response.status_code == 201

    expected_titles = {"Assigned filter task", "Unassigned filter task"}
    for assignee_value in ("", "   "):
        response = client.get("/tasks", params={"assignee": assignee_value})
        assert response.status_code == 200
        assert {task["title"] for task in response.json()} == expected_titles


def test_list_tasks_invalid_status_returns_422(client):
    response = client.get("/tasks", params={"status": "Blocked"})

    assert response.status_code == 422


def test_list_tasks_invalid_priority_returns_422(client):
    response = client.get("/tasks", params={"priority": "Urgent"})

    assert response.status_code == 422


def test_get_task_by_id_returns_task(client, created_task):
    response = client.get(f"/tasks/{created_task['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == created_task["id"]
    assert data["title"] == created_task["title"]


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get(f"/tasks/{MISSING_TASK_ID}")
    assert response.status_code == 404
    assert MISSING_TASK_ID in response.json()["detail"]


def test_patch_partial_update_keeps_other_fields(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"description": "Updated description"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated description"
    assert data["title"] == created_task["title"]
    assert data["status"] == created_task["status"]
    assert data["priority"] == created_task["priority"]
    assert data["id"] == created_task["id"]


def test_patch_task_adds_due_date(client, created_task):
    due_date = (date.today() + timedelta(days=7)).isoformat()

    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"due_date": due_date},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] == due_date


def test_patch_task_clears_due_date(client):
    due_date = (date.today() + timedelta(days=7)).isoformat()
    create_response = client.post(
        "/tasks",
        json={"title": "Task with due date", "due_date": due_date},
    )
    assert create_response.status_code == 201
    task = create_response.json()

    response = client.patch(
        f"/tasks/{task['id']}",
        json={"due_date": None},
    )

    assert response.status_code == 200
    assert response.json()["due_date"] is None


def test_patch_not_found_returns_404(client):
    response = client.patch(
        f"/tasks/{MISSING_TASK_ID}",
        json={"title": "Updated"},
    )
    assert response.status_code == 404
    assert MISSING_TASK_ID in response.json()["detail"]


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "InProgress"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "Done"},
    )
    assert response.status_code == 422


def test_patch_same_status_returns_422(client, created_task):
    response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )
    assert response.status_code == 422


def test_delete_existing_returns_204_no_body(client, created_task):
    response = client.delete(f"/tasks/{created_task['id']}")
    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete(f"/tasks/{MISSING_TASK_ID}")
    assert response.status_code == 404
    assert MISSING_TASK_ID in response.json()["detail"]


def test_patch_forbidden_backward_transition_to_do_keeps_task_unchanged(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "In progress task",
            "description": "Original description",
            "status": "InProgress",
            "priority": "High",
            "assignee": "Alex",
        },
    )
    assert create_response.status_code == 201
    created_task = create_response.json()

    patch_response = client.patch(
        f"/tasks/{created_task['id']}",
        json={"status": "ToDo"},
    )
    assert patch_response.status_code == 422

    get_response = client.get(f"/tasks/{created_task['id']}")
    assert get_response.status_code == 200
    stored_task = get_response.json()

    assert stored_task["status"] == "InProgress"
    assert stored_task["title"] == created_task["title"]
    assert stored_task["description"] == created_task["description"]
    assert stored_task["priority"] == created_task["priority"]
    assert stored_task["assignee"] == created_task["assignee"]
