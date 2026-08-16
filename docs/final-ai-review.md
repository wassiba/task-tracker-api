# Final AI Review and Ownership Evidence

## AGENTS.md guardrails

- Repo-specific stack and commands included: yes.
- Docs-first/read-first guardrail included: yes.
- Unexpected `app/` or `frontend/` edits rule included: yes.
- Scope rule applied: the final project added no product feature; the only `app/` edit is the reproduced nullable-title correction described below.

## AI code review mini-log

Review target: the final-project diff in `app/models.py` and `tests/test_tasks.py` for the explicit null PATCH-title defect.

| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| Rejecting explicit `title: null` is necessary because the old validator allowed a non-string value into storage. | Useful | A live PATCH returned HTTP 200 with `"title": null`, contradicting `TaskResponse.title: str` and the documented title rule. | Reproduced before editing; corrected with a before-validator that distinguishes omission from explicit null. |
| The regression test should verify both HTTP 422 and that the stored task remains unchanged. | Useful | A rejection alone is insufficient if storage is mutated before failure. | The focused test performs a GET after the failed PATCH and compares the complete task representation with the pre-request value. |
| Make `TaskUpdate.title` a required `str` to prevent null values. | Wrong | Making the field required would break PATCH partial-update semantics by requiring a title for description-, priority-, assignee-, date-, or status-only updates. | Rejected. The optional field default was retained while explicit null is rejected by validation. Existing partial-update tests remain green. |

Focused verification: `1 passed, 0 failed`. Full final verification: `38 passed, 0 failed, 0 skipped`. Both runs emitted one sandbox-related pytest cache warning that does not affect test execution.

## AI security mini-review

The final review reused the read-only findings reconciled in `docs/security-review.md` and checked them against the current files. None requires an out-of-scope product feature for this submission.

| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| Task routes have no authentication, authorization, or task ownership boundary. | `app/main.py`, `app/models.py`, `README.md` | Valid | Every caller uses one shared in-memory task collection. This is an intentional course limitation, not a newly introduced defect. | Do not expose to untrusted users; define identity and ownership requirements before wider deployment. |
| Text/filter sizes, task count, and list result size are mostly unbounded. | `app/models.py`, `app/main.py`, `app/storage.py` | Valid | The repository supports the observation, but material impact depends on untrusted or high-volume use. | Keep documented as a conditional wider-deployment risk; do not add pagination or product behavior in this project. |
| Dependencies, GitHub Actions tags, runner, and base image use mutable references. | `requirements.txt`, `.github/workflows/ci.yml`, `Dockerfile` | Valid | This is a reproducibility and supply-chain maintenance concern; it is not evidence of a current vulnerability. | Handle through a separate pinning and update-cadence decision, preserving `httpx2` until separately reviewed. |

## Manual security check

I independently reviewed the tracked-file list, ignore rules, Docker build inputs, CI workflow, and final diff. The local `.env` is ignored and untracked; I did not open or copy it. No `.env` file, credential file, production log, personal/customer dataset, or obvious secret placeholder is tracked, and `.dockerignore` prevents environment files and logs from entering the Docker build context. I also confirmed that CI has read-only repository permissions and no deployment or secret-consuming step.

## One AI output I rejected or corrected

An earlier AI review claimed that the ignored local Python 3.14 virtual environment undermined the documented Python 3.11 target. I rejected that conclusion because the virtual environment is untracked, while the repository's authoritative CI and Docker configuration explicitly use Python 3.11 and the recorded CI run for the reviewed commit passed on Python 3.11.15. I retained the documented project target and labeled the stronger tracked and execution evidence instead of changing the project to match one developer's local environment.

## Three AI usage rules

1. Never paste: secrets, raw `.env` contents, credentials, unrestricted production logs, or personal/customer data.
2. Always verify: inspect the exact diff and check claims with the strongest applicable source, test, runtime, browser, CI, or Docker evidence.
3. Record AI contributions by: naming the reviewed artifact, grading comments or findings, recording corrections and rejections, and preserving the commands and results used to decide.

## Ownership statement

I am comfortable submitting this repository as my work because I can explain the purpose and effect of every final change. I reproduced the nullable-title defect before correcting it, reviewed the bounded diff, and verified it with both focused and full regression tests. I independently checked the API, browser flow, Docker runtime, CI configuration, documentation claims, and tracked-file safety boundaries rather than accepting AI wording as proof. I also recorded the limitations and rejected suggestions that were unsupported or outside the course scope.
