# Authoring Reviewer Context

Reviewers: this file is authoring guidance for the context files in this directory tree. It is not review guidance. Skip it.

Every file here is loaded into a reviewer's context to buy attention it would not otherwise spend. An entry earns its place only by changing what the reviewer looks at or concludes. Anything a competent reviewer already applies unprompted, or that a formatter, linter, type checker, compiler, or CI job already reports, is noise that displaces signal.

## Layering

- `personas/` own **cross-cutting facts** — bugs that apply in all languages and all codebases, thoughts on code maintaibility, and other abstractions. 
- `languages/` own **language-specific facts** a persona needs to apply to this code, and nothing else, like language-specific best practices and package ecosystem notes. A bug that reads the same in Go, Rust, and Python belongs in a persona, however vivid the language-specific example that surfaced it.
- `configuration.md`, `dependencies.md`, `verification.md`, and `output.md` own reviewer **process**: what to load, what to prove, and what to emit. Parent workflow skills own target preparation and lifecycle evidence.
- Repository-specific facts — layer rules, banned paths, local mechanisms, named packages — belong in the target repository's own guidance, never here. This tree stays portable across codebases. A persona that needs such facts must derive them from the repository under review.

## What a language file is for

* Language best practices - structural and external advice that an LLM may or may not prioritize.
* Language tooling notes - Checks that a codebase may or may not have run that can help review quality
* Expert knowledge - calling out issues where a general reviewer of that language reading the diff carefully and unhurried would still miss it. If a LLM will catch an issue without guidance, don't call out that issue.
