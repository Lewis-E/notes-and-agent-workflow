# Review Output

Return local review text only. Do not post, publish, edit code, or make acceptance/lifecycle decisions.

Start with a compact scope record:

```markdown
## Scope
- Target: <kind and exact range/path>
- Pin: <commit and re-check result, or not applicable>
- Pass: <label, mode, and persona>
- Evidence: <requirements, repository guidance, checks, searches, and past reviews actually used>
```

Then report findings in two sections, omitting an empty section:

```markdown
## Blocking
1. **<action-oriented title>** — `path/file.ext:line`
   - Changed behavior: <what the change now does>
   - Evidence: <quoted/paraphrased source plus verified supporting source>
   - Impact: <specific reachable consequence and affected consumer>
   - Smallest correction: <bounded fix or decision needed>

## Non-blocking
1. ...same fields...
```

Use line ranges from the reviewed target when available. For snippets, cite a stable excerpt or caller-provided label. Link or name requirements and external sources precisely enough for the parent to verify them. Do not use vague claims such as “best practice,” “could be cleaner,” or “might be slow.”

If there are no findings, write:

```markdown
## Findings
No findings. Inspected <changed behaviors and key evidence>; automated-check classes were intentionally excluded.
```

If the target moved, do not return findings. Write only:

```markdown
## Stale target
Expected <pin>; observed <identity>. Discard this pass and review the updated target.
```

If the target is conflicting, ineligible, inaccessible, or missing required evidence, return `## Target blocked` with the verified condition and needed parent action; do not return findings.

End with factual limitations only when they constrain confidence, such as unsearched related repositories, unavailable past reviews, or inaccessible requirements. Do not add strengths, praise, summaries of passing CI, publication-ready comments, fix patches, or a ready/not-ready verdict. The parent owns deduplication, disposition, and readiness.
