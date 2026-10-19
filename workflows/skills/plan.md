---
name: plan
description: Use this skill to create the smallest executable plan, apply one proportional review when warranted, and obtain human approval.
---

# Plan

This skill owns `plan`, `plan-reviewed`, and `plan-approved`; `/skill:maintain-work-context` owns checkpoints. Follow the [artifact boundary](../references/artifact-boundary.md), [delivery and verification strategy](../references/delivery-and-verification-strategy.md), and [human review packet](../references/human-review-packet.md).

## Choose the Smallest Delivery

Read `work.yaml`, `AGENTS.md`, `PLAN.md`, decision-relevant research, and [`workflow-policy.json`](../workflow-policy.json). Inspect only facts needed to shape the change; trust unchanged behavior and automation.

Apply the artifact boundary. If a different implementation would change the thesis or principles, return to `/skill:context-and-requirements`. Recommend the smallest existing-pattern approach, asking the human only when alternatives materially differ in outcome, ownership, cost, or risk.

Keep only approved outcomes, necessities, and responses to evidenced plausible failures. Delete optional polish, parity, hardening, trial runs, and checks that couldn't change the outcome. If removing work still meets the contract without unacceptable evidenced risk, remove it.

Plan for conversations with other teams to happen in the pull request; do not delay a pull request on the results of a conversation. Never plan a step before the PR that asks a team whether they will review or accept a change. Put design questions and known gaps in PR descriptions.

Keep requirements, constraints, non-goals, invariants, acceptance criteria, decisions, and verification limits under `Decisions`; keep only unresolved blocking choices under `Open Questions`.

## Write Small Ordered Steps

The whole plan is the MVP; each checkbox is a small implementation step, not a miniature deliverable. Give it one primary change and a done state we can implement and inspect without unpacking independent clauses.

Split parts that can be implemented, inspected, reordered, or fail independently. Helper/interface creation, rule or data population with source rationale, behavior changes, call-site integration, and outside validation are usually separate steps. Sharing a repository, file, or feature is not a reason to merge them. If “and” joins separately meaningful changes, split them. Run-on sentences with `;` are often a sign of overcomplicated steps. Think about an overwhelmed reader managing many tasks at once-- is each task small enough for that reader to understand, but meaningful enough to be worth understanding?

Use work-area headings with unique uppercase prefixes and stable IDs formatted `**[PREFIX-NN]**`. Passing selected tests is implicit in completing the responsible implementation step; never add a “run tests” checkbox. Keep approved integration or manual validation separate only when it exercises a different boundary. Existing CI is background evidence, not a task.

Let plan order and hierarchy show dependencies. A worthwhile behavior test may be an earlier step when it defines the contract and can fail for the expected reason; the implementation step makes it pass. Do not force red-green separation for trivial tests.

Use hierarchy to make plans readable. Work-area headings and indentation and nested lists are good tools for implying meaning and relating tasks without needing more words.

We don't need to group tasks into one step to batch them. Plan execution may batch adjacent ready steps while preserving order and completion marks. This includes batching workers, reviews, commits, and checkpoints.

Keep procedures and evidence in research and chronology in `agent-journal.md`. Never include code, commit messages, or workflow bookkeeping. Request `plan` when coherent.

## Review Once and Approve

Show uncertain step boundaries to the human before review. Skip independent review for a tiny low-risk plan or human waiver; record why and request `plan-reviewed`.

Otherwise dispatch `plan-reviewer` once with fresh context, artifact paths, relevant research, and repository anchors. Preserve its output under `plan-reviews/`. The parent validates findings, splits oversized steps, removes make-work, applies corrections, and proceeds. Another review requires a human request or a stale or wrong first target.

Present the corrected plan without reconfirming unchanged decisions. Request `plan-approved` only after explicit approval, a signed checkpoint, and a clean work repository.
