---
name: event
description: Apply event-driven patterns. Test that events are published with correct payloads and that event schemas are versioned.
disabled: true
---

# Event

Events represent facts that have already occurred. They are immutable, named in past tense (e.g., `OrderPlaced`, `PaymentReceived`), and carry the data needed by consumers.

## Testing Event Publishing

- **Unit level** — test that a command handler publishes the correct event.
  - Arrange: set up the aggregate/entity in a state that triggers an event.
  - Act: execute the mutating operation.
  - Assert: verify the exact event type and payload were emitted.
  - Mock the event bus / message publisher at the port boundary.

- **Integration level** — test that events are actually published to the real message infrastructure.
  - Use a real message broker (in-memory broker, testcontainer).
  - No mocks.

## Testing Event Schemas

- Event payloads must have defined schemas (protobuf, JSON Schema, Avro, etc.).
- Test that:
  - Schema changes are backward compatible.
  - Serialization/deserialization round-trips produce identical data.
  - Old consumers can still read new events (forward compatibility test).

## Fixtures

- Store sample event payloads as fixture files.
- Use these fixtures in both publisher and consumer tests to ensure contract alignment.
- For integration tests, first consume the real broker to capture actual event shapes as fixtures.
