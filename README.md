# Notes and Agent Workflow

This repository is a notes directory for agent-assisted development. Pi workflow skills keep requirements, research, plans, and review evidence in `work/`, separate from the repositories that receive the code change.

- [`AGENTS.md`](AGENTS.md) describes how the notes directory and its work repositories are organized.
- [`workflows/`](workflows/) is the Pi package with the lifecycle skills, subagents, and the `work-yaml` helper. Its [README](workflows/README.md) covers dependencies and the lifecycle.
- `work/` holds one nested Git repository per piece of work, and `work-archive/` holds finished ones. Both start empty.

## Install

Clone this repository, then load the package from your checkout:

```text
pi install <checkout>/workflows
```

Start Pi in the repository you want to change and run `/skill:start-work`, pointing it at `<checkout>/work/` for the new work repository.
