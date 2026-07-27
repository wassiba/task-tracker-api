# Mid-Course Project User Stories

## Selected Feature 1: Due Dates and Overdue Indication

### User Story 1 — Create a task with a due date

As a user, I want to assign an optional due date when creating a task so that I can track when the task should be completed.

#### Acceptance Criteria

- The Create Task modal includes an optional due date field.
- A task can be created without a due date.
- A valid due date is stored and returned by the backend.
- An invalid date format is rejected with a validation error.
- The created task displays its due date on the board.

---

### User Story 2 — Update or clear a due date

As a user, I want to add, change, or clear the due date of an existing task so that I can keep task deadlines accurate.

#### Acceptance Criteria

- The Edit Task modal displays the task's current due date.
- The due date can be changed to another valid date.
- The due date can be cleared.
- Updating only the due date does not remove or alter unrelated task fields.
- The board refreshes after a successful update.

---

### User Story 3 — Identify overdue tasks

As a user, I want overdue unfinished tasks to be visually identified so that I can prioritize them.

#### Acceptance Criteria

- A task is overdue when its due date is earlier than the current date.
- Tasks with status `Done` are not displayed as overdue.
- Overdue tasks show a clear visual indicator on the card.
- Tasks without a due date are not displayed as overdue.
- Tasks due today are not displayed as overdue.
- Future-dated tasks are not displayed as overdue.

---

### User Story 4 — Use overdue information from the API

As a user, I want overdue status to follow one consistent backend rule so that the board identifies missed deadlines accurately.

#### Acceptance Criteria

- The backend supports identifying unfinished overdue tasks.
- The frontend applies the same overdue rule used by the backend when displaying its visual indicator.
- Tasks due today and tasks with status `Done` are not identified as overdue.
- The board does not require a frontend overdue-filter control.

---

### Corrected AI Assumption for Feature 1

An AI tool may assume that any task with a past due date should remain marked overdue, including completed tasks.

This project corrects that assumption: tasks with status `Done` are excluded from overdue results and do not display an overdue indicator.

---

## Selected Feature 2: Search and Combined Filters

### User Story 1 — Search task text

As a user, I want to search task titles and descriptions so that I can quickly locate a task.

#### Acceptance Criteria

- The frontend includes a text search field.
- Search matches task titles.
- Search matches task descriptions.
- Search is case-insensitive.
- Partial matches are supported.
- A search with no matches returns an empty task list without an error.

---

### User Story 2 — Filter tasks by status

As a user, I want to filter tasks by status so that I can focus on one workflow stage.

#### Acceptance Criteria

- The frontend includes a status filter.
- Valid values are `ToDo`, `InProgress`, and `Done`.
- The backend returns only tasks matching the selected status.
- Invalid status values are rejected with a validation error.
- All Kanban columns remain visible, including empty columns.

---

### User Story 3 — Filter tasks by priority

As a user, I want to filter tasks by priority so that I can focus on the most important work.

#### Acceptance Criteria

- The frontend includes a priority filter.
- Valid values are `High`, `Medium`, and `Low`.
- The backend returns only matching tasks.
- Invalid priority values are rejected with a validation error.
- Returned tasks remain sorted in the frontend by priority and then task ID.

---

### User Story 4 — Combine search and filters

As a user, I want to combine search, status, priority, and assignee filters so that I can narrow the board to the exact tasks I need.

#### Acceptance Criteria

- Search, status, priority, and assignee filters can be active together.
- Every active filter is combined using AND logic.
- Filtering is performed by the backend.
- Empty filter values are omitted from the request.
- Clearing filters restores the full board.
- Active filters are preserved after task refresh operations.

---

### User Story 5 — Filter by assignee

As a user, I want to filter tasks by assignee so that I can view work assigned to a specific person.

#### Acceptance Criteria

- The frontend includes an assignee filter.
- Assignee matching is case-insensitive.
- Partial assignee matches are supported.
- The assignee filter can be combined with other filters.
- Tasks without a matching assignee are excluded.

---

### Corrected AI Assumption for Feature 2

An AI tool may assume that filtered-out workflow stages should be hidden from the interface.

This project corrects that assumption: the three Kanban columns remain visible at all times, even when one or more columns contain no matching tasks.
