# My Personal AI Playbook

> A one-page, evidence-backed guide to how I use AI-assisted coding tools.

## When I reach for AI first

- For ambiguous or evidence-sensitive work, I start with ChatGPT for course-level framing and Codex App for repository-grounded planning. The Part 5.4 comments exercise showed why: generic ideas became a bounded proposal aligned with the Task Tracker architecture.
- After approval, I use Cursor for structured backend work, Copilot for bounded frontend work, or Claude Code for supervised repository-wide execution. Tests, runtime or browser checks, and the exact diff determine acceptance.

## When I do not reach for AI first

- I pause before sharing secrets, personal or customer data, unrestricted logs, regulated or confidential information, or material with uncertain authorization. I classify, minimize, sanitize, and verify the environment first; otherwise, I use local or manual analysis.
- I reason independently when the task tests my understanding or involves security, privacy, ownership, architecture, or user impact. AI may challenge me, but it does not decide for me. The rejected Part 4.5 Python-version finding proved that credible wording can be wrong.

## My non-negotiables

- I do not share raw `.env` contents, credentials, keys, tokens, production secrets, real customer or regulated data, unrestricted production logs, or material without confirmed AI-processing authorization. I use `.env.example`, synthetic data, placeholders, or a minimal sanitized excerpt in an approved environment.
- Approval is operation- and scope-specific. Editing does not authorize expansion, dependencies, Docker, CI, external services, Git mutations, deployment, publication, or destructive actions.
- Work outside the objective or file allowlist is unauthorized. I stop, report it, inspect the diff and untracked files, and request a separate scope decision.

## My review rules

- I inspect the complete diff, modified and untracked paths, nearby context, affected tests, and tracked configuration. I check for scope drift, secrets, placeholders, fabricated claims, weakened tests, temporary code, and unrelated changes.
- Verification matches the artifact: focused and regression tests for code; factual and structural checks for documentation; browser checks for frontend work; and static plus runtime or external evidence for CI, Docker, dependencies, infrastructure, or deployment.
- I reject claims contradicted by stronger evidence and changes that weaken tests, hide failures, expose secrets, or exceed scope. I pause over conflicts, missing authorization, unexplained effects, or unreproducible success. Plausibility is not evidence.

## What I am still figuring out

- Tool roles overlap. A future comments implementation could compare ChatGPT with Codex for planning, Codex with Claude Code for review, and Cursor with Copilot for implementation, judged by verified time, correction effort, scope discipline, and evidence quality.
- I still need authoritative clarification about submitting course and third-party materials to AI. Until then, I prefer my own notes, minimal summaries, owned or public evidence, synthetic substitutes, and local analysis.

## Decision Card

- For a new feature I reach for: ChatGPT for course-level analysis, then Codex App for read-only repository planning; after approval, I use a scope-matched implementation tool and return to Codex for independent review.
- For a code review I reach for: Claude Code for a bounded read-only first pass; I classify findings against the diff, tracked evidence, tests, CI, and project constraints.
- For debugging I reach for: Cursor in diagnosis-only mode for localized failures, escalating to supervised Claude Code for Docker, CI, environment, or cross-cutting failures.
- For infrastructure I reach for: Claude Code in manual-approval mode, one consequential stage at a time, with static and runtime evidence.
- I will never paste: Secrets or raw `.env` contents; personal, customer, or regulated data; unrestricted production logs; or material without confirmed AI-processing authorization.
- My one rule is: Before I accept or act on any AI-generated change or claim, I will inspect the exact affected diff and verify it against tracked, reproducible evidence.

## Thirty-Day Review

- Review date: September 15, 2026
- Question to answer: Am I still following this playbook?
