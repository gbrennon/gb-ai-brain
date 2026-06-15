---
name: unit-test
description: Write unit tests following AAA (Arrange-Act-Assert) with a single action per test. Each test exercises exactly one behavior. Mocks allowed. For Rust, use fake impls instead of mocks.
disabled: true
---

# Unit Test

Write unit tests using the AAA (Arrange, Act, Assert) pattern. Each test must test exactly one action/behavior — a single Act step.

## Structure

```
describe("methodName") {
  it("should [expected behavior] when [condition]") {
    // Arrange — set up all preconditions, create mocks/fakes
    // Act — invoke a single method or operation
    // Assert — verify the outcome with a single logical assertion
  }
}
```

## Rules

- **One Act step per test** — never call multiple methods and assert on each.
- **One logical assertion per test** — a test should fail for exactly one reason.
- **Descriptive test names** — follow `methodName_stateUnderTest_expectedBehavior` or `should [behavior] when [condition]`.
- **Mocks are allowed** — use mocks/fakes to isolate the unit under test. Never rely on real infrastructure (DB, network, filesystem) in unit tests.
- **For Rust** — prefer `fake` impls (manual fake implementations of traits) over mocking libraries. Define fakes in a `#[cfg(test)]` module alongside the test.
- **No test interdependence** — each test must be fully isolated and runnable in any order.
- **No logic in tests** — no conditionals, loops, or try/catch in tests. Tests are declarative.
