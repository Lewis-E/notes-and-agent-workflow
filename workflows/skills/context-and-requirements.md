---
name: context-and-requirements
description: Use this skill to confirm human context, research how things currently work, and approve requirements before planning.
---

# Context and Requirements

This skill owns `human-context`, `research`, and `context-and-requirements`; `/skill:maintain-work-context` owns their signed checkpoints. Follow the [artifact boundary](../references/artifact-boundary.md) and the [delivery and verification strategy](../references/delivery-and-verification-strategy.md).

## Confirm Only What Is Needed

Start from information the human already supplied. Ask only about a decision that blocks the smallest useful implementation; group related questions in one `ask_user_question` call. Do not run an exhaustive interview, do not ask the human for facts tools can retrieve or test, and do not ask them to reconfirm a prior answer or documented requirement.

Capture the base what-and-why thesis and core principles in `AGENTS.md`. Put exact outcomes, constraints, non-goals, acceptance criteria, named behavior, and finite “do” or “do not” instructions in `PLAN.md` under `Decisions`; put only unresolved choices under `Open Questions`. Abstract shared intent into `AGENTS.md` only when it guides unforeseen tradeoffs, while retaining the exact contract in `PLAN.md`.

Treat scope and verification limits literally. A broad answer such as “strictly everything” closes the whole named category; do not reopen it through narrower interpretations or substitute work. Existing explicit answers satisfy human confirmation. Request the signed `human-context` checkpoint when the brief is sufficient to direct the remaining discovery.

## Research Blocking Unknowns

Research only an unknown that could change requirements or the MVP implementation. Trust current code and automation; do not create lanes to prove unchanged systems work, copy the functionality of similar repositories based on that similarity, or gather optional background. Minimize or avoid searches for best practices unless searching for best practices is one of the project goals.

When the work adds a capability, check whether existing code already provides it in this repository, related repositories, or maintained packages. Find related repositories in repository guidance, including any repository-context skill it names. Record what was searched and any equivalent found.

To answer specific questions about how things currently work, read the repository yourself. Use the configured `researcher` only when source discovery, external evidence, or a distinct session context boundary will help. Resolve the `researcher` binding and required capabilities from `<workflow-root>/role-bindings.json` before dispatch.

When research is needed, create `research/README.md` and one file per necessary lane from the [research lane stubs](../references/research-lanes.md). Give each lane one decision-relevant question, require primary sources where available, and keep its findings, citations, and access gaps in that file. Independent lanes may run concurrently. Researchers write only their assigned work-repository files and never edit target repositories.

If no research is needed, record that the trusted baseline and supplied context were sufficient; do not invent a lane to satisfy the `research` gate. Request the signed `research` checkpoint either way.

## Confirm the Contract

Move decision-relevant conclusions into `PLAN.md`; leave evidence in research. Change `AGENTS.md` only when discovery changes the project's purpose or an enduring principle.

Resolve only ambiguity that affects delivery. Present the exact current contract and obtain confirmation only for decisions not already explicitly approved. A required unresolved choice returns `needs-human`; optional uncertainty is omitted from the MVP. Request `context-and-requirements` and advance to `/skill:plan` when the work repository is clean.
