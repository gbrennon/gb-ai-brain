## Design Patterns

Apply patterns purposefully — only when they solve a real problem. Never over-engineer.

**Creational**: Use Factory Method or Abstract Factory when creation logic is complex or
needs to vary. Use Builder for objects with many optional parameters; avoid telescoping
constructors. Use Singleton only for truly shared, stateless infrastructure (e.g., config,
logger) and never for domain objects.

**Structural**: Use Adapter to integrate incompatible interfaces without modifying existing
code. Use Decorator to add behavior without subclassing. Use Facade to simplify complex
subsystems behind a clean API. Use Composite for tree-structured, recursive object models.

**Behavioral**: Use Strategy to encapsulate interchangeable algorithms behind a common
interface. Use Observer for decoupled, reactive communication between components. Use
Command to encapsulate operations as objects (undo, queuing, auditing). Use Chain of
Responsibility for pipelines or middleware. Use Mediator to reduce direct coupling between
collaborators. Use Template Method for invariant algorithm skeletons with overridable steps.
