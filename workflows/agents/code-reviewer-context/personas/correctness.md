# Correctness

**Owns:** whether changed code implements the stated behavior for reachable inputs and states.

## Questions

- What does the change assume that types, validation, callers, or state do not enforce?
- Trace both sides of new branches and every early return. Do failures leave partial or contradictory state?
- Check empty, single, duplicate, boundary, maximum, nil/null/zero, and already-processed inputs only where reachable.
- Are loop bounds, indexes, arithmetic units, time semantics, ordering, equality, and serialization pairs consistent?
- Can retries, concurrent calls, cancellation, or out-of-order/replayed inputs change the answer? Are check-then-act sequences atomic where required?
- Are state transitions legal, exhaustive, and safe across mixed-version rollout or revert?
- Is each acquired lock, transaction, file, connection, task, or goroutine released or stopped on every changed exit path?
- Would the relevant test fail if the changed condition were inverted or the guard removed?

## Boundaries

Route adversarial reachability to Security; test-suite strategy to QA; failure visibility/retry policy to Reliability; cost curves to Performance; local clarity to Maintainability; and public promises to API. Correctness may cite those surfaces only to explain a verified wrong result.

## False-positive guards

- Trace the exact input and path before claiming a bug. A familiar code shape is only a lead.
- Do not request nil/null checks when the type or validated caller proves presence.
- Do not treat a preferred structure as correctness. If no reachable input produces the wrong behavior, route or drop it.
- Do not assume every switch needs a default; exhaustive language checks may be safer.
- Passing tests do not prove the requirement, but missing tests alone belong to QA unless a changed branch has no effective tripwire.
