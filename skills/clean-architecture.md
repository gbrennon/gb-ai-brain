---
name: clean-architecture
description: Apply Clean Architecture dependency rule — inner layers depend on abstractions, outer layers implement them. Test each layer in isolation with appropriate test doubles.
disabled: true
---

# Clean Architecture

Follow the dependency rule: source code dependencies point inward. Nothing in an inner circle can know about something in an outer circle.

## Layers (inward to outward)

1. **Entities** — enterprise-wide business rules. Pure domain objects.
2. **Use Cases** — application-specific business rules. Orchestrate entities.
3. **Interface Adapters** — controllers, presenters, gateways. Convert data formats.
4. **Frameworks & Drivers** — DB, web, UI, external tools.

## Testing by Layer

### Entities — Unit Tests
- Pure logic, no dependencies. Straightforward AAA unit tests.

### Use Cases — Unit Tests
- Inject outbound port interfaces (gateways, presenters).
- Test each use case with mocked/faked dependencies.
- For Rust use fake impls of gateway traits.

### Interface Adapters — Integration Tests
- Controllers, serializers, gateways.
- Test with real frameworks (real HTTP client against local server, real ORM).
- No mocks. Use fixtures derived from real dependency calls.

### Frameworks & Drivers — Integration / E2E Tests
- Full system wiring tests.
- Test that the application boots, routes correctly, and persists as expected.

## Contract Tests
- Define interface contracts at each boundary.
- Run the same test suite against different implementations (test double vs real adapter) to ensure correct substitution (LSP).
