# Go Hazard Reference

Patterns are leads, not findings. Scan live packages and confirm a reachable bad outcome.

## Hazard taxonomies

### T8. False-success mutation

- Signal: a write-like function returns `nil` without performing the mutation or after discarding an error.
- Search: `rg -n 'func .*\b(Save|Write|Update|Delete|Publish)\b|return nil'`

### T9. Incomplete variant handling

- Signal: a type switch or enum-like switch has a permissive default that treats unknown values as success.
- Search: `rg -n 'switch .*\.\(type\)|case default|default:'`

### T1. Discarded inputs

- Signal: meaningful parameters are assigned to `_` or accepted through a narrowed helper signature.
- Search: `rg -n '_ = [A-Za-z_][A-Za-z0-9_]*|func [^(]+\([^)]*_[ ,)]'`

### T2. Ignored errors

- Signal: returned errors are assigned to `_` or overwritten before inspection.
- Search: `rg -n '_, _ :=|_ = .*\([^)]*\)|[A-Za-z_]+, _ :='`

### T3. Panic across a library boundary

- Signal: reusable package code calls `panic`, `log.Fatal`, or `os.Exit` for recoverable input or I/O errors.
- Search: `rg -n 'panic\(|log\.Fatal|os\.Exit'`

### T4. Missing error propagation

- Signal: a call returning an error is followed by success without checking that error.
- Search: `rg -n 'err :=|if err != nil|return nil'`

### T5. Typed-nil interface confusion

- Signal: a pointer is stored in an interface and later compared only with `nil`.
- Search: `rg -n 'var .* interface\{|any\)|== nil|!= nil'`

### T6. Unowned goroutine

- Signal: `go` starts work without cancellation, joining, bounded lifetime, or error collection.
- Search: `rg -n '\bgo [A-Za-z_(]|errgroup\.Go|context\.Background\('`
