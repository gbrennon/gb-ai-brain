---
name: hexagonal-architecture
description: Apply hexagonal architecture (ports and adapters) principles. Keep domain core pure, inject infrastructure via ports. Write tests that verify port contracts and adapter behavior independently.
disabled: true
---

# Hexagonal Architecture

Organize code into three layers: domain (core), application (ports), and infrastructure (adapters).

## Structure

```
src/
  domain/        # Entities, value objects, domain services — zero infrastructure dependencies
  application/   # Port interfaces (inbound/outbound), use cases, DTOs
  infrastructure/ # Adapters implementing ports (DB, HTTP, message brokers)
```

## Testing by Layer

### Domain — Unit Tests
- Pure business logic. No mocks, no infrastructure.
- Test entities, value objects, domain services with unit tests (AAA).

### Application — Unit Tests
- Test use cases / application services.
- Mock or fake **outbound ports** (interfaces) to isolate the use case.
- For Rust, implement fake adapters `#[cfg(test)]` for each port.

### Infrastructure — Integration Tests
- Test each adapter against its real dependency.
- No mocks — connect to a real database, real HTTP server, etc.
- Use fixtures for deterministic input/output scenarios.
- Verify that the adapter correctly implements its port contract.

### Port Contract Tests
- Write a shared test suite that exercises a port interface.
- Run the same suite against both the mock/fake and the real adapter to verify contract conformance.
