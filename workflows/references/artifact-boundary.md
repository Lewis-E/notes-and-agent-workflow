# Artifact Boundary

**Lifecycle process and evidence artifacts belong in the active nested work repository, never in target repositories.** This includes context, plans, checklists, `agent-journal.md`, findings, validation results, and other workflow-only material.

Target repositories receive only independently justified production code, tests, configuration, or genuine product documentation. A workflow artifact does not become product documentation merely because it is Markdown or useful during implementation.

External handoffs do not widen this boundary. Never automate deployment. Never automate release. Never mark a pull request ready. Never merge. A configured finish flow may push an accepted implementation branch and open or reuse a draft pull request, but it must keep workflow evidence in the work repository.

## AGENTS.md, PLAN.md, and Agent Journal

**`AGENTS.md` is the project's thesis and core principles, `PLAN.md` is the current requirements and execution contract, and `agent-journal.md` is the chronological workflow record.**

### AGENTS.md: thesis and vibes

Keep this file brief enough to understand at a glance: one thesis paragraph and, only when useful, a few enduring product or design principles. Capture the base knowledge: what are we working on, whose problem matters, what outcome is worth pursuing, and why. Then state the principles that should guide judgment calls. This is the project's identity and vibes, not an exhaustive specification. The thesis and principles should not change even if implementation plans completely change.

Do not put individual task instructions in `AGENTS.md`. Exclude repository-by-repository behavior, implementation steps, workflow names, version or tag rules, sequencing, credential mechanisms, actor restrictions, rollout instructions, validation exceptions, acceptance criteria, and finite “do not” lists. A fact is not appropriate merely because it is important or stable.

Abstract concrete instructions when they reveal an enduring principle, but keep the exact instructions in `PLAN.md`. For example, replace “do not add workflow X, signing method Y, app Z, or credential Q” with a principle such as “do not add functionality merely to mirror adjacent repositories or generic best practices unless a human explicitly planned it; favor simple infrastructure and a small trust surface.” The abstraction must guide choices not already named by the current plan; it must not disguise a task list as prose.

Use two tests. First, rewriting the implementation plan from scratch should not require changing `AGENTS.md`; a changed project purpose or enduring principle is context discovery, not replanning. Second, a principle belongs there only if it helps decide an unforeseen tradeoff; a statement whose completion or compliance can be checked against the current change belongs in `PLAN.md`. Named systems belong in the thesis only when essential to answering what the project is, not to prescribe their implementation.

### PLAN.md: current contract

Put the approved requirements, constraints, non-goals, invariants, acceptance criteria, implementation decisions, repository-specific behavior, and exact “do” or “do not” instructions in `PLAN.md` under `Decisions`. Put unresolved choices in `Open Questions`. Put concrete delivery and validation work in the checklist. The plan may link to research for detail and evidence.

The checklist decomposes the MVP into small ordered implementation steps under work-area headings; a checkbox need not be independently shippable. Each step has one primary change and a clear done state. Split helper/interface creation, behavior or data population, call-site integration, worthwhile test contracts, and separate integration validation when they can be implemented, inspected, reordered, or fail independently. Small steps may still run in one worker batch and one checkpoint.

Every checkbox under one heading shares that heading's unique ID prefix. A checked box means its step was done the way the approved plan describes. For a planned test-first step, that may mean the focused test fails for the expected missing behavior; the later implementation step makes it pass. If the human explicitly agreed to skip extra checks, that also counts as done. Do not add a second validation narrative or a checkbox merely to run required tests.

### Research and history

Keep sourced facts and investigation detail in `research/`. Append superseded decisions, implementation events, checks, findings, and handoffs to `agent-journal.md`; do not preserve history by bloating either current file.

## Review Evidence

Keep reviewer output in two directories at the work-repository root:

- `plan-reviews/` for independent plan-review output; and
- `implementation-reviews/` for every implementation review, whether mid-implementation or whole-change, including review bundles, reviewer output, and dispositions.

Create these directories when the first artifact is written.
