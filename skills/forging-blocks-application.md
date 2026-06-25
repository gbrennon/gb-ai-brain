---
name: forging-blocks-application
description: Write code using ForgingBlocks Application block — UseCase, MessageHandler, inbound/outbound Ports, Repository, UnitOfWork. Use when defining system behavior, coordinating domain logic, and setting boundaries that Infrastructure implements.
disabled: true
---

# Application Block

The Application block defines what the system does. It coordinates domain logic, handles incoming requests, and invokes outbound capabilities through ports. It does not contain business rules or infrastructure details. Depends on Domain and Foundation.

## UseCase — Single Business Operation

Define a use case as an inbound port that accepts input and returns output.

```python
from forging_blocks.application import UseCase, Repository, UnitOfWork
from forging_blocks.foundation import Result, Ok, Err

class RegisterUser(UseCase[dict, Result[str, str]]):
    def __init__(self, repo: Repository[User, str], uow: UnitOfWork) -> None:
        self._repo = repo
        self._uow = uow

    def execute(self, input_data: dict) -> Result[str, str]:
        user = User(user_id=input_data["id"])
        self._repo.add(user)
        self._uow.commit()
        return Ok(user.id)
```

Inject dependencies via constructor — the use case depends on outbound port protocols, not concrete implementations.

## MessageHandler — Command, Event, Query

React to individual messages using specialized handlers.

```python
from forging_blocks.application import CommandHandler, EventHandler, QueryHandler
from forging_blocks.foundation import Command, Event, Query, Result

class PlaceOrderHandler(CommandHandler[PlaceOrder]):
    def handle(self, command: PlaceOrder) -> None:
        # Validate, invoke domain, persist
        pass

class OrderPlacedHandler(EventHandler[OrderPlaced]):
    def handle(self, event: OrderPlaced) -> None:
        # React to fact (send email, update read model)
        pass

class GetOrderHandler(QueryHandler[GetOrder, OrderDTO]):
    def handle(self, query: GetOrder) -> Result[OrderDTO, str]:
        # Query without side effects
        pass
```

`CommandHandler[Cmd]` handles commands (intent). `EventHandler[Evt]` handles events (facts). `QueryHandler[Qry, R]` handles queries and returns results.

## Outbound Ports — What the Application Needs

Define ports for persistence, messaging, and infrastructure.

```python
from forging_blocks.application import Repository, UnitOfWork
from forging_blocks.application import CommandSender, EventPublisher, MessageBus

# Repository — persist and retrieve domain objects
class TaskRepository(Repository[Task, str]):
    pass  # add(), get(id), remove(), list()

# Unit of Work — transaction boundary
class TaskUnitOfWork(UnitOfWork):
    pass  # commit(), rollback(), flush(), is_active

# Message Bus — dispatch messages
class TaskMessageBus(MessageBus):
    pass  # dispatch(message)
```

Outbound ports are **Protocols** that Infrastructure implements. Application defines the contract; Infrastructure provides the mechanism.

## Wiring It Together

```python
class CreateTask(UseCase[dict, Result[str, str]]):
    def __init__(
        self,
        repo: Repository[Task, str],
        uow: UnitOfWork,
        bus: MessageBus,
    ) -> None:
        self._repo = repo
        self._uow = uow
        self._bus = bus

    def execute(self, input_data: dict) -> Result[str, str]:
        task = Task(task_id=input_data["id"])
        self._repo.add(task)
        self._uow.commit()
        self._bus.dispatch(TaskCreated(payload={"id": task.id}))
        return Ok(task.id)
```

The application layer orchestrates — it does not enforce invariants (that's Domain) and does not talk to databases directly (that's Infrastructure implementing the port).
