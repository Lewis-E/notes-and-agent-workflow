---
name: plan-execution
description: Use this skill to implement approved checklist results, checked the way the plan describes, and complete the implementation gate.
---

# Plan Execution

This skill owns `implementation`; `/skill:maintain-work-context` owns signed checkpoints. Follow the [artifact boundary](../references/artifact-boundary.md) and [delivery and verification strategy](../references/delivery-and-verification-strategy.md).

## Select the Smallest Ready Batch

Require `plan-approved` and read `AGENTS.md` and `PLAN.md`. The plan is authoritative; core principles guide only unforeseen tradeoffs.

Use supplied plan IDs or the first ready step. Batch adjacent ready steps in one coherent write scope and mark each done state separately. Only parallelize disjoint writes. Small checkbox steps must not multiply assignments, reviews, commits, checkpoints, or validation.

Inspect branch, HEAD, and uncommitted changes to the same files immediately before writing to a repository. Trust recorded state for untouched repositories. Never stash, revert, discard, or overwrite user work without approval.

## Implement Without Expanding

Prefer existing code patterns and automation. Do not add cleanup, parity, hardening, observability, migration support, tests, or infrastructure unless the approved plan requires it or execution reveals concrete evidence that the result cannot function safely without it.

Use the parent session for small coherent work. Dispatch `worker` subagents only when separate context, capability, or parallel ownership materially accelerates delivery. Give subagents a coherent batch, exact boundary, repository state, approved verification, and stopping condition.

Integrate parallel results serially. A conflicting write, changed requirement, or evidenced failure mode returns only the affected work to the human or `/skill:plan`; uncertainty and optional improvements must not expand scope.

## Use Only Approved Evidence

Run only verification selected in the approved plan. If concrete execution evidence calls for a different check, run it only when it stays within the human-approved verification limit; otherwise request the backward transition to `/skill:plan` for human approval. Do not rerun existing CI locally, try to prove unchanged behavior, do trial runs, re-read live systems to confirm a change took effect, or substitute different checks just because the specified checks failed. If automatic CI runs normally, don't also run CI yourself, just record its result.

Do not launch an implementation review for every change. Never review every checkbox or stack reviewers over the same risk. Use a focused review when specific risky boundaries make early feedback cheaper than later rework, or at major checkpoints. Store review results under `implementation-reviews/` so the parent session can reference and validate them.

For a narrow correction, inspect the affected diff and use only the already approved evidence. Don't start another reviewer unless the fix meaningfully changes how things work or the earlier review looked at the wrong version of the change.

## Complete the Result

Check a box when its step is done the way the approved plan describes. For a planned test-first step, the done state may be a focused test that fails for the expected missing behavior; the dependent implementation step must make it pass. Do not add a separate checkbox merely to run a test suite. If the human approved skipping extra checks, write down what could still go wrong instead of proving it some other way. Record changed repositories and commits, available evidence, review output if any, and remaining risk in `agent-journal.md`.

Include the [touched-tests table](../references/delivery-and-verification-strategy.md#report-touched-tests) in the progress report when a batch touches tests. Humans need to be aware of test targets and coverage.

Reconcile each completed batch through one signed work-context checkpoint. Request `implementation` when every required checkbox is complete, then return control for human steering.
