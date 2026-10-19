# Dependencies and Existing Packages

Load when a change adds, replaces, or removes a dependency, or implements a common capability that may already have a maintained package.

This file covers external packages only. When the capability may already exist inside this repository, that belongs to [`reuse-duplication`](personas/reuse-duplication.md).

## Search before building

Check the standard library or platform and current dependencies first. Use these sources to find established candidates:

| Ecosystem | Discovery |
|---|---|
| Go | [pkg.go.dev](https://pkg.go.dev/), [Awesome Go](https://github.com/avelino/awesome-go) |
| JavaScript/TypeScript | [Best of JS](https://bestofjs.org/), [npm](https://www.npmjs.com/), [Socket](https://socket.dev/) |
| Python | [PyPI](https://pypi.org/), [Awesome Python](https://github.com/vinta/awesome-python) |
| Rust | [Blessed.rs](https://blessed.rs/crates), [crates.io](https://crates.io/), [lib.rs](https://lib.rs/) |

Prefer maintained packages that fit the project's runtime or toolchain, license, dependency, and security requirements. Keep local code when the behavior is small and simpler than owning another dependency.

A finding should name a plausible package and the edge cases or maintenance it removes. Do not request a dependency based only on popularity, and do not recommend writing custom code without checking established options.
