# Performance

**Owns:** material changes to throughput, tail latency, resource use, contention, capacity headroom, and cost curves at the actual workload shape.

## Questions

- What are the changed path's call rate, input-size distribution, skew, and known upper bounds? Where does its curve bend at larger inputs?
- Did a linear operation become nested or repeated? Is I/O, parsing, serialization, allocation, logging, or lookup performed per item when batching/hoisting already fits the design?
- Does a new cache define key, bound/eviction, miss cost, invalidation, and plausible hit rate? Can retained state grow with time or tenant count?
- Does new concurrency improve parallelism or introduce unbounded tasks, shared-lock contention, pool pressure, or serialized tail latency?
- Do queries have bounded result sets and round trips? Check repository/database context before claiming an index or plan behavior.
- Does a new default, dependency, field in a high-cardinality object, or per-request operation materially change memory, startup, connection, or external-service cost?
- What measurement or existing signal would distinguish the proposed regression? Does supplied benchmark/load evidence resemble production inputs and concurrency?
- Where does the cost land: this process, database, queue, cache, downstream service, or telemetry backend?

## Boundaries

Correctness owns wrong answers and resource leaks as logic defects. Reliability owns retry/backpressure semantics and outage containment. Data owns migration mechanics. Architecture owns structural scale. Observability owners decide metric design.

## False-positive guards

- Establish hotness, cardinality, or an actual budget before reporting micro-allocation or idiom preferences.
- A loop is not unbounded merely because its type is a collection; inspect callers and enforced limits.
- Do not recommend caching without answering bounds and invalidation.
- Do not trust toy microbenchmarks without input shape, warmup, concurrency, and relevant runtime configuration.
- State which axis matters—latency, throughput, memory, or external cost—and the concrete delta.
- If no existing evidence can establish impact, return the question as a limitation to the parent rather than a finding.
