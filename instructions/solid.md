## Core Philosophy — SOLID by Default

Apply SOLID principles in every suggestion without being asked:

- **S — Single Responsibility**: Each class, module, or function has one reason to change.
  Split concerns aggressively; never mix domain logic with infrastructure concerns.
- **O — Open/Closed**: Favor extension over modification. Prefer abstractions, interfaces,
  and composition over conditional branching on type or instanceof checks.
- **L — Liskov Substitution**: Subtypes must be substitutable for their base types without
  altering correctness. Never override in ways that weaken preconditions or strengthen
  postconditions.
- **I — Interface Segregation**: Prefer narrow, role-specific interfaces over fat ones.
  Clients must not depend on methods they don't use.
- **D — Dependency Inversion**: Depend on abstractions, not concretions. Always inject
  dependencies; never instantiate collaborators inside business logic with `new`.
