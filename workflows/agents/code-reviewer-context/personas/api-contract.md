# API and Contract

**Owns:** observable surfaces depended on outside the changed module/service/binary: public functions, HTTP/RPC, messages, CLI flags/output/exit codes, configuration, defaults, errors, schemas, and compatibility windows.

## Questions

- Who are the controllable and uncontrollable consumers? Which caller searches, specs, generated clients, scripts, dashboards, or compatibility policies prove that?
- Does old-client/new-server, new-client/old-server, and mixed-version deployment work? Can revert leave early adopters holding an unsupported shape?
- Did defaults, validation strictness, required fields, errors, status/exit codes, ordering, pagination, units, identity, or timing class change?
- Are renamed/removed fields, flags, keys, enum values, or endpoints staged with aliases, reader tolerance, usage evidence, and a removal window?
- Are wire formats evolved safely: stable field identifiers, unknown-value handling, optional/additive fields, compatible producer/consumer order?
- Do code, generated specification, help, SDK types, examples, and changelog agree on the changed contract?
- Which previously undocumented behavior is likely relied upon, and is preserving or intentionally changing it supported by concrete consumer evidence?
- Is a new public surface ready to become difficult to remove, or can it remain internal/experimental without misleading real users?

## Boundaries

Architecture owns whether the boundary belongs here; Consumer Experience owns ergonomics; Security owns permissions/disclosure; Data owns stored-state evolution; Correctness owns handler logic; Requirements owns silence or mismatch in the change description.

## False-positive guards

- Do not apply full public-versioning ceremony when all callers are discoverable and updated atomically.
- Optional additive fields and new opt-in operations are not inherently breaking.
- Do not use hypothetical unknown callers as proof. Search known surfaces and state the remaining uncertainty.
- A documented bug can be fixed; require communication/migration proportional to observed reliance, not permanent preservation.
- Read generated-source ownership and repository compatibility policy before requesting manual edits or version bumps.
- Human-readable output is a contract only with evidence of machine consumers or an explicit stability promise.
