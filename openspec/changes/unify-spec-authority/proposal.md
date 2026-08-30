# Proposal: Unify Durable Specification Authority

## Why

Careful uses OpenSpec as the durable record for Deep changes, while the generic Superpowers architectural workflow can instruct agents to create durable-looking specifications under `docs/superpowers/specs/`. Projects that use both can accumulate two competing sources of truth.

This happened in the SBX Session Evidence Collector project: its project guidance already declared OpenSpec canonical, but the generic architectural convention still produced a second specification location.

## What changes

- Define project-level specification authority in `careful.project.yaml`.
- Make Careful resolve and honor the declared authority before creating durable design or requirements artifacts.
- Treat OpenSpec as the canonical authority when configured; retain `docs/superpowers/plans/` for execution plans that link to OpenSpec.
- Prohibit parallel durable specifications in `docs/superpowers/specs/` when a project declares another authority.
- Detect and report conflicting specification locations during adoption, planning, completion, and release review.
- Add mechanical and fixture coverage for authority resolution and duplicate-spec detection.

## Non-goals

- Replace OpenSpec or impose OpenSpec on every project.
- Change the independent review requirement for Deep work.
- Delete or migrate project documents automatically without owner approval.
- Control the separately distributed Superpowers plugin; Careful provides the project-specific authority rule and adapter guidance.

## Impact

This changes the portable workflow policy, project-profile/documentation schema, Careful documentation skill, distributable plugin guidance, adoption fixtures, and contributor documentation. It does not add a runtime service or external dependency.
