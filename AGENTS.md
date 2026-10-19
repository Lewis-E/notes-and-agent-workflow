This directory stores durable work context, agentic workflow development, and standalone reusable skills. Each `./work` subdirectory contains project context as YAML and Markdown files. Actual development for work happens in external directories, while research, plans, and progress tracking are stored here as context. Agentic workflows and their supporting tools—subagents, workflow-specific skills, prompts, and templates—are developed and stored in `./workflows`. Independently invokable capabilities are developed and stored in `workflows/standalone-skills/`.

## Work
A `./work` project may be a single idea, a bug investigation, work relating to one ticket or work relating to a whole collection of tickets, a new feature, or an entire new product. **Every session may be disposable; the work directory must contain enough current state for a different session to continue safely.** Each `work/<name>` directory is its own local Git repository, separate from the implementation and testing repositories it coordinates.

Work follows this process:
* `/skill:start-work`
* `/skill:context-and-requirements`
* `/skill:plan`
* `/skill:plan-execution`
* `/skill:review-work`
* `/skill:finish-work`

At any point within the workflow we may need to `/skill:resume-work` to load context into a new session and `/skill:maintain-work-context` to keep the `./work` directory up-to-date with session progress.

The lifecycle should allow loops:
* `/skill:plan` → `/skill:context-and-requirements`, when problems were found during plan review
* `/skill:review-work` → `/skill:plan-execution`, when problems were found during code review
* `/skill:plan-execution` → `/skill:plan`, when implementation reveals concrete evidence that invalidates the approved delivery or verification strategy
* `/skill:plan-execution` → `/skill:context-and-requirements`, when implementation reveals a missing requirement or stakeholder decision

Before a lifecycle transition, reconcile and commit the work-context repository, then leave it clean. Inspect only repositories that the transition depends on, and report transition issues with human readable descriptions, not commit hashes. When a checkpoint depends on external repository state, record the relevant repository, branch, and commit ID in `agent-journal.md`; cross-repository commits are not atomic.

Workflow state is recorded in `work.yaml`. `AGENTS.md` contains only the project's brief what-and-why thesis and core principles for judgment calls about unforeseen tradeoffs—not individual task instructions. A test for a good agent file is: completely rewriting the implementation plan should not require changing the agent file. `PLAN.md` contains the concise execution checklist, current requirements, non-goals, decisions, and open questions. Concrete instructions may be abstracted into a reusable principle in `AGENTS.md`, but the exact contract remains in `PLAN.md`. `PLAN.md` is human-facing, and so should not contain commit hashes or lists of cli commands -- those go in the `agent-journal.md`. `agent-journal.md` is the append-only chronological record of work, including superseded decisions, checks, findings, checkpoints, and relevant external commits. Preserve full reviewer output beneath `plan-reviews/` and `implementation-reviews/`, with concise dispositions and artifact links in the journal. If the current task depends on recent history, read a bounded tail. Search by gate, item ID, repository, commit, check, or finding when older context is needed. `/skill:maintain-work-context` updates these files.

A work repository provides local durable history, not backup. Remotes are optional and must never be created, pushed, or published automatically. Work repositories must not contain secrets or downloaded credentials. Workflow commands must address the nested repository explicitly, such as `git -C work/<name> status`, because the parent repository ignores `work/*` and cannot report nested changes.

Move finished work repositories to `work-archive/<name>`. The parent repository ignores the entire `work-archive/` directory, so archived projects retain their local history without appearing in this repository's status.

## Workflows
- Subagent sessions represent useful context boundaries, not mandatory handoffs. Keep work in the parent when delegation would add more coordination than speed or insight.
- Default to the smallest useful result, early human-visible progress, existing repository patterns, and trusting unchanged code and automation. Give short regular reports in the main thread for long running work.
- Keep total scope MVP-sized, but decompose approved work into small ordered checklist steps with one primary change each. Split helper creation, behavior/data population, integration, worthwhile test contracts, and separate validation when they can proceed or fail independently. Small steps do not require separate workers, reviews, commits, or checkpoints.
- Add work, research, verification, or reviewer spawns only for an explicit requirement, a necessary dependency, or a plausible failure supported by current evidence. Do not add parity, best-practice, hardening, trial-run, or redundant work by default.
- Trust passing CI instead of re-running the checks. If a human decides how much testing is enough, respect that and report the remaining risks instead of adding more testing.
- Use one plan review by default, no per-item implementation review by default, and one suitable final reviewer unless the human waives review or concrete risk justifies a different boundary.
- Skills under `workflows/skills/` implement lifecycle steps such as interviewing the user, writing a plan, or opening a PR. They are not general-purpose capabilities.
- Workflow skills should stay under 500 words and use reference documents when they need more context. However, it is better to go over 500 words than to destroy meaning.
- Pi loads `workflows/` as a local package; see `workflows/README.md`.
- Delivery and verification follow the [delivery and verification strategy](workflows/references/delivery-and-verification-strategy.md).

## Skills

**`workflows/standalone-skills/` contains independently invokable capabilities and their domain-specific supporting tools.** A skill belongs here when it is useful outside the agentic work lifecycle; a skill that exists only to implement a lifecycle step belongs in `workflows/skills/` instead.

- Each skill directory must contain `SKILL.md` and an `AGENTS.md` describing its purpose, boundaries, dependencies, and maintenance rules.
- Keep detailed domain guidance in `references/` so `SKILL.md` remains focused on invocation and execution.
- Skills may depend on other skills, but the dependency and handoff must be explicit in both skills' documentation.
- Domain-specific scripts shared by multiple skills should use an explicit directory name rather than a generic top-level `scripts/` name.
