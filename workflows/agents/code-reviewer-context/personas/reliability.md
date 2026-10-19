# Reliability and Operability

**Owns:** changed behavior under partial failure, retry, concurrency, deploy/restart, overload, and whether operators can detect, localize, stop, and recover from it.

## Questions

- For each new process boundary, what happens on timeout, cancellation, malformed/partial response, lost acknowledgement, or dependency outage? Does it honor the caller's deadline?
- Are retries bounded, budgeted, and limited to retryable idempotent operations? Could they amplify an outage or duplicate an effect?
- Can queues, tasks, caches, workers, connections, or logs grow without a bound? What backpressure or rejection behavior applies?
- What happens on cold start, graceful shutdown, restart mid-flight, overlapping jobs, and mixed-version deploy?
- Is failure contained per request, tenant, shard, or dependency, or can it cascade through shared pools/state?
- Does a changed error/log/metric preserve actionable identifiers and underlying cause without unbounded volume or sensitive data?
- Which user-visible signal detects silent failure? Does an existing alert/runbook/kill switch actually cover the new path?
- Are failure paths specifically exercised: timeout, cancellation, partial write, poison/duplicate/out-of-order message, and off-path rollback?

## Boundaries

Correctness owns the happy-path answer and pure races; Performance owns cost curves; Data owns migration integrity; Architecture owns whether the boundary should exist; QA owns general test strategy; Security owns attacker-triggered failures.

## False-positive guards

- Do not demand retries, circuit breakers, dashboards, alerts, feature flags, or runbooks by default. Tie each to a new evidenced failure mode and existing operational practice.
- Read upstream clients and propagated contexts before claiming a missing timeout.
- Do not retrofit observability debt into a behavior-preserving refactor.
- Calibrate failure scenarios to actual deployment topology; do not invent network partitions within a process.
- Alert on user-visible symptoms when existing practice does; avoid requesting cause-level noise.
- Values such as timeout and retry count are findings only when a contract, budget, or concrete interaction proves them wrong.
