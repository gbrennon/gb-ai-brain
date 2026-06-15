---
name: cqrs
description: Apply CQRS pattern separating commands (writes) from queries (reads). Test commands for side effects, queries for returned data.
disabled: true
---

# CQRS — Command Query Responsibility Segregation

Separate write operations (Commands) from read operations (Queries). Commands mutate state and return void/ID. Queries return data without side effects.

## Testing Commands

- **Arrange** — set up initial state via repository fakes/fixtures.
- **Act** — execute the command handler.
- **Assert** — verify side effects:
  - Aggregate/entity state changed correctly.
  - Events were emitted.
  - Expected data was persisted.
- **One assertion per test** — test exactly one side effect per test method.
- Use mocks/fakes for outbound ports in unit tests. Use real repos + fixtures in integration tests.

## Testing Queries

- **Arrange** — seed the read model / database with fixture data.
- **Act** — execute the query handler.
- **Assert** — verify the returned data matches expectations.
- Queries must be idempotent and side-effect-free — assert only on return values.
- For integration tests, use real database with fixtures. No mocks.

## Testing Read Models / Projections

- Test that events are correctly projected into the read model.
- Arrange: publish known events through the event bus.
- Act: process the projector.
- Assert: query the read model and verify the resulting state.
