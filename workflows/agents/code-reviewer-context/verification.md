# Finding Verification and Deduplication

Run this gate on each candidate before reporting it.

## Evidence gate

A finding survives only when all are true:

1. **Changed behavior:** identify the changed line or changed behavior that introduces or exposes the problem. Unchanged code may prove impact but is not a standalone target.
2. **Concrete evidence:** cite exact file and line/range when available, plus the relevant code, requirement, configuration, caller, or external contract. Read configuration before claiming tool, dependency, version, or environment behavior.
3. **Reachable impact:** trace a plausible input/state/path to an observable wrong result, contract break, operational failure, or material future-reader cost. Replace “might” with the verified condition; otherwise drop it.
4. **Small correction:** suggest the narrowest correction consistent with existing patterns, approved scope, and verification limits. Do not prescribe a rewrite, test, or hardening work when a smaller product change resolves the concrete issue.
5. **Automation filter:** do not restate formatter, linter, compiler, type-checker, or supplied CI findings. Scanner output is a lead, not proof.

Do not demand guards for states excluded by types or validated callers. Do not infer hot paths, attacker control, public consumers, table size, framework behavior, or language-version semantics without evidence. Do not flag generated output when its source must change instead.

## Classification

- **Blocking:** concrete changed behavior can produce a wrong or unsafe result, violate an approved requirement or compatibility promise, or needs an unresolved product/architecture decision before acceptance.
- **Non-blocking:** a confirmed, significant remaining risk in the changed behavior that the human should see before acceptance. It is not a request for optional improvement and adds no work unless the human chooses it.

Missing extra verification is not a finding when the approved plan intentionally leaves it out. Do not turn inability to prove unchanged behavior into a blocker.

Do not create finer severity buckets. Order by expected impact and actionability, not by persona.

## Dedupe within a pass

Merge candidates with the same root cause and smallest correction. One finding may cite multiple affected locations. If two lenses see the same line, keep the framing that best explains the actual impact; mention a second consequence only when it changes the correction or classification. Do not multiply a systemic concern into one comment per occurrence.

Cross-pass deduplication and final disposition belong to the parent. Return enough evidence for that synthesis; do not claim another pass is wrong or issue a lifecycle verdict.
