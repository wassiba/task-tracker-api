# Task Tracker API

## Overview

This project is a learning implementation of a Task Tracker REST API using:

- Python
- FastAPI
- Pydantic

The project provides:

- FastAPI application
- Kanban frontend
- task creation, editing, deletion, and drag-and-drop status updates
- optional ISO-format due dates and visible overdue identification
- task priority and assignee support
- server-side search and filtering

## Run the API

From the repository root, use the repository virtual environment:

```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`, with Swagger documentation at `http://127.0.0.1:8000/docs`.

## Run the Frontend

Open `frontend/index.html` in a browser while the API is running. The frontend is a standalone HTML application; no frontend automated tooling is configured.

## Run Tests

```powershell
.\venv\Scripts\python.exe -m pytest -q
```

## Search and Filters

`GET /tasks` supports:

- `search`: case-insensitive partial matching across title and description;
- `status`;
- `priority`;
- `assignee`: case-insensitive partial matching;
- `overdue`.

Active filters combine using AND logic. Search and filtering are performed by the backend, while the existing frontend remains responsible for display sorting.
