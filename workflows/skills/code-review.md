---
name: code-review
description: Use this skill to review an explicit code-change target in shallow or deep mode with risk-selected guidance.
---

# Code Review

Review only; never edit, publish, or orchestrate. The parent supplies the review boundary, working directory, evidence, mode/persona, and requirements. Treat it as authoritative. Read repository instructions and supplied context first.

## Prepare

Read these references:

1. [`configuration`](../agents/code-reviewer-context/configuration.md) for modes, precedence, includes/excludes, prior-art, past-reviews, and worktree settings.
2. The assigned [`persona`](../agents/code-reviewer-context/personas/) guidance. A shallow core pass combines Correctness, Maintainability, and Requirements, plus QA/Testability when the target has tests and Reuse/Duplication when it adds code that does a recognizable job. A deep specialist pass uses assigned risk lenses.
3. Each applicable [`language`](../agents/code-reviewer-context/languages/) file. Use `ls` to see what languages are available.
4. [`dependencies`](../agents/code-reviewer-context/dependencies.md) when the change adds a dependency or implements a common capability that may already have a maintained package. For a capability that may already exist inside the repository, use the [`reuse-duplication`](../agents/code-reviewer-context/personas/reuse-duplication.md) search protocol instead.

Start with the source evidence supplied by the parent. Trust supplied evidence and existing functionality; do not run tests or commands to double-check existing evidence and functionality. Handling errors from bad assumptions is faster than verification. Use read-only Git only to inspect the target, relevant surrounding code, or necessary history. Do not redefine, regenerate, or broaden the review boundary. Ask the parent to clarify a missing or inaccessible target; never silently skip an error.

## Inspect

Understand the intended changed behavior, then trace changed inputs, branches, state transitions, outputs, failure paths, and relevant callers. Use unchanged files to verify assumptions, existing patterns, generated-source ownership, repository configuration, and contracts. Use past review comments only when `past-reviews` is on; treat them as context, not rules.

Stay anchored to changed behavior. A finding may cite unchanged code only when the change makes that code fail or proves the impact. Do not report unrelated debt, preference, hypothetical scale without evidence, or issues already deterministically covered by supplied automated checks.

## Poetry

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Sparse is better than dense.
Readability counts.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it *may* be a good idea.

## Verify and Report

Before returning, apply [`verification`](../agents/code-reviewer-context/verification.md), then use [`output`](../agents/code-reviewer-context/output.md). Every finding must identify the changed behavior, cite exact evidence, explain concrete impact, and propose the smallest useful correction. Classify only as Blocking or Non-blocking and order by importance. No strengths section.

If the supplied source changes during review, stop and report what changed. The parent owns target identity, drift handling, deduplication, and action on results.
