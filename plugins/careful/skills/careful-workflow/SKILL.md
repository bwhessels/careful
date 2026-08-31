---
name: careful-workflow
description: Run the default Careful workflow for product exploration, feature work, architecture changes, bug fixes, and implementation requests. Use whenever Codex should automatically classify risk, challenge consequential decisions, distinguish evidence from assumptions, select Quick/Standard/Deep depth, coordinate OpenSpec artifacts when warranted, and provide a final evidence-based handoff.
---

# Careful Workflow

Apply Careful without requiring the user to remember workflow commands. Read the [portable core contract](references/core-contract.md) before beginning substantive work.

## Classify and select depth

Before classification, look for `careful.project.yaml`. When present, use its commands, risk boundaries, documentation map, and self-hosting fixture requirements. Do not read `.careful/` unless the user explicitly requests private local context.

Treat an explicit user request for Quick or Deep as authoritative. Otherwise select:

- **Quick** for contained, reversible work with no public, product, architectural, data, security, or compatibility impact.
- **Standard** for ordinary feature, bug-fix, refactor, and product work.
- **Deep** for risky changes; architecture, product, public-contract, data, security, privacy, reliability, or hard-to-reverse decisions; or material uncertainty. Escalate to Deep when new evidence crosses a threshold.

Use OpenSpec only for Deep work or when the change needs durable requirements/history. For an initialized project, use its configured schema. Otherwise offer initialization once the user accepts a durable change.

Route the Deep distribution check from the request and repository evidence: when a Deep change affects commands, installation, distribution, generated project guidance, or shared filesystem artifacts, read and complete the [portable Deep change checklist](references/deep-change-checklist.md) before implementation. When none of those surfaces changes, continue with ordinary Deep controls using the core contract.

## Work loop

1. Inspect the codebase and relevant evidence before recommending a path.
2. Label consequential statements as **Verified**, **Inferred**, **Assumption**, or **Unknown**.
3. For consequential decisions, consider alternatives privately and present one recommendation with a concise reason.
4. Block only for material harm, incompatible requirements, or insufficient evidence for an irreversible decision. State the evidence, the recommended alternative, and what would unblock the work.
5. Honor an explicit user override. Record the rationale and accepted risk; do not represent the risk as resolved.
6. Build incrementally; use tests, existing project commands, and focused checks as evidence.
7. Run autonomous evidence, change-impact, and codebase-hygiene assessment at task start, after material changes, and before finalizing when the project provides the assessment commands or ledger. Treat the assessment as internal workflow state: satisfy routine findings automatically, add verification or escalate when findings are material, and flag the user only for owner decisions, unavailable external evidence, or accepted residual risk.
8. For behavior, contract, architecture, configuration, operational, or contributor-workflow changes, apply the documentation map inline: identify the canonical document, update it once, or retain evidence for a no-impact conclusion. Do not require a documentation command for this baseline check.
9. For Deep work, obtain an independent review after implementation. Separate spec/decision compliance from code/product quality. After correcting a material finding, obtain an independent review of the corrected artifact; claim clean closure only after a pass with no material actionable findings. Otherwise report unavailable review, residual risk, or an accepted override.
10. Before finalizing, assess retrospective signals: blocks, overrides, material review findings, failed verification, repeated rework, and durable user corrections. Report no high-signal candidate or present concise evidence-backed candidates. Do not require a retrospective command for this baseline check.
11. Provide the final handoff in the format in the [portable core contract](references/core-contract.md), including documentation-impact, autonomous-assessment, and retrospective-assessment results when applicable.

Before creating a durable proposal, design, requirements document, or change record, resolve the project’s declared specification authority. When `documentation.spec_authority: openspec` is present, use OpenSpec for durable artifacts and use the configured execution-plan location only for linked implementation plans. Do not create a parallel durable specification under `docs/superpowers/specs/`; report an existing competing document for owner review instead of migrating it silently.

## Special entry points

- For exploration, do not implement. Use the OpenSpec explore stance: investigate, challenge framing, and identify unknowns.
- For an existing unfamiliar project, invoke `careful-adopt` before relying on inferred conventions.
- Use `careful-documentation` for a dedicated documentation audit, information-architecture redesign, or documentation repair.
- Use `careful-retrospective` for an explicit or full retrospective; run it before the final handoff when its outcome must be presented in that handoff.

## Explicit controls

Honor `/careful:quick`, `/careful:deep`, `/careful:review`, `/careful:retro`, `/careful:adopt`, and `/careful:override <reason>` as force/escape hatches. Do not require them during ordinary work.
