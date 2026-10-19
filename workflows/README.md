# Notes Workflows

**`notes-workflows` is a Pi package for a notes-centered development lifecycle.** It exposes native `/skill:<name>` commands while keeping requirements, research, plans, and review evidence separate from the repositories that receive the product change.

## Installation

### Dependencies

You need:

- Pi;
- [Pi Subagents](https://github.com/nicobailon/pi-subagents), which supplies the subagent runtime and default worker agent;
- a Pi structured-question capability that exposes `ask_user_question`;
- Python 3.11 or newer; and
- `uv`.

The package is not published to npm. Load it from a local checkout of this repository.

### Install the Package

Replace `<notes-checkout>` with the absolute path to your checkout:

```text
pi install <notes-checkout>/workflows
pi list
```

`pi list` should show the resolved `workflows` directory once. Pi may store the source as a relative settings entry, so compare resolved locations rather than raw settings text.

To remove this local package intentionally, run:

```text
pi remove <notes-checkout>/workflows
```

Pi loads lifecycle skills from [`skills/`](skills/) and the packaged researcher, plan reviewer, and code reviewer from [`agents/`](agents/). The packaged researcher uses the same runtime name, `researcher`, so Pi Subagents resolves it at package priority instead of the lower-priority builtin. It adds stratified sampling and script-first processing rules for large datasets. The original builtin remains installed with Pi Subagents and becomes active again if this package stops exporting its replacement.

Keep `pi.subagents.agents` in [`package.json`](package.json) pointed at the `./agents` directory. Pi Subagents recursively scans declared directories; listing individual Markdown files prevents these agents from being discovered. Restart Pi after changing the package manifest, then inspect `researcher` in `/subagents` and confirm its source is `notes-workflows` and its path ends with `workflows/agents/researcher.md`. Pi does not copy these resources into a target repository.

## Workflow Lifecycle

Start Pi in a target repository, then invoke `/skill:start-work` with the absolute Notes `work/` destination for the nested work repository. This kicks off the workflow.

#### Workflow Values
* Default to the smallest useful result and readable steps and reports
* Trust unchanged code and automation to speed up work
* Work, verification, and review steps require an explicit purpose. We avoid optional work.
* Batch parallel steps to speed up work, but avoid multiplying reviews and checkpoints.

#### Workflow Documents
The workflow keeps `work.yaml`, `AGENTS.md`, `PLAN.md`, `agent-journal.md`, research, available validation evidence, and review findings in that work repository.

* `AGENTS.md` is a brief what-and-why thesis plus core principles that can and must survive a complete replan. It never carries the task list or exact contract.
* `PLAN.md` contains the approved work checklist, current requirements, constraints, non-goals, decisions, and open questions. It's a human facing document that prioritizes being readable, but can be completely rewritten as needed if implementation plans change.
* `agent-journal.md` contains the chronological work history with LLM-facing data. It's a honeypot for the LLM's constant desire to write things down so we can avoid spamming the user-facing thread.
* Target repositories receive product code, tests, configuration, and genuine product documentation, but never workflow commentary or evidence.

#### Workflow Process
Use the phase skills in order:

1. `/skill:start-work` creates the work repository and first signed checkpoint.
2. `/skill:context-and-requirements` confirms the human brief and researches only decision-blocking unknowns.
3. `/skill:plan` creates the MVP checklist, uses at most one default independent review, and requests human approval.
4. `/skill:plan-execution` implements the checklist, checked the way the approved plan describes, without per-item review by default.
5. `/skill:review-work` uses one proportional whole-change reviewer, or records an approved review waiver, and asks for explicit final acceptance.
6. `/skill:finish-work` records acceptance, produces the final handoff, and completes the lifecycle.

Use `/skill:resume-work` for a read-only reconstruction after interruption. `/skill:maintain-work-context` is the only skill that changes lifecycle gates or creates work-context checkpoints.

The completion gates are:

```text
started → human-context → research → context-and-requirements → plan →
plan-reviewed → plan-approved → implementation → final-review →
final-acceptance → finished
```

Human approval is explicit at `human-context`, `context-and-requirements`, `plan-approved`, and `final-acceptance`. A backward transition invalidates its destination and every later gate when new evidence changes the contract or delivered result, while Git and `agent-journal.md` preserve history.

The final handoff is either a local summary or, when explicitly configured and safe, a pushed accepted branch with a draft pull request. The workflow should never mark a pull request ready, merges, deploys, releases, or changes ticket status without a human ordering this action.

## Code Review Helper

[`skills/code-review.md`](skills/code-review.md) is a helper skill used by the lifecycle's configured `code-reviewer`. Parent workflow skills define and prepare the review target. The reviewer accepts that boundary, inspects relevant source and history with read-only Git, and returns findings without editing or publishing.

## Customize Subagent Roles and Timing

The lifecycle uses logical `researcher`, `worker`, `plan-reviewer`, and `code-reviewer` roles. Map them to available agents in [`role-bindings.json`](role-bindings.json). The workflows package provides the default researcher and dedicated reviewers; Pi Subagents provides their runtime and the default worker. A replacement must provide the capabilities listed for its logical role. Each role-consuming skill reads the mapping, checks suitability, and dispatches the mapped name.

Set collaboration timing in [`workflow-policy.json`](workflow-policy.json). `safe-checkpoint-minutes` guides when an agent should wrap up at a coherent boundary, while `feedback-deadline-minutes` guides when to return control. These values are customizable runtime guidance, not plan content, absolute deadlines, or blockers. Shorten them for hands-on steering or lengthen them for larger coherent items; keep oversized work visible as separate checklist items rather than hidden runtime slices.

Because Pi loads the checkout directly, committed changes to either configuration affect future sessions that use that source.
