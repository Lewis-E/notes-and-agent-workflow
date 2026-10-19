# JavaScript and TypeScript Review Guidance

Read the nearest `package.json`, the effective `tsconfig` after inheritance, the module type, and the supported runtimes to understand how JS is being used in this code.

 - Use the [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide) for practical language  patterns and built-in behavior. Defer to the repository's runtime and framework documentation for host APIs.
 - Use the [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html) for everyday type-system guidance.  For public types and declaration files, use TypeScript's [Do's and Don'ts](https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html).
 - Use the [TSConfig Reference](https://www.typescriptlang.org/tsconfig/) if compiler settings affect the reviewed behavior. Repository ESLint, formatter, and framework rules remain the code-style authority.
- Favor [well-known packages](https://github.com/bestofjs/bestofjs) for dependencies.

## Specific Guidance

 - TypeScript uses structural typing and erases types at runtime. Narrowing, excess-property checks, non-null assertions, `any`, and unchecked indexed access can make compile-time confidence stronger than runtime guarantees.
 - Promises must be returned or awaited on the intended path. Check rejection propagation, microtask ordering, cancellation/abort signals, stale async responses, and listener/timer cleanup.
 - JavaScript numbers lose integer precision above `Number.MAX_SAFE_INTEGER`; `Date` parsing input form. `BigInt` cannot mix implicitly with `number` or serialize through JSON.

 ## Which checks are JavaScript/TypeScript-specific?

 - Run the configured formatters, linters, and type-checkers if supplied results are absent or stale. Investigate configuration changes and semantic gaps.
 - Verify changed package entry points and `exports`/`imports` conditions in each supported module environment. Do not assume a bundler and Node resolve the same path.
