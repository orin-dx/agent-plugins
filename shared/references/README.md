# Shared Reference Map

References are organized by the decision they support. Start with the current cognitive concern, then select a language file only when the evidence is language-specific.

| Directory | Use for |
| :--- | :--- |
| `hazards/` | Candidate defect signals, boundary hazards, confirmation, and refutation |
| `architecture/` | Semantic models, structural causes, boundary value design, and remediation |
| `verification/` | Evidence selection, language-native checks, implementation review, and interface coverage |
| `delivery/` | Changesets, commits, pull requests, and review operations |
| `authoring/` | Reader-focused prose, comments, and diagrams |
| `evaluation/` | Behavioral comparison with controlled fixtures and hidden oracles |
| `workspace/` | Persisted artifact locations and workspace conventions |
| `tooling/` | Cross-cutting tool preferences for repository work |

Runtime instructions cite the exact file they need. This map is for maintainers; agents should not load it before following a direct reference.
