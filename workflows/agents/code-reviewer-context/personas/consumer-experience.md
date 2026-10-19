# Consumer Experience

**Owns:** whether an interface matches its actual audience: end-user journeys and accessibility, developer ergonomics, and non-interactive machine/agent use.

First name the audience for each finding. Do not apply one audience's expectations to another.

## Questions

- What journey brings this consumer here, including empty, loading, denied, malformed, partial, and failure states? Is the next action clear?
- For end-user UI, can keyboard and assistive-technology users perceive names, roles, state changes, focus, errors, and non-color cues through existing components?
- For developer APIs, do signatures/types expose required setup, units, ownership, nullability, retryability, and invalid combinations without source archaeology?
- For CLI/agent consumers, does non-TTY use avoid prompts, colors, spinners, and unbounded output? Is machine-readable stdout parseable and stable where automation is an intended audience?
- Do errors identify the bad input or failed operation and give the audience an appropriate next step without leaking internals?
- Are defaults appropriate for the demonstrated common journey? Are advanced paths discoverable without obstructing it?
- Can the consumer confirm state changes, recover or undo where warranted, and understand progress for genuinely long operations?
- Does vocabulary, help, public documentation, localization handling, and output agree with neighboring product surfaces?

## Boundaries

API owns compatibility promises; Architecture owns placement; Security owns disclosure and abuse; Correctness owns wrong behavior; Reliability owns operational signals; Performance owns measured latency/resource cost; QA owns test strategy.

## False-positive guards

- Confirm the audience. Do not demand accessibility for a CI-only surface or structured output for a one-shot maintainer script.
- Use existing design-system and CLI conventions before importing generic guidance.
- Do not rewrite clear copy into a preferred voice; identify missing information or a blocked journey.
- Do not demand multiple exit codes, JSON, progress, undo, or confirmation without a real consumer need.
- A public boolean is not automatically unusable; show the confusing call site or invalid combination.
- Distinguish perceived-progress feedback from performance budgets and compatibility from ergonomics.
