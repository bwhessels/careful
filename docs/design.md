# Careful design

## Artifact ownership

| Concern | Owner |
| --- | --- |
| User-facing intent and depth selection | Careful workflow |
| Durable requirements, deltas, designs, and history | OpenSpec |
| Execution discipline, testing, debugging, and review | Careful skills / Codex agents |
| Deterministic checks | Project tooling and CI |

## Default flow

```text
request → classify depth → inspect evidence → challenge if consequential
        → implement → documentation impact → independent review when triggered
        → final handoff → retrospective when high-signal
```

OpenSpec owns the current-vs-proposed boundary: main specs describe current observable behavior, while changes capture time-bound deltas, design, tasks, evidence, and history.

## Automation policy

The default workflow is automatic. `/careful:quick`, `/careful:deep`, `/careful:review`, `/careful:retro`, `/careful:adopt`, and `/careful:override` are force or recovery controls, not a required command vocabulary.

## Self-hosting

Careful uses `careful.project.yaml` when working on itself. The profile identifies the distributable plugin, fixture projects, risk boundaries, public documentation, and portable validation commands. `.careful/` is local maintainer context and is intentionally excluded from the public workflow.
