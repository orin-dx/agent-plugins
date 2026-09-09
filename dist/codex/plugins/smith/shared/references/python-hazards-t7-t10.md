# Python Boundary Hazard Reference

## T7. Intent-capture discard

- Signal: dataclass, model, TypedDict, or configuration fields are accepted but omitted from downstream kwargs, serialized output, subprocess arguments, storage, or network requests.
- Search definitions and boundary construction: `rg -n '@dataclass|BaseModel|TypedDict|subprocess\.|requests\.|httpx\.|json\.dump|model_dump'`
- Trace every relevant field from construction to the acting boundary. Aliases, model serializers, and `exclude_*` options can change the wire contract.

## T10. Error downgrade

- Signal: `except` replaces a typed exception with a string, `None`, boolean, or unrelated exception without preserving `__cause__`.
- Search: `rg -n 'except .*:|raise .* from None|return (None|False)|str\(.*[Ee]rror'`
- Confirm whether callers retain the error type, cause, retryability, and actionable context.
