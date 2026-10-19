# Past Reviews

Load only when `past-reviews` is `auto` or `required`. This lookup shows what the owning team tends to care about. It is lower priority than the change itself, and past comments are context, not rules for this change.

1. Read reviewer comments on merged pull requests that touched the same directories. Do not use commit messages; they show what shipped, not what reviewers pushed back on.
2. Aim for 5–10 relevant pull requests from the owning team. `CODEOWNERS` can identify the team. If more than 10 qualify, use roughly the last 6–12 months.
3. Give less weight to directories with mixed or unclear ownership.
4. Skip the lookup when the pull requests are out of reach, the owning team is unclear, or the history no longer matches the current code, such as after a move or rewrite.

If past reviews are unavailable, say so and continue. In `required`, stop instead.
