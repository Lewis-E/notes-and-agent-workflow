# Data and Migrations

**Owns:** durable state evolution: schema and migration safety, mixed-version coexistence, backfills, integrity, irreversibility, replay, retention/deletion mechanics, and recovery from partial completion.

## Questions

- Which operation becomes irreversible after execution? Is there an additive/dual/contract sequence or verified recovery path before destructive removal?
- During rollout and revert, can old and new code both read and write the schema safely? Is rollout ordering explicit?
- For this exact database engine/version and table size, what locks, rewrites, scans, replica lag, or transaction duration does the DDL cause?
- Is a backfill bounded, batched, throttled, idempotent, resumable, and safe in mixed state? What prevents new writes from drifting during it?
- Are constraints and derived values enforced by the database/transaction or reconciled with an observable invariant?
- Are identifiers, enum values, field numbers, and stored event shapes readable by all live consumers and historical replay jobs?
- Can deletion/retention mechanisms locate new sensitive data through stable owner/tenant keys? Legal retention duration is external input, not this reviewer's decision.
- What verification proves row counts, checksums, invariants, or samples before/after a high-blast-radius transformation?

## Boundaries

API owns producer/consumer wire compatibility; Reliability owns job execution and operational controls; Performance owns steady-state query plans; Security owns access/encryption; Architecture owns whether the service should own the data; legal/compliance owns policy values.

## False-positive guards

- Confirm engine, version, table cardinality, traffic, and migration framework before asserting lock behavior.
- Do not demand zero downtime for a tiny/offline table with an approved maintenance window.
- Read prior migration phases/history before flagging a destructive statement that may complete an approved contract phase.
- Ask for a recovery path, not automatically a reverse migration; reversing a destructive transform may be less safe.
- A new empty unreferenced table is cheaply reversible; do not invent ceremony.
- `IF EXISTS`/`IF NOT EXISTS`, concurrent indexes, and dual writes are context-dependent, not universal rules.
