---
name: event-handler
description: Test event handlers (consumers/subscribers). Verify correct processing of events, error handling, idempotency, and retry behavior.
disabled: true
---

# Event Handler

Event handlers consume events and produce side effects (update read models, call external APIs, emit derived events).

## Testing Event Handlers

### Unit Tests
- **Arrange** — create the event payload (use fixture data). Inject fake/mock outbound ports.
- **Act** — invoke the handler with the event.
- **Assert** — verify the handler's side effect:
  - Correct data was written to the outbound port.
  - Derived events were published.
  - Expected transformations were applied.
- **For Rust** — use fake implementations of handler dependencies.
- **Idempotency tests** — process the same event twice and verify the second run produces no additional side effects.

### Integration Tests
- Use real infrastructure (database, message broker) — no mocks.
- Publish the event to the real broker and verify downstream state changes.
- Fixtures: capture real event payloads from the broker and reuse them.

### Error Handling Tests
- **Poison message** — feed an invalid payload and verify the handler:
  - Logs the error with sufficient context.
  - Does not crash.
  - Sends the message to a dead-letter queue (DLQ) or skips gracefully.
- **Transient failure** — simulate a temporary dependency outage and verify:
  - Retry logic kicks in (exponential backoff, max retries).
  - Event is eventually processed after recovery.
  - No duplicate side effects if the handler is re-entered.

### Retry & Idempotency Tests
- **At-least-once delivery** — verify the handler deduplicates events (idempotency key, version check, upsert).
- **Ordering** — if event ordering matters, test that out-of-order events are handled correctly (rejected, re-ordered, version-gated).
