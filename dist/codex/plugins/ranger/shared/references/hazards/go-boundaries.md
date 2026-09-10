# Go Boundary Hazard Reference

## T7. Intent-capture discard

- Signal: struct fields or options are accepted but omitted from JSON, database writes, HTTP requests, subprocess arguments, or downstream option structs.
- Search definitions and boundaries: `rg -n 'type .* struct|json:"|http\.NewRequest|exec\.Command|database/sql|Encode\('`
- Trace fields through constructors, copied structs, interfaces, and boundary adapters. Export status and JSON tags can change the wire contract.
- Refute when another owner consumes the field, omission is explicit for the active mode, or the field cannot affect the boundary operation.

## T10. Error downgrade

- Signal: `%v`, string conversion, boolean returns, or sentinel replacement removes wrapping, identity, or retry information.
- Search: `rg -n 'fmt\.Errorf\(|errors\.New\(|err\.Error\(\)|return (true|false), nil'`
- Confirm whether callers can still use `errors.Is`, `errors.As`, and the original context.
- Refute when a documented boundary requires a narrower shape, sensitive context must be removed, or failure is signaled through another explicit channel.
