# Task Tracker API Security Review

- **Review status:** Final reconciliation record; no remediation was performed
- **Review date:** 2026-08-11

## Repository baseline

- Branch: `mid-course-project`
- Commit: `790a7c7d359944ef9d1b02f450fc981af5cb05c7`
- Baseline tests: prior evidence records 37 collected, 37 passed, and 0 failed
- Current review note: the regression suite was not rerun during this read-only reconciliation

## Scope and method

This review reconciles five AI-assisted findings with six independently prepared human findings. It uses static repository inspection, the complete 30-page external Human Security Scan Notes, prior regression evidence, and the focused null-title verification recorded in those notes.

The review distinguishes:

- Verified repository facts
- Directly exercised behavior
- Architectural inference
- Intentional course limitations
- Conditional wider-deployment concerns
- Time-sensitive external evidence

No application code, test, dependency, configuration, CI workflow, Docker artifact, or security control was changed. No scanner, server, application, Docker command, installation, network request, or external-service operation was run during reconciliation.

## Grading definitions

- **Valid:** Repository evidence supports the stated defect, limitation, or risk, including a clearly qualified conditional risk.
- **False Positive:** The claimed condition is contradicted by repository evidence or does not apply.
- **Noise:** The observation is technically true but lacks a meaningful security, governance, or reproducibility consequence in the reviewed scope.
- **Medium:** Material under the stated conditions or relevant to reproducibility and supply-chain governance, but not necessarily a demonstrated exploit.
- **Low:** A supported limitation or hardening concern with limited current impact in the course-scoped design.

## AI findings

| Finding ID | Severity | Finding | Repository evidence | Final grade | Grade reason | Qualification | Next action |
|---|---|---|---|---|---|---|---|
| SEC-AI-01 | Medium | Task CRUD has no caller identity, authentication, authorization, or ownership enforcement. | `app/main.py`; `app/models.py`; `README.md` | Valid | Every task route operates on a shared collection without a security dependency or owner identity. | Intentional course limitation; Medium only when reachable by untrusted clients. | Define identity and ownership requirements before any approved wider deployment. |
| SEC-AI-02 | Medium | Application-level bounds are absent for stored text other than title, filter text, task count, and list results. | `app/models.py`; `app/main.py`; `app/storage.py` | Valid | Description, assignee, search, and assignee-filter text lack comparable limits; storage is uncapped and listing has no pagination or result cap. | Conditional architectural risk under untrusted or high-volume access; no exhaustion event was demonstrated. | Document current assumptions and reconsider limits and pagination only if exposure or volume requirements change. |
| SEC-AI-03 | Medium | Python dependencies and the Docker base image use floating references. | `requirements.txt`; `.github/workflows/ci.yml`; `Dockerfile` | Valid | Dependencies lack versions and hashes, CI upgrades pip, and `python:3.11-slim` is not digest-pinned. | Reproducibility and supply-chain concern; no current-vulnerability claim. Preserve `httpx2` unless separate evidence and approval support a change. | Handle through a separate dependency and image maintenance decision. |
| SEC-AI-04 | Low | GitHub Actions use mutable major-version tags. | `.github/workflows/ci.yml` | Valid | `actions/checkout@v7` and `actions/setup-python@v7` are not immutable commit-SHA references. | Low because the workflow is test-only, grants `contents: read`, and contains no explicit secret, write, or deployment step. | Handle through a separate CI-hardening decision. |
| SEC-AI-05 | Low | Task storage is process-local and non-persistent. | `app/storage.py`; `docs/decisions/in-memory-task-storage.md`; `README.md` | Valid | A module-level dictionary loses state on restart and cannot provide shared state across processes. | Restart loss is repository-supported; multiple-worker divergence is an architectural inference. This is an intentional single-instance course decision. | Reassess only if persistence or multi-instance operation becomes approved scope. |

## Human findings

