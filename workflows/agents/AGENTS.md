# Packaged Agents

This directory contains the agent definitions exported by the `notes-workflows` Pi package. Pi Subagents supplies the runtime that discovers and executes them.

## Package discovery

- Keep `pi.subagents.agents` in `../package.json` pointed at the `./agents` directory. Pi Subagents recursively scans declared directories; individual Markdown file entries are not discovered.
- A package agent with the same runtime name as a Pi Subagents builtin takes precedence over that builtin. User and project agents remain higher priority than package agents.
- Do not edit installed definitions under `~/.pi/agent/npm/node_modules/pi-subagents/`. Durable customizations belong here.

## Researcher maintenance

`researcher.md` is a maintained fork of the Pi Subagents builtin researcher. It retains the upstream web-research behavior and adds bounded stratified sampling, diverse CI cohort coverage, and script-first processing for large datasets.

When Pi Subagents changes its builtin researcher:

1. Compare the new builtin with `researcher.md`.
2. Incorporate useful upstream behavior without weakening the local sampling and programmatic-processing rules.
3. Keep the runtime name `researcher` so the package definition continues to shadow the builtin.
4. Restart Pi and inspect `researcher` in `/subagents`. Confirm the source is `notes-workflows`, the path ends with `workflows/agents/researcher.md`, the script-processing tools are present, and the prompt contains the large-dataset guidance.

If this package stops exporting `researcher`, the unchanged Pi Subagents builtin becomes active again. Runtime resolution is the relevant verification; do not add tests that merely assert authored prompt wording or headings.
