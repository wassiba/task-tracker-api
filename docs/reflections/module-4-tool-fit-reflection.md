# Module 4 Tool-Fit Reflection

During the course, I used GitHub Copilot, Cursor, Claude Code, and ChatGPT in different stages of the Task Tracker project. Using them for different kinds of work taught me that the most suitable tool depends on the task and workflow, not on declaring one tool universally superior. This reflection compares what each tool did well, where it needed the most scrutiny, and what verification habits I intend to keep.

## GitHub Copilot: Inline Completion for Bounded Frontend Work

I used Copilot mainly for the Kanban frontend: building and refining the HTML/CSS/JS board, wiring it to the FastAPI backend, adding filters, and implementing the create/edit task modal and drag-and-drop status updates. Its strength was translating already-scoped, already-reviewed prompts (usually prepared with ChatGPT first) into working code directly in the editor, especially for repetitive patterns like event handlers, fetch calls, and state-reset logic. Its main limitation was that its suggestions were shaped mostly by the code immediately around the cursor, so they could look locally correct while missing wider rules, such as backend-authoritative updates or preserving form input after a 422 response. Accepting a suggestion with Tab only meant it had been inserted, not that it was correct; every change still needed browser checks, tests, and a Git diff review.

## Cursor: Structured, Repository-Aware Backend Generation

Cursor did the heavy lifting for the Module 2 backend: the Pydantic models, the in-memory storage layer, the five CRUD routes, the status-transition business rules, and the pytest suite. Because it could read real project files through explicit `@` references, it avoided inventing structure that didn't match the repository, and it was well suited to larger, multi-file, well-specified tasks. But it also created real friction: on a vague prompt it modified `app/main.py` and briefly created an unrequested test file, and on another task it touched the existing `/health` endpoint when the request was scoped elsewhere. That taught me to open a fresh chat per logical task, name the exact files allowed to change, and review every modified or newly created path before accepting anything — strict prompts, not trust, were what made its output reliable.

## Claude Code: Repository-Wide Execution Under Supervision

Module 4 was Claude Code's domain: CI workflow creation and auditing, the Docker build and container verification, documentation rewriting against a claim-vs-reality audit, the AI-review triage log, the in-memory storage technical decision note, and the Git workflow around all of it. Its value was combining repository inspection, file edits, terminal commands, and Git operations in one place, with the ability to propose a plan before touching anything. But that same reach is why the actions with real effect — file overwrites, the intentional red-run test failure, Docker builds, staging, commits, and pushes — needed the most careful approval and independent verification, not just a confident-sounding report. The clearest example was the Part 4.5 review itself: Claude Code flagged the README's Python-version wording as unsupported based on the local virtual environment, but that environment was git-ignored and the tracked CI evidence (Python 3.11, 37 passed) directly contradicted the finding. A plausible AI conclusion turned out to be wrong, and only checking it against tracked evidence caught that.

## ChatGPT: Course Analysis and Continuity, Not Direct Editing

In this project, I used ChatGPT mainly outside the Task Tracker repository as a mentor, planner, reviewer, and Knowledge Base curator. It analyzed course materials, improved prompts, guided implementation checkpoints, reviewed Claude Code reports independently, preserved continuity between modules, and maintained the external course Knowledge Base. This differed from Cursor, Copilot, and Claude Code, which operated directly inside or immediately around the Task Tracker code and repository.

## Preferred Tool by Task

For a small line-level completion, I'd reach for Copilot. For a visible, file-level or multi-file IDE edit, Cursor. For repository-wide work involving commands, tests, Docker, CI, or Git, Claude Code, with approval checkpoints kept in place. For course analysis, prompt improvement, and Knowledge Base upkeep, ChatGPT.

## The Mistake That Taught Me the Most

The Part 4.5 Python-version finding was the most instructive AI mistake of the course: a technically plausible claim that fell apart once I checked which evidence it actually relied on. It reinforced that a confident finding is not proof, and that ignored local state should never outweigh tracked, reproducible project evidence.

## Verification Habit I'm Keeping

I now treat every AI-generated change or claim as unverified until it's backed by evidence: checking the actual diff, running the relevant tests and the full regression suite, and confirming nothing unrelated changed, before treating any milestone as done.

## No Universal Winner

I used all four tools enough to judge each one in its own role, but not enough, across large enough projects, to call any of them universally better. The course showed me that the tools suit different kinds of work — inline completion, structured multi-file IDE edits, repository-wide terminal execution, and course-level analysis are different problems. This experience gives me a practical basis for choosing a tool according to the task in future projects.

## What I'd Do Differently Next Time

I'd define architecture, scope boundaries, business rules, and verification requirements up front, set project-level instructions and approval boundaries before any implementation began, and break work into small, independently testable milestones from the start — each ending in a real diff review and regression check rather than a trusted report.