| Human ID | Finding | Evidence | Context | Relationship to AI review | Next action |
|---|---|---|---|---|---|
| SEC-HUM-001 | PATCH accepts `title: null` and storage retains it even though `TaskResponse.title` requires a string. | `app/models.py:85`, `app/models.py:92`, `app/models.py:120`, `app/storage.py:148`, and `app/storage.py:79`. The focused model/storage check exited 0 and returned `accepted_null_update= True` and `stored_title_type= NoneType`. | Current course risk; directly confirmed invalid stored state. API response-validation and later search failures are code-supported consequences not directly exercised. | You-only finding. It is distinct from general input-size limits. | Add a focused endpoint regression test before considering any separately approved behavior change. |
| SEC-HUM-002 | The API has no caller identity, authorization, or task-ownership boundary. | Task CRUD handlers in `app/main.py`; request models in `app/models.py`; limitations in `README.md`. | Intentional course limitation and wider-deployment access-control concern. | Agreement with `SEC-AI-01`. | Record identity, ownership, and deployment requirements before wider access is approved. |
| SEC-HUM-003 | Stored text, filter text, task count, and list responses lack application-level bounds beyond the title maximum. | `app/models.py`; `app/main.py`; `app/storage.py`. | Wider-deployment concern under untrusted or high-volume use. | Agreement with `SEC-AI-02`. | Document volume assumptions and revisit bounds only if those assumptions change. |
| SEC-HUM-004 | Tasks disappear on restart, and multiple workers would maintain separate collections. | `app/storage.py`; `docs/decisions/in-memory-task-storage.md`; `README.md`. | Intentional course limitation; multiple-worker behavior is architectural inference. | Agreement with `SEC-AI-05`. | Reassess only if persistence or multi-instance operation enters approved scope. |
| SEC-HUM-005 | CI and container builds use mutable runner, action, base-image, pip, and Python-dependency references. | `.github/workflows/ci.yml`; `requirements.txt`; `Dockerfile`. | Wider-deployment reproducibility and supply-chain concern; no current-vulnerability claim. | Agreement with both `SEC-AI-03` and `SEC-AI-04`; both AI IDs remain distinct. | Prepare a separate reproducibility and reference-maintenance decision. |
| SEC-HUM-006 | The 37-test suite lacks direct negative coverage for several enforced boundaries and the nullable-title path. | `tests/test_tasks.py`; `tests/conftest.py`; static inventory of 37 test functions. | Current coverage risk. Missing coverage does not prove that every untested input is vulnerable. | You-only finding; separate from implementation vulnerabilities. | Begin with the focused null-title endpoint regression associated with `SEC-HUM-001`. |

## Checked-clean areas

The human review checked the following areas without identifying a supported finding:

- Server-managed IDs and timestamps
- Backend status-transition enforcement
- Overdue-state authority
- Error and stack-trace exposure
- Frontend DOM injection
- Committed secrets and environment-file exclusion
- Local-scope CORS configuration
- Docker runtime privilege and final-image contents
- GitHub Actions permissions, secrets, and failure propagation
- Test-state isolation
- Unknown request-field rejection

These clean-area results do not imply permanent security and were not converted into findings.

## Reconciliation

### Agreement

| AI finding | Human finding | Reconciled conclusion |
|---|---|---|
| SEC-AI-01 | SEC-HUM-002 | Same missing identity, authorization, and ownership boundary |
| SEC-AI-02 | SEC-HUM-003 | Same application-level resource-bound concern |
| SEC-AI-03 | SEC-HUM-005 | Human review covers floating dependencies and Docker image references |
| SEC-AI-04 | SEC-HUM-005 | Human review also covers mutable Action and runner references |
| SEC-AI-05 | SEC-HUM-004 | Same process-local and non-persistent storage limitation |

### AI-only

None. The Human Notes covered every AI finding.

### You-only

| Human finding | Reconciled conclusion |
|---|---|
| SEC-HUM-001 | Directly confirmed nullable PATCH-title defect not identified among the five AI findings |
| SEC-HUM-006 | Direct negative-test coverage gap not elevated by the AI audit |

## Coverage observations

**What Codex covered well:** The AI review identified the main cross-cutting architectural and supply-chain risks and generally qualified them appropriately for the course scope.

**What human review uniquely contributed:** Human review discovered and directly verified the nullable-title defect, separated coverage gaps from implementation vulnerabilities, documented checked-clean areas, and applied project-context judgment to intentional limitations.

