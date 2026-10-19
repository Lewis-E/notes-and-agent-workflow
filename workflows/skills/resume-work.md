---
name: resume-work
description: Use this skill to reconstruct durable workflow and repository state and identify the next safe action without mutation.
---

# Resume Work

This skill is diagnostic and read-only. Never edit, stage, stash, commit, transition, configure remotes, or repeat an external action. Follow the [artifact boundary](../references/artifact-boundary.md) and trusted-baseline [delivery and verification strategy](../references/delivery-and-verification-strategy.md).

## Reconstruct the Active Boundary

Require the absolute active `<work-dir>` and verify it is the Git top-level containing `work.yaml`. Resolve absolute `<workflow-root>` from the loaded package, or require it. Run the locked state validator before interpreting state.

Read `work.yaml`, `AGENTS.md`, the complete `PLAN.md`, and only research, review evidence, or journal entries relevant to the current phase and pending action. Apply the artifact placement tests and report misplaced task instructions or erased exact requirements without editing them. When `codemode` is available, gather these reads, the validator result, and the work repository's Git state in one script that prints only what the diagnosis needs.

Validate that completed gates form one contiguous ordered prefix. Report a contradictory boundary, but finish the diagnosis. Inspect the work repository's branch, HEAD, signature, staged and unstaged paths, and whether `work.yaml` differs from `HEAD`.

Trust recorded target-repository baselines unless there is an interrupted write, pending external action, reported drift, or overlapping next write. Inspect only those repositories. Do not inventory every configured target, compare unrelated commits, rerun checks, or revalidate completed work merely because the session changed.

## Reconcile Interrupted Work

Treat an interrupted action as potentially completed before its final journal update. For that action only, compare the recorded target with current repository or external state. If a matching run is active, continue it rather than launching a duplicate. If failure or outcome remains unknown, return the exact action to the human without retrying it; unrelated work may continue.

Use `continue` when the next write is safe and evidence is current, `continue-with-warning` when a non-required signal is unknown, and `needs-human` only for the affected action or necessary decision. Human-approved omitted verification is neither stale nor missing. Uncertainty about unchanged baseline behavior does not justify new checks.

## Report the Next Useful Action

Present the [human review packet](../references/human-review-packet.md). Lead with the exact decision or changed state requiring attention. Report the objective, current phase, relevant repository state, pending action, material finding, and the smallest next action that produces progress. Omit routine unchanged inventories and optional follow-up ideas.
