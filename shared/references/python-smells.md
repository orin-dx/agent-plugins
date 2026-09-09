# Python Architecture Smells

- Parallel dictionary, dataclass, TypedDict, or model shapes represent the same domain concept.
- Serialization aliases or validation rules differ across producer and consumer models.
- The same state transition is implemented in multiple services or command handlers.
- Async work has no owner responsible for awaiting, cancellation, and error collection.
- Filesystem, environment, or process state is read throughout the domain layer instead of at one boundary.
- Tests construct hand-written dictionaries that can drift from the production serializer.
- Architectural rules exist only in prose and have no type, test, lint, or CI enforcement.

Use these signals to decide whether instances need a local repair, one canonical model or operation, or an architecture escalation.
