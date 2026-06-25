---
name: forging-blocks-maintenance
description: Use when writing code or tests for the forging-blocks repository. Covers code conventions — imports, type annotations, docstrings, naming, async patterns, test conventions, and code patterns.
---

# ForgingBlocks Maintenance

Code style and practices for the [forging-blocks](https://github.com/forging-blocks-org/forging-blocks) project. Derived from `src/forging_blocks/`, `tests/`, and published docs.

## Project Structure

```
src/forging_blocks/
  foundation/       # Result, Ok, Err, ValueObject, Port, Messages, Errors, Specification, AutoFreeze, Meta, Debuggable, Identified, Mapper
  domain/           # Entity, AggregateRoot, AggregateVersion, ValueObject (re-export), Specification (re-export), Domain Errors
  application/      # UseCase, MessageHandler, CommandHandler/EventHandler/QueryHandler, Outbound Ports (Repository, UoW, EventStore, etc.), Application Errors
  infrastructure/   # BaseRepository, InMemory* implementations, Serialization, FileSystem, Logging, MessageBus, EventBus, EventStore, UnitOfWork
  presentation/     # Entry points (empty)

tests/
  fixtures/         # FakeEventWithName, FakeEventWithValue, SimpleFakeCommand, GitTestRepository, Scenario factories
  forging_blocks/   # Mirrors src structure (foundation/, domain/, application/, infrastructure/)
  scripts/          # Tests for scripts
  conftest.py       # git_repo, pyproject_toml, git_repo_with_remote fixtures
```

Dependency rules: Foundation → Domain → Application; Infrastructure/Presentation depend on Application; all depend on Foundation.

## Imports

Three groups: standard library → third-party → local. Blank lines between groups. Alphabetical within groups.

```python
import inspect
from abc import ABC, abstractmethod
from collections.abc import Hashable, Callable, Mapping
from typing import Any

import pytest

from forging_blocks.domain import Entity, DraftEntityIsNotHashableError
from forging_blocks.foundation import Result, Ok, Err
from forging_blocks.foundation.autofreeze import auto_freeze
```

- `from collections.abc import Callable` (not `typing.Callable`).
- `from typing import Protocol` for protocols.
- `from typing import Self` for `@classmethod` return types.
- Relative imports for sibling modules (`.result`, `.aggregate_version`).
- `__init__.py` re-exports public API with `__all__` list.

## Type Annotations

PEP 695 generic syntax everywhere. `| None` instead of `Optional`.

```python
class Result[ValueType, ErrorType](Protocol): ...
class Entity[TId: Hashable](ABC): ...
class AggregateRoot[TId: Hashable, EventPayloadType = object](Entity[TId]): ...
class UseCase[RequestType, ResponseType](InboundPort[RequestType, ResponseType], Protocol):
    async def execute(self, request: RequestType) -> ResponseType: ...

async def get_by_id(self, id: TId) -> TEntity | None:  # noqa: A002
    ...
```

- Type params: PascalCase (`ValueType`, `ErrorType`, `TId`, `TEntity`).
- `type: ignore[assignment]` for type narrowing. `type: ignore[misc]` where needed.
- `# noqa: A002` when shadowing `id`.
- All methods have return type annotations (including `-> None`).

## Docstrings

Module: short summary line. Class: explain purpose, behavior, responsibilities, non-responsibilities. Reference external influences (Evans, Vernon, Martin) when relevant.

```python
"""Base Entity class for domain blocks."""
```

Method: Google-style `Args:`, `Returns:`, `Raises:`. Double backticks for type references.

```python
def get_value_or(self, default: ValueType) -> ValueType:
    """Return the wrapped success value if Ok, otherwise return the provided default.

    Args:
        default: The value to return if this result is an error.

    Returns:
        The unwrapped success value if Ok; otherwise, `default`.
    """
```

Application ports: Responsibilities / Non-Responsibilities sections in class docstrings. Use `Notes:` for additional context.

## Naming

| Element | Convention | Examples |
|---|---|---|
| Classes | PascalCase | `Result`, `Ok`, `Err`, `ValueObject`, `AggregateRoot`, `Entity` |
| Methods/functions | snake_case | `is_ok`, `collect_events`, `get_value_or`, `is_persisted`, `execute`, `handle` |
| Private attributes | `_` prefix | `_value`, `_error`, `_id`, `_status`, `_storage` |
| Type parameters | PascalCase | `ValueType`, `ErrorType`, `TId`, `TEntity` |
| Modules | snake_case | `entity.py`, `aggregate_root.py`, `base_repository.py` |
| Test names | `test___method___when_condition_then_expected` or `test_when_condition_then_expected` | `test___init___when_id_is_none_then_creates_draft_entity`, `test_save_and_get_events` |

## Async Patterns

Application use cases, infrastructure implementations, and handlers use `async def`.

```python
async def execute(self, request: RequestType) -> ResponseType: ...
async def get_by_id(self, id: TId) -> TEntity | None:  # noqa: A002
    return self._storage.get(id)
async def handle(self, message: MessageType) -> ResultType: ...
```

## Foundation Abstractions

### Result

`Result` is a `Protocol` with `Ok` and `Err` implementations. Supports `__match_args__` for pattern matching. Operations: `is_ok`, `is_err`, `value`, `error`, `map`, `map_error`, `flat_map`, `get_value_or(default)`, `get_value_or_else(fn)`. Accessing wrong side raises `ResultAccessError`.

```python
def divide(dividend: int, divisor: int) -> Result[int, str]:
    if divisor == 0:
        return Err("Division by zero")
    return Ok(dividend // divisor)
```

### Structured Errors

`Error` base class extends both `Exception` and `Debuggable`. Building blocks: `ErrorMessage`, `ErrorMetadata`, `FieldReference`. Specialized: `ValidationError`, `ValidationFieldErrors`, `RuleViolationError`, `CombinedErrors`, `CombinedRuleViolationErrors`, `NoneNotAllowedError`, `CantModifyImmutableAttributeError`, `ResultAccessError`, `NotCallablePredicateError`.

### ValueObject

```python
class Email(ValueObject[str]):
    __slots__ = ("_value",)
    def __init__(self, value: str) -> None:
        super().__init__()
        if "@" not in value:
            raise ValueError("Invalid email")
        self._value = value.lower().strip()
    @property
    def value(self) -> str:
        return self._value
    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
```

Natural assignment in `__init__`, auto-frozen after init, selective equality via `_equality_components`. Import from `forging_blocks.foundation.value_object` or `forging_blocks.domain.value_object`.

### Auto-Freeze

`@auto_freeze` freezes instances after `__init__`. Supports `attrs=["_id"]` for selective freezing. Depth-tracking for `super().__init__()` chains. Skips abstract classes (`inspect.isabstract`). Custom `__setattr__` must check `_autofreeze__frozen`/`_autofreeze__frozen_attrs`.

```python
@auto_freeze(attrs=["_id"])
class User:
    def __init__(self, user_id: str, name: str) -> None:
        self._id = user_id
        self._name = name
```

### Messages

`Message`, `Command`, `Event`, `Query` with `MessageMetadata` (message_id, created_at, message_type, correlation_id, causation_id). Subclasses implement `_payload` and `value`.

```python
class FakeEventWithName(Event[dict[str, object]]):
    def __init__(self, name: str, metadata: MessageMetadata | None = None) -> None:
        super().__init__(metadata)
        self._name = name
    @property
    def _payload(self) -> dict[str, object]:
        return {"name": self._name}
    @property
    def value(self) -> dict[str, object]:
        return self._payload
```

Decorator messages (`@event_dataclass`, `@command_dataclass`, `@query_dataclass`, `@message_dataclass`) produce frozen dataclasses with auto-serialization.

### Port

```python
class EmailSender(Port):
    def send(self, to: str, subject: str, body: str) -> Result[None, str]: ...
```

Roles: `Port`, `InboundPort`, `OutboundPort` (generic Protocols).

### Specification

```python
class IsActive(ExpressionSpecification[Customer]):
    def __init__(self) -> None:
        super().__init__(lambda c: c.active)
```

Composable via `&`, `|`, `~`. Classes: `Specification`, `ComposableSpecification`, `ExpressionSpecification`, `AndSpecification`, `OrSpecification`, `NotSpecification`.

### Other Protocols

- `Identified` — objects with `id` property (may be None).
- `Debuggable` — structured debug info.
- `Mapper[SourceType, TargetType]` — explicit transformation.
- `Serializable` — `to_dict()`/`from_dict()` (structural, no inheritance).
- `@runtime_final`, `FinalMeta`, `FinalABCMeta` — optional runtime method finality.

## Domain Patterns

### Entity

Identity-based equality. Selective freeze on `_id`. Strict type comparison (`type(self) is not type(other)`). Draft entities (id=None) are not hashable.

```python
class User(Entity[int]):
    def __init__(self, entity_id: int | None = None, name: str = "") -> None:
        super().__init__(entity_id)
        self.name = name
```

### AggregateRoot

Consistency boundary with `AggregateVersion`. `record_event` for event recording. `apply` (abstract) + `replay` for event sourcing. `@runtime_final` on: `apply`, `replay`, `collect_events`, `discard_events`, `record_event`.

```python
class Order(AggregateRoot[str]):
    def __init__(self, order_id: str) -> None:
        super().__init__(order_id)
        self._items: list[str] = []
    def add_item(self, item: str) -> None:
        self.record_event(ItemAdded(order_id=self._id, item=item))
    def apply(self, event: Event) -> None:
        match event:
            case ItemAdded(payload={"item": item}):
                self._items.append(item)
```

### Domain Errors

`EntityIdModificationError`, `EntityIdDeletionError`, `DraftEntityIsNotHashableError`, `EntityIdNoneError`.

## Application Patterns

### Use Case

Inbound port for orchestration. Coordinates domain + outbound ports. Not responsible for business rules.

```python
class PrepareReleaseUseCase(UseCase[PrepareReleaseInput, PrepareReleaseOutput]):
    def __init__(self, version_control: VersionControl, tag_repository: TagRepository) -> None:
        self._version_control = version_control
        self._tag_repository = tag_repository
    async def execute(self, request: PrepareReleaseInput) -> PrepareReleaseOutput: ...
```

### Message Handlers

`CommandHandler[CommandType] = MessageHandler[CommandType, None]`
`EventHandler[EventType] = MessageHandler[EventType, None]`
`QueryHandler[QueryType, ResultType] = MessageHandler[QueryType, ResultType]`

### Outbound Ports

`ReadOnlyRepository`, `WriteOnlyRepository`, `Repository`, `UnitOfWork`, `MessageBus`, `CommandSender`, `EventPublisher`, `EventStore`, `QueryFetcher`, `FileSystem`, `Logger`, `Notifier`, `SpecificationRepository`.

Application errors: `ConcurrencyError`, `EventStoreError`, `EventBusError`, `UnitOfWorkError`.

## Infrastructure Patterns

### Base Repositories

```python
class BaseReadRepository[TEntity, TId](ReadOnlyRepository[TEntity, TId]):
    __slots__ = ("_storage",)
    # get_by_id, list_all, find_matching, count_matching, exists_matching

class BaseWriteRepository[TEntity: Identified[Any], TId](WriteOnlyRepository[TEntity, TId]):
    __slots__ = ()
    # save, delete_by_id, _validate_id

class BaseRepository[TEntity: Identified[Any], TId](
    BaseReadRepository[TEntity, TId], BaseWriteRepository[TEntity, TId],
):
    __slots__ = ()
```

### Event Store

`EventStore` is abstract. `InMemoryEventStore`: `save_events`, `get_events` (version range), `get_snapshot`, `save_snapshot`, concurrency via `expected_version`.

## Testing

### Test File Header

```python
# pyright: reportPrivateUsage=false, reportMissingTypeArgument=false, reportUnknownParameterType=false, reportUnknownMemberType=false, reportUnknownVariableType=false, reportUnknownArgumentType=false, reportMissingParameterType=false, reportIncompatibleMethodOverride=false, reportUnusedClass=false, reportFunctionMemberAccess=false
```

### Test Structure

- Class-based with `@pytest.mark.unit` / `@pytest.mark.integration` / `@pytest.mark.e2e` on the test class.
- Class-level `@pytest.fixture` methods for shared setup.
- Test names: `test___method___when_condition_then_expected` (triple underscores for dunders) or `test_when_condition_then_expected`.
- `pytest.raises` for expected exceptions with context assertions.
- `@pytest.mark.asyncio` for async test methods.

```python
@pytest.mark.unit
class TestUser:
    @pytest.fixture
    def persisted_user(self) -> User:
        return User(1, "Alice")

    def test_is_persisted_when_id_defined_then_returns_true(self, persisted_user: User) -> None:
        result = persisted_user.is_persisted()
        assert result is True

@pytest.mark.integration
class TestInMemoryEventStore:
    @pytest.fixture
    def event_store(self) -> InMemoryEventStore:
        return InMemoryEventStore()

    @pytest.mark.asyncio
    async def test_save_and_get_events(self, event_store: InMemoryEventStore) -> None:
        ...
```

- Test intent first: `assert result.is_ok` not `assert isinstance(result, Ok)`.
- Use fakes for Ports; don't mock what you don't own.
- `assert result.is_ok`/`assert result.is_err` for Result assertions.
- Shared fixtures: `FakeEventWithName`, `FakeEventWithValue`, `SimpleFakeCommand`, `GitTestRepository`, `Scenario`.

## Tooling Config Summary

- Ruff: line-length 100, double quotes, target Python 3.14. Select: E, W, F, I, B, C4. Ignore B008. Per-file ignores for tests: E501, B011, B009.
- Pyright: strict mode, pythonVersion 3.14.
- Coverage: minimum 90%.
- pytest markers: `unit`, `integration`, `e2e`. `asyncio_mode=auto`.
- Python 3.14+ (PEP 695 generics, `| None`).

## Code Patterns

- Abstract/Protocol bodies use `...` (Ellipsis). Concrete methods use `pass` or real code.
- `@runtime_checkable` on `Protocol` classes. `@abstractmethod` on abstract methods.
- `@runtime_final` on methods that must not be overridden.
- `__match_args__` for pattern matching (`__match_args__ = ("_value",)`).
- `__slots__` on `ValueObject` subclasses and repository base classes.
- `auto_freeze` for immutability — decorator or `auto_freeze(cls)` in `__init_subclass__`.
- `inspect.isabstract(cls)` in `__init_subclass__` to detect abstract vs concrete.
- `type(self) is not type(other)` for strict type comparison in `__eq__`.
- `object.__setattr__` to bypass frozen attribute protection in `__init__`.
- f-strings for formatting — never `%` or `.format()`.
