# Careful portable workflow contract

Version: 1

This is the canonical, host-neutral policy for every supported Careful adapter. Adapters supply discovery, commands, permissions, and review mechanics; they do not redefine this policy.

## Baseline

For substantive product, coding, debugging, and architecture work, select one depth before implementation:

- **Quick** — reversible, narrow work with clear evidence.
- **Standard** — ordinary implementation or investigation; verify material claims and assess documentation impact.
- **Deep** — risky, architectural, product, public-contract, data, security, privacy, reliability, or hard-to-reverse work; use a durable OpenSpec change when available, challenge the decision, and obtain independent review.

For consequential claims, use only these labels: **Verified**, **Inferred**, **Assumption**, and **Unknown**. Research time-sensitive or consequential external claims and do not overstate sources.

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
