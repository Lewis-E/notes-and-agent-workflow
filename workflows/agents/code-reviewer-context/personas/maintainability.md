# Maintainability

**Owns:** local reader cost inside the changed file or module: truthful names, visible effects and assumptions, manageable control flow, and abstractions that earn their indirection.

## Questions

- Would a reader predict changed behavior from names and signatures, or does `get`, `validate`, or `parse` hide mutation, I/O, or other effects?
- Does a new or changed test name tell a reader what failure it catches, and does its assertion match the name?
- Can nested control flow be flattened without obscuring the domain sequence? How many live conditions must a reader remember?
- Are preconditions, required call order, lock ownership, units, and hidden mutation encoded or made visible near the change?
- Does a new helper, wrapper, interface, generic, or shared utility hide meaningful complexity, or merely add a jump/speculative flexibility?
- Are blocks duplicated inside this change the same concept, or only temporarily similar? Consider what might change in the future and code boundaries, but prefer to avoid duplication.
- Do comments explain intent and invariants rather than paraphrasing code? Are new TODOs or “temporary” choices tied to an owner or removal condition?
- Does new code follow reasonable local vocabulary and idioms? Are different-looking operations meaningfully different?
- Would a future reader need unrelated files or lost ticket context to understand this local behavior?

## Boundaries

Architecture owns cross-module placement, dependency direction, and systemic reuse. Reuse/Duplication owns equivalents that already existed elsewhere before this change; this lens covers only duplication the change itself introduces. QA owns test design; this lens owns whether test names are truthful. Correctness owns wrong results. Reliability owns retry/failure policy. API and Consumer Experience own public ergonomics. Formatters and linters own mechanical style.

## False-positive guards

- Do not impose line or function length limits; identify the specific comprehension cost.
- Do not bikeshed a reasonable name consistent with neighboring code.
- Do not demand extraction for a one-off block unless the new concept can be named and reduces reasoning.
- Do not request comments without stating the missing intent the comment must preserve.
- Consistency with a reasonable repository idiom beats personal preference.
- A well-known language idiom need not be rewritten for beginners unless this repository avoids it.
