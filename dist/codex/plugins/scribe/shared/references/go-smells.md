# Go Architecture Smells

- Parallel structs or option types represent the same domain concept at adjacent boundaries.
- JSON tags, validation, or defaults differ between producer and consumer representations.
- The same state transition is implemented in multiple packages or command handlers.
- Goroutines lack one owner for cancellation, joining, and error collection.
- Interfaces mirror concrete implementations without establishing a real ownership boundary.
- Tests hand-build wire structs or maps that can drift from production encoders.
- Architectural rules exist only in prose and have no compile, test, lint, or CI enforcement.

Use these signals to decide whether instances need a local repair, one canonical model or operation, or an architecture escalation.
