# QA and Testability

**Owns:** whether tests provide a reliable tripwire for the changed claim and whether the code exposes controllable, observable seams at the appropriate test level.

## Questions

- Did the change delete, skip, or loosen an existing test or assertion? Without an approved requirement change behind it, report this as Blocking.
- Which specific test fails if the changed behavior regresses, and does its assertion encode the requirement rather than “some error” or a private call sequence?
- Which changed success, boundary, and failure behaviors lack a tripwire? Match test investment to consequence, not a coverage percentage.
- Do tests observe public behavior or intentionally stable contracts rather than implementation order, private helpers, incidental strings, or mock choreography?
- Are time, randomness, network, filesystem, concurrency, and globals controlled enough for deterministic isolated execution?
- For a bug fix, would the new test fail on the pre-fix target? For a parser/serializer/state transition, would a property or fuzz test add material coverage?
- Are scale discontinuities exercised: second page/batch, more than one caller, empty state, partial completion?
- Does a failure message identify the input and expected behavior? Can a single failing test be understood without shared mutable fixture state?
- Does the chosen test level match the real coupling: unit, integration, contract, or live/manual evidence?

## Boundaries

Correctness decides whether the implementation is right today. Reliability owns the right failure policy but QA checks whether that policy is tested. Security owns attack-specific cases. Maintainability owns test names. CI infrastructure, runner health, and raw coverage targets are not this lens.

## False-positive guards

- Do not demand a unit test for integration-shaped behavior or a test for every line/branch.
- Do not treat a changed test file or increased coverage as proof; read assertions.
- Do not condemn mocks categorically; object only when they pin non-contract interactions or verify themselves.
- Real I/O is appropriate when it is the subject of the test and the harness controls it.
- Do not request every conceivable edge case. Name the regression and why its absence is risky.
- Existing ugly tests are out of scope unless this change modifies or relies on their false signal.
