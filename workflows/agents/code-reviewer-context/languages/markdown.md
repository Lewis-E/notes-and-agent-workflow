# Markdown

**Owns:** whether changed Markdown is correct, maintainable, discoverable, and usable by its intended human or machine audience.

Name the audience first: human developer, user, stakeholder, LLM/operator, or reviewer. Judge terminology, detail, assumed context, navigability, and actionability for that audience, not for an abstract reader.

## Questions

- Does the document use repository terminology consistently, especially where concepts can be confused, such as logical worker roles versus checkout write ownership?
- Do frontmatter and routing descriptions accurately make the documented capability discoverable and selectable?
- Is there one useful H1, followed by a coherent heading hierarchy and locally consistent heading case and section order?
- Does the document follow applicable local word-budget guidance without deleting necessary context or hiding it in the wrong layer?
- Do links and paths resolve to current targets, and are package-shipped capabilities documented where their intended audience will look?
- Is policy defined once in its owning document and referenced elsewhere, rather than duplicated until copies drift? Has a reference document absorbed instructions or decisions owned by a skill or other authoritative surface?
- Do ownership statements agree across the changed documentation, repository guidance, and actual workflow behavior?
- Do prose-facing tests assert routing or behavior rather than pinning incidental phrases, punctuation, or section placement?
- Can the audience act without unexplained internal jargon? Prefer plain descriptions such as “mandatory test-first ordering” when a phase label alone would not convey the requirement.
- Does every finding cite exact file and line evidence and explain the audience or operational impact?

## Boundaries

Requirements owns whether the requested outcome was delivered; Consumer Experience owns non-document interfaces and journeys; QA owns executable test strategy; Maintainability owns code-reader cost. This lens owns Markdown structure, documentation routing, terminology, ownership, and audience comprehension.

## False-positive guards

- Preserve intentional local conventions; do not impose universal heading, voice, capitalization, or section-order rules.
- Do not copyedit subjective wording. Report prose only when it affects correctness, routing, comprehension, actionability, or maintenance.
- Scale detail to the demonstrated audience and task; concise documentation is not incomplete merely because more could be said.
- Do not demand that every capability be documented everywhere. Identify the audience’s expected discovery surface and the concrete gap.
- Do not report a stale link or contradictory rule without opening the relevant target and verifying the conflict.
