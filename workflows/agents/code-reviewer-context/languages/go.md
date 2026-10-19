# Go Review Guidance

Read the applicable `go.mod` or `go.work` directive, build tags, supported platforms, and configured linters to understand how Go is being used in this code.

- Reference [Effective Go](https://go.dev/doc/effective_go) and [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments) for idioms, naming, errors, interfaces, concurrency, and common review mistakes. A consistent repository convention wins when both choices are valid.
- When exported documentation changes, use [Go Doc Comments](https://go.dev/doc/comment) for package comments, symbol comments, links, headings, and examples.
- Favor [well-known packages](https://github.com/avelino/awesome-go) for dependencies.

## Specific Guidance

- Interfaces containing typed nil pointers are non-nil. Trace interface construction before adding or removing nil checks.
- Slices share backing arrays; `append`, subslicing, and retained capacity can create aliasing or unexpectedly keep memory alive. Maps are reference-like and have deliberately unspecified iteration order.
- `defer` arguments are evaluated immediately and deferred calls run last-in, first-out. Check cleanup on every return, panic, and partial-initialization path.
- Error identity crosses wrapping boundaries through `errors.Is`/`errors.As`; string comparison and discarded `%w` chains can silently break callers.
- Every goroutine needs an owner and termination path. Check channel closure ownership, context propagation, timer/ticker cleanup, lock ordering, `WaitGroup` use, and check-then-act races against the memory model.

## Which checks are Go-specific?

- Use fresh supplied `go test`, `go vet`, and race-detector results rather than repeating them. If concurrent behavior changed and race results are missing or stale, run the narrowest relevant `go test -race` package set and state what it did not cover.
