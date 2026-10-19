# Delivery and verification strategy

**Deliver the smallest useful result quickly. Trust the codebase's current behavior, conventions, and existing automation until the change or concrete evidence gives a reason not to.** Verification exists to answer a delivery decision, not to manufacture confidence.

## Delivery

### Start from the trusted baseline

Assume unchanged code, CI, release systems, dependencies, and operational paths continue to work. Inspect enough existing code to understand the change, but do not create work to prove the baseline, compare every neighboring repository, or validate behavior the change does not affect.

Evidence can revoke trust: a current failure, changed dependency, touched shared contract, repository warning, or explicit human concern. Investigate that evidence narrowly. Uncertainty alone is not evidence.

### Keep the result MVP-sized

Include work only when it is:

1. an explicit approved outcome or constraint;
2. necessary to make that outcome function; or
3. the smallest response to a plausible failure supported by current evidence.

Use the deletion test: if removing an item still satisfies the approved outcome without an evidenced unacceptable risk, remove it. Do not add parity work, hardening, cleanup, observability, trial runs, migration aids, or “best practice” machinery because it might be useful. Optional work is omitted unless the human chooses it.

Produce a concrete human-visible result as early as dependencies allow. Prefer existing patterns and automation over new infrastructure.

### Make the plan small without making more work

MVP describes the total scope, not the size of a checkbox. Decompose approved scope into small ordered steps with one primary change and a clear done state. Split parts that can be implemented, inspected, reordered, or fail independently. Defining a helper, populating its rules and source rationale, changing conversion behavior, wiring the call site, and exercising a separate integration boundary are different steps even when they share one repository or feature.

Small steps improve steering and allow useful red-green order; they do not require separate workers, reviews, commits, or checkpoints. Execution may batch adjacent ready steps while preserving their individual status. Do not create process-only steps for assignment, waiting, automatic CI, or running an already-required check.

## Verification and review

### Decide whether to verify

Additional verification is optional. Add a check only when all are true:

- the work changes the behavior or boundary being checked
- a specific plausible failure would matter to an approved outcome
- existing automatic CI or supplied evidence does not already cover it
- the result could change the delivery decision
- the cheapest adequate check costs less than the risk it reduces

Existing automatic CI is inherited evidence, not a checklist item. Do not rerun it, reproduce it locally, or add a second check without a specific reason. Do not use trial runs, dry runs, disposable publications, live exercises, re-reading live systems to confirm a change took effect, or manual confirmation unless a named failure calls for it.

Follow the verification limit the human approved. If it is “no validation beyond existing CI,” do not add tests, trial runs, checks against live systems, or another check in their place. Record the risks that remain and stop there unless the human approves an exception.

### Add tests only for regressions that affect the goal of the work

Add a test only when it protects important changed behavior, such as realistic regressions that might come from future work and are not already tested, or changes to stable public boundaries. Tests must cost less to maintain than the value of the risk; tests that will change any time the code changes are expensive. Do not test prose, fixtures, private structure, or ordinary framework behavior. Do not write tests that merely confirm code was added.

When worthwhile tests define new behavior, they may be an earlier checklist step: author the focused contract, confirm it fails for the expected reason, then implement the behavior in a later step that makes it pass. This makes the dependency visible. Do not force test-first ordering to meet a coverage/quality metric or split out a checkbox whose only content is running tests; passing the selected suite is implicit in completing any implementation step.

“No new tests” and “no additional verification” are both complete strategies when approved. Neither needs a substitute check.

### Report touched tests

When work adds, changes, skips, or deletes tests, report those tests:

| Test | Change | Result |
|---|---|---|
| `rejects_expired_token` | new | failed as expected, then passes |

Change is new, changed, weakened, skipped, or deleted. Bold weakened, skipped, and deleted rows and give the reason.

### Spend reviews once

Default to one independent plan review. The parent applies supported findings and proceeds without another pass. A second plan review requires an explicit human request or an invalid first target, not merely a corrected draft.

Do not review every checklist item. Use no implementation review by default; reserve one focused review for any risky parts where finding and fixing a problem early is much easier than fixing it later. Use one considered reviewer for the final change, not a routine panel. Skip independent review when the human waived it or when the workflow's proportional-review rule allows a recorded skip.

Do not stack core and specialist reviews over the same risk. Don't start another reviewer for a small fix the parent can check itself. Review again only when a fix meaningfully changes how things work or the earlier review looked at the wrong version of the change.
