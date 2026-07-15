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
