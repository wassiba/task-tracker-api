# Module 2 — Task Tracker API Summary Checklist

**Project:** FastAPI Task Tracker REST API  
**Storage:** In-memory dictionary only; data cleared when the server process ends. No database or ORM.

---

## 1. Models and Enums

| Enum / Model | Values / Fields | Rules |
|---|---|---|
| **TaskStatus** | `ToDo`, `InProgress`, `Done` | — |
| **TaskPriority** | `Low`, `Medium`, `High` | — |
| **TaskCreate** | `title` (required), `description`, `status`, `priority`, `assignee` | Default status: `ToDo`. Default priority: `Medium`. Rejects blank/whitespace-only titles. Rejects titles > 200 chars. Forbids unknown fields. |
| **TaskUpdate** | All fields optional | Forbids `id`, `created_at`, `updated_at`. |
| **TaskResponse** | `id`, `title`, `description`, `status`, `priority`, `assignee`, `created_at`, `updated_at` | — |

---

## 2. Endpoints and Runtime-Verified Status Codes

> Status codes below were verified at runtime. Not every response is guaranteed to appear in Swagger.

| Method | Path | Runtime-verified status codes |
|---|---|---|
| **GET** | `/health` | **200** |
| **POST** | `/tasks` | **201** valid creation · **422** invalid request data |
| **GET** | `/tasks` | **200** list (including `[]` when no tasks match) · **422** invalid `status` or `priority` query values |
| **GET** | `/tasks/{task_id}` | **200** found · **404** missing |
| **PATCH** | `/tasks/{task_id}` | **200** valid partial update · **404** missing · **422** invalid request data or invalid status transition |
| **DELETE** | `/tasks/{task_id}` | **204** empty body on delete · **404** missing |

---

## 3. Status-Transition Rules

**Allowed**

| From | To |
|---|---|
| `ToDo` | `InProgress` |
| `InProgress` | `Done` |
| `Done` | `InProgress` |

**Rejected**

| From | To |
|---|---|
| `ToDo` | `Done` |
| `Done` | `ToDo` |
| any | same status |

**Note:** Title-only and other non-status PATCH requests skip transition validation.

**Six-transition matrix (runtime-verified):** `200, 200, 422, 200, 422, 200`

---

## 4. Verification Commands and Results

| Check | Command / Action | Result |
|---|---|---|
| Model imports | `app/models.py`, `app/storage.py` import check | Passed |
| Assignment verifier | `tests/verify_a.py` | All checks passed |
| CRUD endpoints | Manual verification (all five) | Passed |
| Full test suite | `pytest` | **17 passed**, 0 failed, 0 warnings |

---

## 5. Break Test Evidence

| Step | Observation |
|---|---|
| Disable `validate_status_transition(...)` | Exactly **2** tests failed |
| `test_patch_invalid_transition_todo_to_done_returns_422` | Returned **200** (expected **422**) |
| `test_patch_same_status_returns_422` | Returned **200** (expected **422**) |
| Restore production code | All **17** tests passed again |

**Conclusion:** Transition validation is enforced in production code and is covered by tests.
