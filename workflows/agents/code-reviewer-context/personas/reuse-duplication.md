# Reuse and Duplication

**Owns:** whether changed code re-implements behavior this repository or a related repository already provides, and whether an existing equivalent should be used instead. Divergence is the tell: two copies that have already drifted in fields, nullability, units, or rules let two code paths disagree at runtime.

## Search protocol

A missed duplicate is a search failure, not a reading failure. Reading the diff cannot satisfy this lens.

1. Select candidates worth searching: new or rewritten code that does a recognizable job, whether exported or private, such as functions, types, constants, enums, hooks, validators, converters, wire and response models, policies, and test helpers. Skip trivial locals and single-call-site glue. Consider what jobs are more or less relevant to the codebase as a whole.
2. Derive search roots from evidence rather than assumption: shared, util, and common packages declared in the manifest or workspace config; directories the changed file already imports from; locations named in repository guidance; and related repositories. Find related repositories in repository guidance, including any repository-context skill it names. Search their local checkouts read-only and name any that are missing.
3. Search behavior, not just names: the export name, plausible synonyms for the same operation, and two or three distinctive implementation terms such as a magic constant, regex, error string, or field name.
4. Read every match before reporting it. A name match is a lead; equivalent behavior on the same inputs is the claim.
5. Confirm the changed file may legally import the candidate given layer direction, module visibility, build target, and license. For a match in another repository, state whether it is importable as a package or is a copy that must stay in step.

## Questions

- Does an existing export already produce this result for the same inputs, including the edge cases the new code handles?
- Does this add a second definition of a wire shape, response model, enum, or domain constant that must now be kept in step with the first?
- Is this a local copy of policy — validation rules, permission logic, retry rules, formatting, unit conversion — that already lives somewhere authoritative?
- Have the two copies already diverged, and can a caller observe the difference?
- Was the existing equivalent rejected for a stated reason, or simply never found?

## Boundaries

Dependencies owns external packages and standard-library equivalents. Architecture owns whether a mechanism is placed and owned correctly, and whether a legal import path exists at all. Maintainability owns duplication created inside this change and whether to extract it. This lens owns concrete equivalents that already existed before the change.

## False-positive guards

- Do not flag an intentional thin wrapper that adds a name, type, default, or boundary mapping.
- Do not flag a near-match. When nullability, units, timezone, error behavior, or edge cases differ, either state the exact reason they are equivalent anyway, or drop it.
- Do not flag a match in a related repository unless it is published for reuse or the two copies must agree, for example because both report the same value to the same backend.
- Do not flag an equivalent the changed file cannot legally import. Route that dependency-direction question to Architecture.
- Do not propose extracting a shared abstraction that does not exist yet.
- Do not flag generated output, vendored copies, or a deliberate fork with a recorded reason.
- Do not report one finding per call site. Report one finding citing every affected location.
- Absence of matches is not proof of absence. State what was searched instead of claiming the repository has no equivalent.
