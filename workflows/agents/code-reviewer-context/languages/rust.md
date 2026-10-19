# Rust Review Guidance

Read the applicable `Cargo.toml`, lint table, profile settings, minimum supported Rust version, target matrix, and `unsafe` policy to understand the use of rust in the code. 

- Use the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) for naming, conversions, common traits, documentation, predictability, and future-proof public APIs.
- Use the [Rust Style Guide](https://doc.rust-lang.org/style-guide/) and the project's rustfmt configuration for formatting conventions. Use [Clippy's documentation](https://doc.rust-lang.org/stable/clippy/) to understand configured lints rather than enabling stricter lint groups by default.
- When public documentation changes, use rustdoc's [How to write documentation](https://doc.rust-lang.org/rustdoc/how-to-write-documentation.html) for examples, links, panic/error sections,
and safety notes.
- When `unsafe` code changes, use the [Rustonomicon](https://doc.rust-lang.org/nomicon/) for established unsafe-code guidance, but still require the local invariants to be stated and proved.
- Favor [well-known crates](https://blessed.rs/crates) for dependencies.

## Specific Guidance

- Ownership errors can hide behind unnecessary `clone`, `Arc`, leaked allocations, or overly broad lifetimes even when the borrow checker accepts the result. Check who owns data and when `Drop` runs. Think about how the data should be owned based on the intent of the code. Similarly, destructors, guards, and resources can live longer or shorter than a reader expects. Good rust code should have clear and comprehensible lifetimes and ownership. Cleanup that must happen needs an explicit fallible `close` or `shutdown` on every path.
- Holding a lock or borrow guard across `.await` can create contention, deadlock, or non-`Send` futures. Spawned tasks need clear join, cancellation, and shutdown ownership. `Send` and `Sync` assumptions deserve explicit evidence at boundaries. 
- Rust `String`s and `Integer `casts and byte behavior can be tricky and deserves close examination. Look out for where we might want `OsStr` for operating system specific behavior and remember Comparison on `Path` is byte comparison and resolves nothing, including `..`, links, and case. Remember that integer casts may truncate or wrap, indexing can panic, and string indexes are byte offsets constrained by UTF-8 boundaries.
- `.await` is a cancellation point. A dropped future stops at its last suspension without unwinding, so `select!`, timeouts, and dropped `JoinHandle`s abandon partially applied work. Multi-step writes and buffered reads need cancel-safe framing or an owning task.
- Blocking calls compile fine in async code. `std::sync::Mutex`, `std::fs`, `Command::status`, and `thread::sleep` inside an async function stall a runtime worker, and the symptom appears as latency somewhere unrelated. The async equivalent or `spawn_blocking` is the fix. Always consider if async/synch mixed code makes sense.
- Think about the intent of the code when you think about `unwrap`, `expect`, and `panic`. Consider where an error should show and who will see it. Consider when process termination is appropriate.
- Remember that `cargo` can change available features in a build. A green workspace build does not represent the feature and target combinations all downstream crates compile, so `cfg`, optional-dependency, and build-script changes need the affected combinations built.

## Which checks are Rust-specific?

- Use fresh configured `cargo fmt --check`, `cargo check`, and Clippy results instead of repeating them. Match the repository's feature, target, workspace, and minimum-version policy.
- If we don't have fresh results, it's ok to run checks.
- rustfmt, Clippy, rustdoc, the compiler, and generated bindings own mechanical findings.
