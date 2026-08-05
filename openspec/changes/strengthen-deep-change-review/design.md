## Context

Strict OpenSpec validation proves artifact shape, not cross-change sequencing or operational design completeness. During the initializer review, `portable-workflow-core` and `cross-harness-adoption` were modified before they existed in current specs; the validator accepted the change. Independent review also needed several passes to expose source-mount, URL, non-interactive, and bootstrap ambiguities.

The approved response has two enforcement levels: automate the relationship that can be derived mechanically, and add concise triggered guidance for judgments that require design reasoning.

## Decisions

### 1. Declare active-change dependencies in `.openspec.yaml`

An active change MAY declare direct predecessors using:

```yaml
depends_on:
  - multi-harness-adapters
```

The validator SHALL read active change proposals and current capability directories. When change B modifies a capability absent from `openspec/specs/` and change A adds that capability, B SHALL list A in `depends_on`. Validation SHALL reject missing active dependencies, unknown dependency names, self-dependencies, and dependency cycles. It SHALL report the consumer change, capability, and required predecessor.

The check SHALL use the Python standard library and remain separate from OpenSpec's schema validation. `scripts/validate_self_hosting.py` SHALL invoke it so the project validation command cannot omit the rule.

### 2. Trigger a structural checklist only for distribution-like Deep changes

The portable policy SHALL require a distribution-contract section when a Deep change creates or modifies a command, initializer, installer, package/plugin distribution, symlink/submodule layout, generated project guidance, or another shared filesystem artifact. The Critical Deep design template SHALL provide these slots:

- Bootstrap and discovery entry point.
- Stable consumer mount and reference resolution.
- Cloneable source identity and immutable version/revision behavior.
- Interactive, dry-run, and non-interactive defaults.
- Tracked, ignored, local, and private state ownership.
- Upgrade, repair, migration, rollback, and destructive-action boundaries.

Each slot SHALL contain a concrete decision or `Not applicable — <evidence>`. Unrelated Deep changes SHALL not be forced to include the section. Host adapter skills SHALL point to the portable rule rather than copy the checklist.

### 3. Close material review findings with one clean pass

A material finding is one that changes a requirement, public contract, architecture, security/privacy boundary, compatibility claim, migration behavior, or verification conclusion. After correcting a material Deep spec or implementation finding, Careful SHALL obtain another independent review of the corrected artifact. Review closure requires a pass with no material actionable findings.

If another material finding appears, correct it and repeat. If independent review is unavailable or the user accepts residual risk, the handoff SHALL state the missing clean pass or override; Careful SHALL not claim the review is clean. Minor editorial findings do not reset the clean-pass gate.

### 4. Validate mechanics and behavior separately

Dependency behavior SHALL use deterministic unit fixtures and a self-hosting integration check. The checklist and clean-pass rule SHALL use pressure scenarios against the workflow skill: capture baseline behavior without the new guidance, add the smallest portable-policy/workflow update, and forward-test the same scenarios in fresh contexts. Skill and plugin validators prove package shape but do not replace behavioral tests.

## Risks and mitigations

- **Markdown proposal parsing is brittle.** Parse only the documented capability headings and backticked bullet identifiers; fail clearly on ambiguous declarations.
- **Dependency checks create false ordering constraints.** Require a dependency only when the modified capability is absent from current specs and an active change explicitly adds it.
- **The checklist becomes universal ceremony.** Gate it on observable distribution/command/file-layout triggers and allow evidenced non-applicability per slot.
- **Review loops never end.** Reset only for material actionable findings; otherwise record unresolved residual risk or an explicit override.
- **Adapters drift from the portable rule.** Keep normative language in `core/` and thin adapter references, then run parity and fresh-session fixtures where available.

## Validation

- Unit tests demonstrate missing dependency failure before implementation, then cover declared, unknown, self, and cyclic dependencies.
- Self-hosting validation runs the dependency validator against the real active changes.
- Baseline and forward pressure scenarios cover skipped distribution fields and premature review closure.
- Validate every changed skill, the Codex plugin, all OpenSpec artifacts, and affected adapter fixtures.
- Obtain independent specification-compliance and code/product-quality reviews; after material corrections, obtain one clean confirmation pass.
