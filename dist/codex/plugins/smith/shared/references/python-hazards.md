# Python Hazard Reference

Patterns are leads, not findings. Scan live application modules and confirm a reachable bad outcome.

## Hazard taxonomies

### T8. False-success mutation

- Signal: a function named `save`, `write`, `update`, `delete`, or `publish` returns success without awaiting or performing the mutation.
- Search: `rg -n 'def (save|write|update|delete|publish)|async def (save|write|update|delete|publish)|return (True|None)'`

### T9. Incomplete variant handling

- Signal: `match`, type dispatch, or string-tag branching accepts a fallback that silently treats a new variant as success.
- Search: `rg -n 'match |case _|isinstance\(|\.get\([^,]+,'`

### T1. Discarded inputs

- Signal: public parameters are renamed to `_...`, immediately deleted, or never used while callers supply meaningful values.
- Search: `rg -n 'def .*\(_|del [A-Za-z_][A-Za-z0-9_]*'`

### T2. Silent fallback

- Signal: broad exception handling substitutes empty data, defaults, or success.
- Search: `rg -n 'except (Exception|BaseException)|except:|or \[\]|or \{\}|return None'`

### T3. Unchecked optional or dynamic values

- Signal: values from `dict.get`, deserialization, or dynamic attributes are dereferenced without validation.
- Search: `rg -n '\.get\([^)]*\)\.|getattr\([^,]+,[^,]+\)\.'`

### T4. Missing error propagation

- Signal: an exception is logged or converted but the caller receives success or loses the original cause.
- Search: `rg -n 'except .*:|raise [A-Za-z_][A-Za-z0-9_]*\([^)]*\)$'`

### T5. Shared mutable defaults

- Signal: a function or model field uses a mutable value as a default.
- Search: `rg -n 'def .*=(\[\]|\{\}|set\(\))|Field\(default=(\[\]|\{\})'`

### T6. Lost asynchronous work

- Signal: a coroutine or task is created without awaiting, retaining, or observing its failure.
- Search: `rg -n 'create_task\(|ensure_future\(|asyncio\.gather\('`
