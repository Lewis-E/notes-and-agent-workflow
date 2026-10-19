# Research Lane Files

`/skill:context-and-requirements` owns research planning, progress, and findings. `/skill:maintain-work-context` checkpoints these files without interpreting them.

Create `research/README.md` from this index shape:

```markdown
# Research

Based on the confirmed `human-context` checkpoint.

- [ ] [<lane-id>](<lane-id>.md) — <question this lane must answer>
```

Create one `research/<lane-id>.md` per question:

```markdown
# <Question>

## Findings

<Verified facts and clearly labeled inferences.>

## Sources

<Files, tickets, documents, or URLs.>

## Access Problems

None.
```

Do not put commit hashes in research files; `agent-journal.md` records checkpoint commits.

Check an index item only after its findings and sources answer the question. If a lane is blocked or replaced, explain why in its file and keep the index accurate.
