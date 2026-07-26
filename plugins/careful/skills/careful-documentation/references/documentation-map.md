# Documentation map

Route each fact to one canonical home. Link instead of copying.

| Document | Canonical purpose |
| --- | --- |
| README | orientation, basic run path, and links |
| Specs | current observable behavior |
| Changes | proposed/in-progress delta and history |
| Architecture | current system boundaries and structure |
| ADRs | why a consequential decision was made |
| Development docs | contributor commands and operating procedures |
| Reference | generated or canonical technical contract |

## Impact routing

- Observable behavior changes: update specs.
- Public API or configuration changes: update reference and migration guidance.
- Boundary/dependency/deployment changes: update architecture; add ADR when consequential.
- Contributor or operator workflow changes: update development docs/runbooks.
- Orientation changes: update README only when the starting path changed.

For a Deep change, record either the affected documents or an evidence-based no-impact decision. Check links and project documentation tooling before completion.
