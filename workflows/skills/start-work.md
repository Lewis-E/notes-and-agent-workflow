---
name: start-work
description: Use this skill to create a new work item and its first signed checkpoint.
---

# Start Work

This skill owns the `started` gate. `/skill:maintain-work-context` validates runtime paths and creates the signed checkpoint. Keep every lifecycle process artifact in the nested work repository and separate the current plan from history as described by the [artifact boundary](../references/artifact-boundary.md).

## Gather the Request

Use supplied information to obtain a short description of the work. Determine its title, kind, affected directories, and optional ticket URL. Use `ask_user_question` only for a missing fact that blocks creation; group questions and do not ask the human to repeat or reconfirm information already provided.

Resolve `<workflow-root>` from the loaded package source and determine the absolute `<work-dir>` beneath the Notes `work/` directory. If `<work-dir>` already exists and is non-empty, stop rather than overwrite it; use `/skill:resume-work` for an existing item.

## Create the Work Repository

1. Create `<work-dir>` and initialize it as a local Git repository on `main`. Do not configure a remote.
2. Use the locked state CLI to create `work.yaml`. Repeat `--directory` for work affecting multiple directories:

```bash
uv run --project <workflow-root> --locked work-yaml --work-dir <work-dir> create --kind <kind> --directory <affected-directory> [--ticket <url>]
```

Run the same locked command with `--work-dir <work-dir> create --help` for allowed kinds and complete usage. Do not create or edit `work.yaml` by hand.

3. Create concise `AGENTS.md`, `PLAN.md`, and `agent-journal.md` files. Add a small `.gitignore` for temporary files, generated caches, and local secrets, and never add secrets or downloaded credentials.

Use this `AGENTS.md` shape and the strict placement rules in the artifact boundary:

```markdown
# Project Title

<One short thesis paragraph: what we are working on, whose problem matters, the outcome worth pursuing, and why.>

## Product Principles

- <A list of decisions making principles for handling unforeseen tradeoffs —the project's vibes— not task instructions.>

## Context

See @PLAN.md for the task execution checklist, requirements, constraints, non-goals, decisions, and open questions. See @agent-journal.md for chronological workflow history.
```

Keep the initial `AGENTS.md` file under 150 words unless the human explicitly asks for more project-level framing. Do not copy the initial prompt into it. **Write it so a complete replacement of the implementation plan would not require changing the thesis or principles.** Put every specific requirement, named implementation behavior, acceptance criterion, and finite “do” or “do not” instruction in `PLAN.md`, even when it is important or expected to remain stable. When concrete instructions imply a broader decision rule, state that abstraction as a core principle and retain the exact instances in `PLAN.md`; the principle must guide choices the current task did not enumerate.

Use this `PLAN.md` shape:

```markdown
# Plan

See @AGENTS.md for the project thesis and core principles.

## Decisions

Record current requirements, constraints, non-goals, acceptance criteria, implementation and verification limits, and their rationale.

## Open Questions

Record unresolved requirements, tradeoffs, and assumptions without inventing answers.

## Checklist

- [ ] Complete context and requirements.
- [ ] Replace this bootstrap checklist with an approved execution plan.
```

Use this `agent-journal.md` shape, replacing the timestamp when the file is created:

```markdown
# Agent Journal

Append concise chronological entries with the newest entry at the end. If the current task depends on recent history, a bounded tail of this file is useful. This file can be searched by gate, item ID, repository, commit, check, or finding when older context is needed.

## YYYY-MM-DDTHH:MM:SSZ — started

- Created the work item.
- Record decisions, assumptions, open questions, evidence, and handoffs here. Keep records concise.
```

Keep the `AGENTS.md` thesis stable. Preserve consequential bootstrap context in the journal when the checklist is replaced; keep current specifics in `PLAN.md`.

## Checkpoint and Route

Request the `started` checkpoint from `/skill:maintain-work-context`, passing absolute `<work-dir>` and `<workflow-root>` values. Require a valid signed commit and a clean work repository; do not run a second commit flow here. Then route to `/skill:context-and-requirements`, which confirms human context before launching research.
