---
name: e2e-test
description: Write end-to-end tests that simulate the full application flow from entry point to outcome. Use fixtures, never mocks.
disabled: true
---

# E2E Test

End-to-end tests validate the entire system from the user's perspective, exercising all layers (API, domain, persistence, external integrations).

## Rules

- **No mocks anywhere** — every layer runs for real. External dependencies must be real instances (test databases, local services, sandbox APIs).
- **Simulate real usage** — drive the application through its public entry points (HTTP endpoints, CLI commands, message ingestion, UI actions). Never call internal functions directly.
- **Fixture-driven setup** — seed the system with fixture data that represents realistic scenarios. Fixtures must be deterministic and committed to the repository.
- **Fixture creation** — first exercise the real external dependency to capture fixture data, then reuse that data for repeatable tests.
- **Full flow assertion** — assert on the final observable outcome (response body, database state, emitted events, side effects). Each test should assert that the whole flow completed successfully.
- **Happy path first** — cover the primary success scenario. Add edge-case and error-flow scenarios as separate tests.
- **Isolation** — reset the system state between tests (truncate tables, restart containers, reset queues).
- **Separate suite** — keep e2e tests in their own directory and CI job. They are slow and should not block fast feedback.
