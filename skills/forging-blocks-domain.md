---
name: forging-blocks-domain
description: Write code using ForgingBlocks Domain block — Entity, AggregateRoot, ValueObject, and domain errors. Use when modeling problem-space concepts, rules, and constraints independent of frameworks and infrastructure.
disabled: true
---

# Domain Block

The Domain block represents the problem space. It contains concepts, rules, and constraints that give meaning to your software — independent of databases, frameworks, or delivery mechanisms. Depends only on Foundation.

## Entity — Defined by Identity

Entities are objects whose identity matters over time, not their attributes.

```python
from forging_blocks.domain import Entity

class Task(Entity[int]):
    def __init__(self, task_id: int | None = None) -> None:
        super().__init__(task_id)
        self._title = ""
        self._completed = False

    @property
    def title(self) -> str:
        return self._title

    def complete(self) -> None:
        self._completed = True
```

- Equality is by **type + `_id`**, not attributes — `Task(1) == Task(1)` even if other fields differ.
- `_id` is selectively frozen after `__init__` — modifying it raises `EntityIdModificationError`, deleting it raises `EntityIdDeletionError`.
- Draft entities (`_id = None`) compare by reference and are not hashable (`DraftEntityIsNotHashableError`).
- `is_persisted()` returns `True` when `_id is not None`.
- Use `@auto_freeze(attrs=["_id"])` for selective freezing on custom entities.

## ValueObject — Immutable by Value

Use Foundation's `ValueObject` for immutable concepts without independent identity.

```python
from collections.abc import Hashable

from forging_blocks.foundation import ValueObject


class TaskTitle(ValueObject[str]):
    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        super().__init__()
        if not value.strip():
            raise ValueError("Title must not be empty")
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @property
    def _equality_components(self) -> tuple[Hashable, ...]:
        return (self._value,)
```

Two value objects with the same `_equality_components` are equal and have the same hash. They are immutable — post-init mutation raises `CantModifyImmutableAttributeError`.

## AggregateRoot — Consistency Boundary with Events

Aggregate roots define a consistency boundary and record domain events.

```python
from forging_blocks.domain import AggregateRoot, AggregateVersion
from forging_blocks.foundation import Event

class TaskCompleted(Event[dict]):
    pass

class Task(AggregateRoot[int]):
    def __init__(self, task_id: int, version: AggregateVersion | None = None) -> None:
        super().__init__(task_id, version or AggregateVersion(0))
        self._status = "active"

    def complete(self) -> None:
        event = TaskCompleted(payload={"task_id": self.id})
        self.apply(event)

    def _handle(self, event: Event[dict]) -> None:
        if isinstance(event, TaskCompleted):
            self._status = "completed"
```

- Identity must be non-None, non-empty, non-False (raises `EntityIdNoneError`).
- `apply(event)` calls `_handle()`, increments `version`, and queues the event for later collection.
- `replay(event)` calls `_handle()` and increments `version` but does NOT queue — used for event store reconstitution.
- `collect_events()` drains and returns queued events (called by Unit of Work after persistence).
- `discard_events()` clears the queue on rollback.
- `record_event(event)` queues an event without calling `_handle()` (for integration events).

## Domain Errors

Use `RuleViolationError` or `ValidationError` for invalid domain states.

```python
from forging_blocks.foundation import RuleViolationError, ErrorMessage

raise RuleViolationError(ErrorMessage("Task cannot be completed: already done"))
```

Domain errors express meaning in domain terms — not transport, persistence, or framework concerns.
