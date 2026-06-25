---
name: forging-blocks-foundation
description: Write code using ForgingBlocks Foundation block — Result, ValueObject, Port, Mapper, Specifications, Messages, and structured Errors. Use when defining shared abstractions and contracts that all other blocks depend on.
disabled: true
---

# Foundation Block

The Foundation block provides low-level, reusable abstractions shared across the system. It depends on nothing. All other blocks may depend on Foundation. It contains no domain logic, no application orchestration, and no infrastructure concerns.

## Result — Explicit Outcomes

Model success and failure as return types instead of exceptions.

```python
from forging_blocks.foundation import Result, Ok, Err

def parse_int(value: str) -> Result[int, str]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err(f"invalid integer: {value!r}")
```

Use `.map()`, `.flat_map()`, `.map_error()` to compose. Use `.get_value_or(default)` or `.get_value_or_else(fn)` for fallbacks. Match on `Ok(value)` / `Err(error)` for branching.

## ValueObject — Immutable by Value

Wrap primitives to make domain rules visible and reusable.

```python
from collections.abc import Hashable

from forging_blocks.foundation import ValueObject


class Email(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
```

Always call `super().__init__()`. Implement `value` and `_equality_components` — both must have return type annotations. Use `__slots__`. Autofreeze makes it immutable after init.

## Port — Boundary Contracts

Define interfaces as `Port` protocols to decouple blocks.

```python
from forging_blocks.foundation import Port, InboundPort, OutboundPort

class EmailSender(Port):
    def send(self, to: str, subject: str, body: str) -> Result[None, str]: ...
```

Use `InboundPort` / `OutboundPort` to signal direction — what the app offers vs what it needs.

## Mapper — Type Transformation

```python
from forging_blocks.foundation import Mapper

class UserDTOMapper(Mapper[User, UserDTO]):
    def map(self, source: User) -> UserDTO:
        return UserDTO(id=source.id, name=source.name)
```

## Messages — Command, Event, Query

```python
from forging_blocks.foundation import Command, Event, Query

class PlaceOrder(Command[dict]):
    """Intent to perform an action."""

class OrderPlaced(Event[dict]):
    """Fact that has already occurred."""

class GetOrder(Query[dict]):
    """Intent to retrieve information (side-effect free)."""
```

Messages are immutable, architecture-neutral, carry payloads and metadata (message_id, created_at, correlation_id).

## Specification — Composable Rules

```python
from forging_blocks.foundation import Specification, AndSpecification

class IsAdult(Specification[dict]):
    def is_satisfied_by(self, candidate: dict) -> bool:
        return candidate.get("age", 0) >= 18
```

Compose with `AndSpecification`, `OrSpecification`, `NotSpecification`.

## Errors — Structured Error Model

```python
from forging_blocks.foundation import (
    ValidationError, RuleViolationError,
    CombinedErrors, ErrorMessage,
)

# Validation error for input rules
raise ValidationError(ErrorMessage("email must contain '@'"))

# Rule violation for business invariants
raise RuleViolationError(ErrorMessage("order cannot be cancelled after shipment"))

# Aggregate multiple errors
errors = CombinedErrors([
    ValidationError(ErrorMessage("invalid email")),
    RuleViolationError(ErrorMessage("insufficient funds")),
])
```

Use `ValidationError` for input validation, `RuleViolationError` for business rules, `CombinedErrors` to aggregate multiple errors.
