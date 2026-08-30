# Careful portable workflow contract

Version: 1

This is the canonical, host-neutral policy for every supported Careful adapter. Adapters supply discovery, commands, permissions, and review mechanics; they do not redefine this policy.

## Baseline

For substantive product, coding, debugging, and architecture work, select one depth before implementation:

- **Quick** — reversible, narrow work with clear evidence.
- **Standard** — ordinary implementation or investigation; verify material claims and assess documentation impact.
- **Deep** — risky, architectural, product, public-contract, data, security, privacy, reliability, or hard-to-reverse work; use a durable OpenSpec change when available, challenge the decision, and obtain independent review.

For consequential claims, use only these labels: **Verified**, **Inferred**, **Assumption**, and **Unknown**. Research time-sensitive or consequential external claims and do not overstate sources.

## Specification authority

Before creating a durable proposal, design, requirements document, or change record, resolve the project’s specification authority from `careful.project.yaml` or an explicit adoption decision.

- When `documentation.spec_authority: openspec` is declared, OpenSpec owns durable specifications and change history.
- When `documentation.spec_authority: project-defined` is declared, use the project’s named authority and preserve its conventions.
- When `documentation.spec_authority: none` is declared, record that explicit decision and apply ordinary documentation-impact controls without requiring a durable specification system.
- When no authority is declared, report it as **Unknown** during adoption when the distinction materially affects the workflow.

Execution plans are separate from durable specifications. A configured execution-plan location such as `docs/superpowers/plans/` may contain implementation steps, but plans must link to the canonical specification and must not become a second source of requirements or decisions.

When an authority is declared, report durable-looking specifications found in competing locations such as `docs/superpowers/specs/`. Do not delete, overwrite, archive, merge, or silently migrate them without explicit owner direction. Documents explicitly marked as historical or pointers to the canonical specification are non-authoritative context.

## Public-readiness contract

When a project configures `public_readiness`, resolve its audience mode, required documents, canonical public documents, checks, and publication/release gates from that project-owned configuration. Supported audience modes are `private`, `internal`, `public-intended`, and `public`; an absent mode is **Unknown** and must not be silently treated as public.

For changes affecting public behavior, installation, configuration, compatibility, security or privacy claims, operations, contributor workflow, or supported status, record the affected public document or an evidence-backed no-impact decision. For `public` and `public-intended` projects, a generic “no documentation impact” statement is insufficient.

Mechanical checks establish objective facts such as required paths, links, commands, generated references, and profile consistency. Independent review establishes semantic accuracy, usability, limitations, risk communication, license/support/disclosure decisions, and publication intent. First-publication and configured release gates evaluate the whole repository. Missing evidence blocks the gate; owner overrides record accepted exposure and do not claim that the risk is resolved.

## Challenge, blocks, and overrides

Consider alternatives privately for consequential decisions and present the selected path with a short reason. Block only for material harm, incompatible requirements, or insufficient evidence for an irreversible decision:

```text
BLOCKED: <decision>
Why: <material risk or contradiction>
Evidence: <concrete evidence or missing evidence>
Recommended alternative: <one path and why>
Unblock: <decision, investigation, or verification>
```

The user can override a block. Record the accepted risk and rationale, then proceed without claiming the risk is resolved.

## Completion controls

Before final handoff, assess documentation impact. For a task with a block, override, material review finding, failed verification, repeated rework, or durable user correction, assess retrospective signals and propose improvements; never apply a learning automatically.

Deep work requires a durable change record when OpenSpec is initialized: proposal, research/evidence, adversarial review, design, tasks, implementation evidence, retrospective, then archive. It also requires an independent review of both specification compliance and code/product quality. If the active host cannot execute that review, say so explicitly, offer its documented recovery path, and do not claim the review occurred.

For a Deep change affecting commands, installation, distribution, generated project guidance, or shared filesystem artifacts, complete [the Deep change checklist](deep-change-checklist.md) before implementation.

After correcting a material Deep review finding, obtain an independent review of the corrected artifact. Claim clean closure only after a pass with no material actionable findings; otherwise report unavailable review, residual risk, or an accepted override.

The final handoff states outcome and deliberate non-goals; evidence; material uncertainties; review and residual risk; decisions requiring the user; documentation-impact result; retrospective result; and any unavailable or degraded adapter control.

## Boundaries

`.careful/` is private local maintainer context. Do not read, copy, or quote it into tracked artifacts without an explicit user request. Public conclusions rely on tracked evidence.
