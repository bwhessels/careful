---
name: careful-documentation
description: Keep project documentation aligned with implemented work in Careful. Use automatically during completion of behavior, API, architecture, configuration, operational, or developer-workflow changes; also use for explicit documentation audits or repairs. Route facts to one canonical document, update only affected sources of truth, and report evidence for no-impact decisions.
---

# Careful Documentation

Read `references/documentation-map.md`. Treat documentation as a routing and verification problem, not a request to write more Markdown.

1. Read the project documentation map when present. For an unknown project, use `careful-adopt` before creating a structure.
2. Resolve `documentation.spec_authority` before creating or updating a durable specification. Use OpenSpec when declared; keep execution plans separate and linked.
3. Assess whether the change affects behavior/specification, public contract/reference, architecture, a consequential decision, contributor workflow, operations, or orientation.
4. Update the canonical source once and link from other documents instead of restating facts.
5. For no-impact conclusions, state the relevant evidence in the final handoff.
6. Verify links, generated/reference outputs, and project documentation checks where available.
7. For Deep work, record the documentation impact assessment in the change evidence. Report competing durable-looking specifications without destructive migration.
