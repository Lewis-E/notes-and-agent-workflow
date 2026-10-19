---
name: maintain-work-context
description: Use this skill to reconcile durable context and own lifecycle transitions and signed checkpoints.
---

# Maintain Work Context

This skill is the sole transition and checkpoint owner. Phase skills own their evidence; this skill validates the requested transition and commits the reconciled work repository. Follow the [artifact boundary](../references/artifact-boundary.md) and trust recorded state outside the transition's actual scope.

## Validate Runtime Paths

Require absolute `<workflow-root>` and `<work-dir>` values. Resolve `<workflow-root>` from the loaded package containing `package.json`, `skills/`, `scripts/`, and `references/`, or require it explicitly. Verify `<work-dir>` is the Git top-level containing `work.yaml`; `/skill:start-work` may pass an absent destination until creation. Never derive paths from the shell's current directory.

Use those paths for state commands:

```bash
uv run --project <workflow-root> --locked work-yaml --work-dir <work-dir> validate
uv run --project <workflow-root> --locked work-yaml --work-dir <work-dir> set <field> <value>
uv run --project <workflow-root> --locked work-yaml --work-dir <work-dir> transition <gate> --support-current
```

Never edit `work.yaml` directly. Use `transition` for lifecycle state and `set` only for non-status fields.

## Reconcile What Changed

Read and validate `work.yaml`, `AGENTS.md`, and the complete `PLAN.md`; read only the journal tail or searched entries needed for this transition. Check the work repository. When `codemode` is available, batch these reads and checks in one script and print only what the transition needs. Inspect a target repository only when the requested checkpoint depends on a new write, commit, check, or reported drift there. Do not repeatedly inventory every configured repository or re-prove an unchanged baseline.

Immediately before relying on a target write, report its path, branch, HEAD, and any uncommitted changes to the files it will touch. Treat unrelated commits and uncommitted changes as normal. Refresh a recorded baseline only when relevant state changed. Never stash, revert, discard, or overwrite user work without approval.

Keep the base what-and-why thesis and core principles in `AGENTS.md`; replacing the implementation plan must not change them. Keep the exact current contract and checklist in `PLAN.md`. Keep sourced detail in research and append only consequential decisions, relevant external commits, interruptions, findings, evidence, and checkpoint outcomes to `agent-journal.md`. A task-list `AGENTS.md` or an abstraction that erased exact requirements is not reconciled.

A failed or unknown external action returns to the human without automatic retry. Pause only the affected operation for a conflicting write, unsafe transition, failed required evidence, or unresolved necessary decision. Human-approved omitted verification is not failed evidence.

## Transition and Checkpoint

Verify ordered prerequisites and only the evidence required by the requested gate. Invoke `transition <gate> --support-current`; a rejected transition must leave `work.yaml` unchanged, and a backward transition invalidates its destination and later gates.

Ensure workflow artifacts remain in the work repository and contain no secrets. Append a concise timestamped journal entry naming the gate or checklist batch, changed repository commits, available evidence, outcome, and next necessary action. Do not create history for routine unchanged state.

Stage the reconciled checkpoint and commit with signing enabled. If signing fails, leave changes staged, report the checkpoint incomplete, and never disable signing or create an unsigned commit. After success, run `git verify-commit HEAD` and require a clean work repository. Report the signed HEAD, relevant target state, preserved overlapping work, and significant remaining risk. Never configure or push a remote automatically.
