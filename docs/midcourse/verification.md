# Mid-Course Project Verification

## Feature 1 — Due Dates and Overdue Indication

### Automated Tests

The backend test suite passed after due-date support was implemented. The tests covered the overdue boundary rules, including that a task due today is not overdue and that a completed task is not overdue. Invalid `due_date` input was also verified to return HTTP 422.

### Manual Browser Verification

Manual browser testing confirmed:

- creating a task with a due date;
- editing and clearing a due date;
- displaying due dates on task cards;
- visibly identifying overdue unfinished tasks;
- not identifying tasks due today as overdue;
- not identifying `Done` tasks as overdue.

The project brief permits either an overdue filter or a visual overdue indicator. This implementation uses the visual indicator.

### Break Test

- **Defect introduced:** The overdue comparison was temporarily changed from `task.due_date < today` to `task.due_date <= today`.
- **Expected failure:** Tests for the due-today boundary should fail because the mutation incorrectly classifies tasks due today as overdue.
- **Actual failure:** The overdue tests failed because tasks due today were treated as overdue.
- **Restored implementation:** The strict comparison, `task.due_date < today`, was restored.
- **Final passing result:** The backend test suite passed after restoration.

## Feature 2 — Search and Combined Filters

### Automated Tests

Focused backend tests covered:

- title and description search;
- case-insensitive and partial search;
- searches with no results;
- assignee filtering and exclusion of unassigned tasks;
- AND logic and all filters combined;
- blank filters;
- invalid status and priority values.

Final command:

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

Final result:

```text
37 passed in 0.80s
```

### Manual Browser Verification

Browser verification confirmed that filtering remained server-side. Search by title and description, case-insensitive and partial matching, individual status/priority/assignee filters, and combined filters were checked. **Clear Filters** restored the full board. Active filters remained applied after create, edit, delete, and drag-and-drop status updates.

### Break Test

- **Defect introduced:** Title search was temporarily changed from partial matching, `search_text in task.title.casefold()`, to exact matching, `search_text == task.title.casefold()`.
- **Expected failure:** Partial-title searches should stop matching, while description substring search should remain unaffected.
- **Actual browser failure:** A partial-title search returned no result. Description search still worked because its substring comparison was unchanged.
- **Actual automated result:**

```text
2 failed, 35 passed in 1.21s
```

The failing tests were:

- `test_list_tasks_search_matches_title`
- `test_list_tasks_search_is_case_insensitive_and_supports_partial_match`

- **Restored implementation:** The title substring comparison was restored.
- **Final passing result:**

```text
37 passed in 0.80s
```
