# Python Review Guidance

Read the applicable `pyproject.toml`, configured tools, and dependency metadata for packages imported in the diff to understand python use in this code. 

 - Follow [PEP 20: The Zen of Python](https://peps.python.org/pep-0020/) at all times.
 - Use [PEP 8](https://peps.python.org/pep-0008/) for code style and programming recommendations, while honoring its rule that project-specific conventions take precedence.
 - Use [PEP 257](https://peps.python.org/pep-0257/) when public docstrings change or the repository treats docstrings as an API contract.
 - Use the official [typing best practices](https://typing.python.org/en/latest/reference/best_practices.html) when annotations or typed public APIs change. Apply syntax recommendations when the project's minimum Python version supports them.
 - For changed asynchronous code, reference [Developing with asyncio](https://docs.python.org/3/library/asyncio-dev.html) for cancellation, blocking calls, thread boundaries, debug mode, and never-awaited coroutine guidance.
- Favor [well-known packages](https://github.com/vinta/awesome-python) for dependencies.

## Specific Guidance

 - Exceptions should be specific and descriptive, which includes extending accurate base classes. When catching and re-raising an exception, preserve the cause with `raise ... from ...`.
 - Naive and aware datetimes do not mix safely. Serialization, decimal/float choice, and timezone assumptions need evidence.
 - Give extra scrutiny to closures, iterators, and generator behavior. Check when work actually runs and who owns the iterator.
 - Native coroutines do nothing until awaited or scheduled. Check task ownership, cancellation propagation, async-generator cleanup, blocking calls on the event loop, and `ExceptionGroup` handling for task groups.

 ## Which checks are Python-specific?

 - Run the repository's configured formatter, linter, type checker, and import checks only when supplied results are missing  or stale. Use the project's settings and supported interpreter; do not invent a new tool policy.
 - When imports, descriptors, decorators, dataclasses, or framework model generation changed, verify the runtime object, not only the annotation or source spelling.
