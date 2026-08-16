# Release Evidence

## Baseline

- Branch: `final-project`
- Date: 2026-08-16
- Starting commit: `2479a5982b7fe99f8582033e91f0f35ff601ab8a`
- Local app run command: `.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000`
- `/health` result: HTTP 200 with `{"status":"ok","timestamp":"2026-08-16T17:23:09.614170+00:00"}`.
- Frontend check: served with `.\venv\Scripts\python.exe -m http.server 5500 --directory frontend` and opened at `http://localhost:5500/`. The three-column Kanban board rendered correctly at a 1280 x 800 desktop viewport. A task was created through the modal, reopened for editing, changed to High priority with an updated description, saved, and visibly rendered with the new values.
- Baseline test command: `.\venv\Scripts\python.exe -m pytest -v`
- Baseline result: 37 passed, 0 failed, 0 skipped, with one non-functional `PytestCacheWarning` caused by the sandbox being unable to update `.pytest_cache`.
- Final result after the bounded title-validation fix: 38 passed, 0 failed, 0 skipped, with the same cache warning.

## CI evidence

- Workflow file: `.github/workflows/ci.yml`
- Final-project CI history: [branch-filtered workflow runs](https://github.com/wassiba/task-tracker-api/actions/workflows/ci.yml?query=branch%3Afinal-project). The latest run observed before this documentation update was [CI run 31961974804](https://github.com/wassiba/task-tracker-api/actions/runs/31961974804), which completed successfully for commit `f9b8c17393b36290deab56bd5cc189599bce8912`. Its test job and `Run tests` step both passed.
- Test command used by CI: `python -m pytest -v`
- Trigger check: the workflow runs on both `push` and `pull_request`.
- Environment check: Python is explicitly set to `3.11` and dependencies are installed from `requirements.txt`.
- Shortcut check: no `continue-on-error`, no `|| true`, and pytest is not skipped.

## Docker evidence

- Build command: `docker build --tag task-tracker:dev .`
- Build result: exit code 0; image `task-tracker:dev` created successfully from the current working tree.
- Run command: `docker run --detach --name tt-dev --publish 8000:8000 task-tracker:dev`
- `/health` check: HTTP 200 with `{"status":"ok","timestamp":"2026-08-16T17:27:48.373896+00:00"}`.
- Docker health check: reached `healthy` with `FailingStreak` 0.
- Non-root check: `docker inspect` reported configured user `app`; `docker exec tt-dev id` reported `uid=999(app) gid=999(app)`.
- No-baked-secrets check: `.dockerignore` excludes `.env`, `.env.*`, logs, Git metadata, documentation, tests, and local environments. The build context was 18.36 kB and the Dockerfile copies only `requirements.txt` and `app/`.
- Cleanup: the temporary `tt-dev` verification container was stopped and removed after the checks; the local image was retained.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The local API command starts the service and `/health` returns 200. | Ran the documented uvicorn command and requested `http://127.0.0.1:8000/health`. | Accurate; HTTP 200 with status `ok`. | None. |
| The frontend must be served over HTTP and supports the Kanban create/edit flow. | Served `frontend/` on port 5500 and exercised the create and edit modals in a browser. | Accurate; board and saved changes rendered correctly. | None. |
| The complete test command passes. | Ran `.\venv\Scripts\python.exe -m pytest -v` before and after final work. | Accurate; 37 baseline tests and 38 final tests passed. | Added one focused regression test for explicit null title updates. |
| The Docker image runs as non-root and exposes a working health endpoint. | Successful build/run, HTTP request, `docker inspect`, and `docker exec ... id`. | Accurate; HTTP 200, Docker `healthy`, UID/GID 999. | None. |
| CI uses Python 3.11 and runs pytest without failure-hiding shortcuts. | Read `.github/workflows/ci.yml` line by line and inspected the final-project branch CI history, including successful run 31961974804 for commit `f9b8c17393b36290deab56bd5cc189599bce8912`. | Accurate; the current `final-project` commit completed successfully and its `Run tests` step passed. | None. |

## Scope control

No product feature was added. The only application behavior change rejects an explicitly null PATCH title, a directly reproduced defect that previously stored state inconsistent with the required string response model. The correction is limited to `app/models.py`, is protected by one focused endpoint regression test, and is explained in `docs/final-ai-review.md`.
