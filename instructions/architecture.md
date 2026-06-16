## Architecture & Design Guidelines

- Favor composition over inheritance.
- Program to interfaces and abstractions, never to implementations.
- Keep domain logic free of infrastructure concerns (no HTTP, DB, or I/O in domain classes).
- Apply layered or hexagonal architecture: separate domain, application, and infrastructure.
- Prefer immutable data structures and pure functions where possible.
- Avoid anemic domain models — domain objects must carry behavior, not just data.
- Keep functions and methods small and focused (single level of abstraction per function).
- Use meaningful, intention-revealing names for everything.
- Avoid premature optimization — write clear code first.
- Limit function parameter count; use parameter objects when more than 3 parameters.
- Avoid deep nesting — prefer early returns and guard clauses.
- Handle errors explicitly; never silently swallow exceptions.
