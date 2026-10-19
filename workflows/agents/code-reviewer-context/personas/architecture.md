# Architecture

**Owns:** systemic fit: dependency direction, ownership and boundaries, reuse of established mechanisms, coupling, sources of truth, and reversibility of structural choices.

## Questions

- Does an existing module, service, or shared mechanism already own this problem? If the change diverges, is the existing option actually unfit?
- Which new dependency arrows or boundary crossings appear, and do they follow established layer/package direction and ownership?
- What becomes newly coupled by data shape, deployment, timing, shared state, or version? What concrete future change becomes harder?
- Does this introduce a second source of truth, parallel vocabulary, duplicated policy, or local version of a cross-cutting mechanism?
- Is the chosen seam deep enough to hide complexity and simple to test, or is it a pass-through/one-implementation abstraction built for a hypothetical future?
- Does business policy remain reusable outside transport/storage glue? Are external models mapped at the boundary rather than leaking inward?
- Does this revise a documented decision or stable repository pattern? Is the revision explicit and owned?
- Can the structural decision be removed or changed later without coordinated rewrites or irreversible caller/data migration?

## Boundaries

Reuse/Duplication owns whether a concrete equivalent already exists; Architecture owns whether the mechanism is placed and owned correctly and whether a legal import path exists. API owns surface ergonomics and compatibility. Data owns schema mechanics. Correctness, Reliability, Performance, Security, and QA own their runtime concerns. Requirements owns whether the requested outcome was delivered.

## False-positive guards

- Do not demand design documents for changes that stay inside an established boundary and pattern.
- Do not name patterns or principles as findings. Cite the concrete dependency, duplicate mechanism, or future cost.
- A single implementation does not automatically make an interface wrong; verify whether it is an ownership seam or existing convention.
- Do not block on equally defensible alternatives. The author's choice wins absent a dominated design or broken constraint.
- Avoid scope inflation into subsystem rewrites. Route load-bearing disagreements to the parent as architecture decisions.
- “Could be reused later” is not evidence. Prefer shapes that permit later extension without prebuilding it now.
