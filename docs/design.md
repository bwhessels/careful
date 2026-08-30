# Careful design

## Artifact ownership

| Concern | Owner |
| --- | --- |
| User-facing intent and depth selection | Careful workflow |
| Durable requirements, deltas, designs, and history | OpenSpec |
| Execution plans and task sequencing | Project-configured execution-plan location, linked to OpenSpec |
| Execution discipline, testing, debugging, and review | Careful skills / Codex agents |
| Deterministic checks | Project tooling and CI |
| Portable policy | `core/policy.md` |
| Triggered Deep distribution checklist | `core/deep-change-checklist.md` |
| Host discovery and permissions | Adapter-specific files in `plugins/careful/` and `adapters/` |

## Default flow

```text
request → classify depth → inspect evidence → challenge if consequential
        → implement → documentation impact → independent review when triggered
        → final handoff → retrospective when high-signal
```

OpenSpec owns the current-vs-proposed boundary: main specs describe current observable behavior, while changes capture time-bound deltas, design, tasks, evidence, and history.

The portable policy owns the requirement for a clean independent pass after a material Deep finding is corrected. Adapters only route to that rule. If a clean pass is unavailable or overridden, the handoff carries that fact and the residual risk; it does not describe the review as clean. The definitions and triggered checklist remain canonical in [`core/policy.md`](../core/policy.md) and [`core/deep-change-checklist.md`](../core/deep-change-checklist.md).

## Automation policy

The default workflow is automatic. `/careful:quick`, `/careful:deep`, `/careful:review`, `/careful:retro`, `/careful:adopt`, and `/careful:override` are force or recovery controls, not a required command vocabulary.

## Self-hosting

Careful uses `careful.project.yaml` when working on itself. The profile identifies distributable adapters, fixture variants, risk boundaries, public documentation, and portable validation commands. `.careful/` is local maintainer context and is intentionally excluded from the public workflow.

## Multi-harness adapters

The policy is canonical in `core/policy.md`; adapters map it to host discovery, controls, and review mechanisms. Capability differences are explicit in `core/adapter-manifest.yaml`. An adapter is never considered behaviorally verified solely because a Markdown layout is valid: release requires a fresh host session and its corresponding fixture evidence.