## Prioritized top-three backlog

| Rank | Finding IDs | Item | Why it matters | Owner | Next action |
|---|---|---|---|---|---|
| 1 | SEC-HUM-001; related SEC-HUM-006 | Establish endpoint-level evidence for nullable PATCH title | It is the only directly confirmed current defect and creates stored state inconsistent with `TaskResponse`. | Backend | Add one focused regression test that submits `{"title": null}` through PATCH and records the endpoint result and stored-state behavior. |
| 2 | SEC-AI-01; SEC-HUM-002 | Define an access-control deployment gate | Any untrusted exposure would give callers access to the shared task collection. | Project/course owner | Record the identity, ownership, and deployment assumptions that must be approved before wider access. |
| 3 | SEC-AI-03; SEC-AI-04; SEC-HUM-005 | Establish a reproducibility and reference-maintenance decision | Fresh CI and container builds can resolve different dependencies, actions, runners, and images. | CI/DevOps | Prepare a separate decision record covering pinning scope, update cadence, authoritative verification sources, and preservation of `httpx2` pending separate evidence. |

## Evidence limitations

- The focused null-title check directly confirmed model/storage acceptance and retention, but did not import `app.main` or exercise the API response and search consequences.
- Prior regression evidence records 37 collected, 37 passed, and 0 failed; the suite was not rerun for this reconciliation.
- `pip-audit` 2.10.1 reported no known vulnerabilities for packages installed in the local project environment at the time checked. This is not a permanent security guarantee.
- Historical exit codes were not retained for the dependency audit and some reference-resolution commands.
- GitHub Action v7 tags existed and resolved to recorded commits at the time checked.
- `python:3.11-slim` resolved to a recorded multi-platform digest and Python 3.11.15 slim manifests at the time checked.
- Nothing was listening on local port 8000 during the recorded local check.
- Docker container enumeration failed because the daemon was unavailable and its configuration could not be read.
- The project owner confirms the project was not deployed remotely. This is owner-provided confirmation, not independently retrieved external evidence.
- Advisories, versions, action tags, runner images, package provenance, dependency resolutions, and image digests are time-sensitive and require fresh authoritative verification before consequential decisions.
- The Human Notes and prompt cite `app/models.py:119` for the `TaskResponse.title` field. At this baseline, the title declaration is at `app/models.py:120`; line 119 declares the ID. This locator difference does not change the finding.

## Verification record

| Verification | Result |
|---|---|
| Root repository instructions | Read and followed |
| Repository root | Confirmed |
| Branch | `mid-course-project` |
| Full commit | `790a7c7d359944ef9d1b02f450fc981af5cb05c7` |
| Initial short Git status | Empty; exit 0 |
| Initial staged-path check | Empty; exit 0 |
| Target review document | Absent |
| External Human Notes | All 30 pages read |
| Static finding evidence | Inspected in repository files |
| Static test inventory | 37 test functions |
| Prior regression evidence | 37 collected, 37 passed, 0 failed; not rerun |
| Historical focused null-title check | Exit 0; accepted null update and stored `NoneType` |
| Final unstaged paths | None |
| Final staged paths | None |
| Final Git status | Working tree clean |

The external Human Notes retain the exact focused-check command. This condensed review records its controls, exit code, and result without copying the complete external report.

## No-behavior-change statement

This reconciliation changed no application behavior. It did not implement, stage, commit, or apply a security fix.

## Acceptance checklist

- [x] All five AI findings retain their approved grades and severities.
- [x] All six human findings are accounted for.
- [x] Every stable finding ID is preserved.
- [x] `SEC-HUM-001` is separate from resource-bound findings.
- [x] `SEC-HUM-006` is separate from implementation vulnerabilities.
- [x] `SEC-HUM-005` remains related to both `SEC-AI-03` and `SEC-AI-04`.
- [x] AI-only is explicitly recorded as empty.
- [x] Checked-clean areas remain clean-area results.
- [x] Direct evidence, inference, course limitations, and wider-deployment concerns remain distinguished.
- [x] Time-sensitive evidence is qualified.
- [x] No fix is represented as implemented.
- [x] No application behavior was changed.
