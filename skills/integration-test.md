---
name: integration-test
description: Write integration tests that exercise real collaborator interactions. Use fixtures derived from real dependency calls, never mocks.
disabled: true
---

# Integration Test

Integration tests verify that multiple units or external dependencies work together correctly.

## Rules

- **No mocks** — use real instances or testcontainers for databases, message brokers, HTTP servers, etc.
- **Fixture-first approach** — call the real external dependency at least once to discover the actual shape of responses, then capture those responses as fixtures for test scenarios.
- **Fixture scope** — store fixtures as files (JSON, YAML, SQL dumps) committed to the repository so tests are repeatable offline.
- **Single external touch per scenario** — for a given test scenario, consume the external dependency once to produce the fixture, then reuse that fixture for all subsequent runs. Only re-run against the real dependency when the contract changes.
- **Test the boundary** — exercise the adapter/port boundary where your domain code meets the outside world.
- **Clean state** — ensure each test starts from a known state. Use setup/teardown or transactional rollbacks.
- **Slow tests are acceptable** — integration tests are expected to be slower. Keep them in a separate test suite from unit tests.
