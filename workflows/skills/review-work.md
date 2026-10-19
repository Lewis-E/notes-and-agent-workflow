---
name: review-work
description: Use this skill to apply one proportional whole-change review or approved waiver and request final human acceptance.
---

# Review Work

This skill decides readiness and owns `final-review`; `/skill:maintain-work-context` owns its signed checkpoint. Follow the [artifact boundary](../references/artifact-boundary.md), [delivery and verification strategy](../references/delivery-and-verification-strategy.md), and [human review packet](../references/human-review-packet.md). Do not publish or finalize work.

## Pin the Changed Target

Require a current `implementation` gate. Read the thesis and core principles in `AGENTS.md` and the exact contract and verification limit in `PLAN.md`. Resolve one target: a pull request, merge-base-aware ref range, or working tree with explicit staged, unstaged, and untracked scope. When `codemode` is available, read the work files and pin the target in one script.

Trust unchanged code and recorded baselines. Confirm only that the review target identifies the intended changed files and has not moved; do not revalidate unaffected repositories, reproduce existing CI, or add checks for preserved behavior without concrete evidence that the change affects it.

Create `implementation-reviews/<review-id>/` and store a concise target manifest, changed-file inventory, diff, and already available check evidence. Do not generate extra evidence for the bundle.

## Review Once

If the human explicitly waived additional verification or independent review, record the skip and the remaining risk the human accepted, prepare the human-facing packet, and request the `final-review` checkpoint without spawning a reviewer.

Otherwise choose one suitable configured `code-reviewer`. Use shallow mode for localized or low-risk changes and deep mode for a changed shared contract, security boundary, data path, large code change, or similar level of risk. Shallow mode already reviews tests when the target touches them. You may choose one or more specialists for any review if needed.

Launch one pass with the pinned target, bundle, project principles, exact requirements, and existing evidence. Reviewers inspect changed behavior and may use unchanged code only as context; they do not rerun checks or search for optional improvements. Preserve the output before interpreting it and confirm the target did not change.

The review-parent only accepts findings tied to changed behavior and the approved contract; it should reject duplicates, pre-existing issues, speculative safeguards and cleanup, and make-work verification. Defer valid non-blocking risks, don't turn them into scope-creep. Report the results and readiness verdict beneath the review directory and link them from `agent-journal.md`.

## Correct Narrowly

Route a supported implementation defect to `/skill:plan-execution`, a plan defect to `/skill:plan`, and missing context or requirements to `/skill:context-and-requirements`. Correct only the supported issue. The parent can inspect narrow corrections without another reviewer. Review again only when a fix meaningfully changes how things work or what they protect, the earlier review looked at the wrong version of the change, or the human asks; never create an automatic loop.

## Request Acceptance

Return `ready` when the target is current, required planned evidence succeeded, and blocking findings are resolved. If the human explicitly approved no extra checks, that meets the plan's requirement. Present the reviewed or explicitly unreviewed target, significant remaining risks, and requested decision. Ask the human to accept or reject; `/skill:finish-work` owns final acceptance and handoff.
