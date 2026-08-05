## Why

The adversarial review of `add-project-initializer` repeatedly found material issues after strict OpenSpec validation had passed: an undeclared dependency on an active predecessor change, incomplete command and distribution contracts, and the need for a clean review after corrections. These are general Deep-change quality failures rather than initializer-specific product requirements.

Careful should turn the approved retrospective lessons into one mechanical dependency check and two narrowly triggered workflow controls, without burdening Quick or ordinary Standard work.

## What Changes

- Add a deterministic validator for active OpenSpec dependencies. A change that modifies a capability absent from current specs but added by another active change must declare that predecessor in `.openspec.yaml` using `depends_on`.
- Add a triggered Deep design checklist for commands, initializers, installers, packaging, shared filesystem artifacts, and other distribution changes. The checklist covers bootstrap entry points, stable consumer paths, cloneable source identity, deterministic/non-interactive behavior, tracked/local/private state, and lifecycle recovery.
- Require one clean independent re-review after material Deep specification or implementation findings are corrected. If a clean pass is unavailable, record the residual risk or explicit user override instead of claiming review closure.
- Apply the dependency convention to the active initializer change and validate representative consumer/change fixtures.

Explicit non-goals: replacing OpenSpec's own schema validator, requiring the distribution checklist for unrelated changes, infinite review loops, adding review requirements to Quick work, or automatically accepting/rejecting review findings.

## Dependency and sequencing

This change depends on `multi-harness-adapters` because it updates the shared portable policy and distributed workflow adapters established by that change. The predecessor SHALL be synced and archived before this change is archived or released.

## Capabilities

### New Capabilities

- `deep-change-quality-controls`: Mechanical active-change dependency validation, triggered distribution-contract completeness, and clean re-review closure for material Deep findings.

### Modified Capabilities

- `self-hosting-careful`: Extend public change validation and fixtures to cover declared active-change dependencies.

## Impact

Affects the portable core policy, Careful workflow adapters, the Critical Deep design template, self-hosting validation scripts, fixtures, contributor/design documentation, and active change metadata. It does not add a runtime service or external dependency.
