# Review Configuration

Configuration precedence is: explicit invocation, workflow defaults, skill defaults, then unambiguous detection. Reject contradictory values rather than guessing.

## Modes and passes

- **Shallow** is the default for direct invocation, `/skill:plan-execution`, and `/skill:review-work` of localized or low-risk changes. Run one bounded core pass combining Correctness, Maintainability, and Requirements, plus QA/Testability if the target adds, changes, skips, or deletes tests, and Reuse/Duplication if it adds or rewrites code that does a recognizable job, such as detecting the cloud, parsing config, or retrying a request.
- **Deep** is for `/skill:review-work` which applies to any large change or when the change touches a shared contract, security boundary, data path, or similar risk. Start with the core, then run separate specialists only where changed surfaces or concrete risks warrant them: Security, QA/Testability, Reliability/Operability, Performance, Architecture, API/Contract, Data/Migrations, or Consumer Experience.
- Core personas cannot be excluded; QA/Testability and Reuse/Duplication are core only when their trigger applies. There is no required specialist count. The parent records why each specialist was selected.
- Explicit persona or language includes augment automatic selection. If the same value is included and excluded, stop as invalid. An exclusion suppresses only an optional specialist or automatically detected language, never relevant core guidance.

Typical routing signals:

| Changed surface or risk | Specialist |
|---|---|
| HTTP/RPC/queue/CLI entry point, trust boundary, permissions | Security |
| Risky behavior change whose tests need more than the core pass | QA/Testability |
| Network call, concurrency, job, deploy or failure-path behavior | Reliability/Operability |
| Collection loops, queries, caches, hot paths, resource growth | Performance |
| New module/package, boundary crossing, shared mechanism | Architecture |
| Public export, wire shape, CLI/config surface | API/Contract |
| Schema, migration, backfill, durable data | Data/Migrations |
| UI, public library ergonomics, human or machine-facing CLI output | Consumer Experience |

Language guidance is independent of persona selection and follows changed file types. Markdown changes load the Markdown language guidance alongside the selected core or specialist persona.

## Searches

- `prior-art` controls the search for existing code that already does what the change adds, in this repository, related repositories, and maintained packages. It accepts `off`, `auto`, or `required` and defaults to `auto`. In `auto`, Reuse/Duplication joins the core when its trigger applies and reports any related repository it could not search. In `required`, it always runs and stops if a related repository cannot be searched. `off` skips it. See [`reuse-duplication`](personas/reuse-duplication.md) and [`dependencies`](dependencies.md).
- `past-reviews` controls a lookup of past review comments to learn what the owning team tends to care about. It accepts `off`, `auto`, or `required` and defaults to `off`. When it is on, follow [`past-reviews`](past-reviews.md).

The reviewer keeps no memory between reviews. Read the repository's own guidance and the requirements the caller supplied; never create or update a saved summary.

## Worktrees

`worktree` is parent-owned and accepts `off`, `auto`, or `on`: shallow defaults to `off`; deep defaults to `auto`. Only a committed pull-request or ref-range target in a clean repository is eligible. In `auto`, the parent may prepare an isolated head checkout when scope or cross-file coupling needs full-file context; in `on`, setup or eligibility failure stops the run. Working trees with uncommitted changes, files, and snippets stay in place. Reviewers may inspect a supplied checkout and manifest but never create, clean up, or mutate one.
