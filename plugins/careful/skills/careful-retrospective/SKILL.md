---
name: careful-retrospective
description: Learn from completed work in Careful. Use after Deep changes and when blocks, overrides, failed verification, material review findings, repeated rework, or explicit user feedback reveal a possible workflow improvement. Analyze evidence and conversation signals, ask only focused follow-ups, and propose scoped improvements for user approval; never silently change a project or shared harness.
---

# Careful Retrospective

Read `references/learning-loop.md`. Run after the final handoff so reflection does not interrupt delivery.

1. Gather observed signals: user corrections, blocks/overrides, failed tests, review findings, rework, and late-discovered conventions. Treat conversation context as evidence only when supported by concrete events.
2. Distinguish **observation**, **evidence**, and **hypothesis**. Do not infer a durable rule from one preference or unusual event.
3. Produce only high-signal candidate lessons. For each, propose the smallest change, expected benefit, trade-off, confidence, and validation condition.
4. Ask focused questions only when the intended scope or cause is unclear.
5. Ask the user which candidates to apply. Allow project-only, shared-harness, mechanical-check, record-only, defer, reject, or a user-specified scope.
6. Never apply a candidate without explicit approval. A shared-harness change is substantive work and must be reviewed, tested against fixtures, versioned, and documented.
