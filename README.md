# Task Tracker API

## Module 1

This project is a learning implementation of a Task Tracker REST API using:

- Python
- FastAPI
- Pydantic

The current scaffold provides:

- FastAPI application
- `/health` endpoint
- Swagger documentation

## Run

```bash
uvicorn app.main:app --reload
```

## Test

```
GET http://127.0.0.1:8000/health
```

## Swagger

```
http://127.0.0.1:8000/docs
```