# Requirements

**Owns:** alignment between supplied intent and the actual change, including acceptance criteria, scope, and durable explanation of why the change exists.

## Questions

- Does the description, ticket, plan, or caller request accurately describe the changed behavior?
- Map each applicable acceptance criterion to concrete code, test, configuration, or documentation evidence. What is missing or silently deferred?
- Did the change add unrelated behavior, cleanup, dependency work, or product decisions? Is bundling named and justified?
- Does the implementation stop at an internal seam while the requested end-to-end outcome remains incomplete?
- Are “no behavior change,” “refactor,” compatibility, or rollout claims true when compared with actual outputs, errors, defaults, and signatures?
- Are affected audiences, intentional removals, and user-visible wording/default decisions identified with the necessary stakeholder context?
- Will future blame/history explain the motivating problem and intentional tradeoff, rather than only the mechanics?
- If the change is reverted or descoped, is the lost capability and remaining work clear?

## Boundaries

Given the stated intent, Requirements asks whether it was delivered—not whether it was the best product idea. Correctness owns code rightness; Architecture owns systemic fit; API owns compatibility; QA owns test quality; specialist lenses own runtime risks.

## False-positive guards

- Scale expected documentation to the change. A small obvious fix does not need a long narrative or ticket.
- Scope expansion is not automatically wrong when it is explicit, inseparable, and approved.
- Do not reopen the specification as a code-review finding. Escalate a real product ambiguity to the parent.
- Do not infer missing acceptance criteria from personal expectations; use supplied requirements and repository evidence.
- The review only covers the result; it doesn’t matter how the individual commits are
 organized. Don't worry about commit hygiene.
