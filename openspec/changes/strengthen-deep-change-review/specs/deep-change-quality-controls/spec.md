## ADDED Requirements

### Requirement: Active OpenSpec dependency validation

Careful SHALL validate dependencies between active OpenSpec changes. A change that modifies a capability absent from current specs but added by another active change SHALL declare that predecessor under `depends_on` in its `.openspec.yaml`. The declaration SHALL use a top-level block list with two-space-indented, unquoted change names; noncanonical inline or quoted forms SHALL fail clearly.

#### Scenario: Modified capability is introduced by an active predecessor

- **WHEN** change B modifies a capability absent from `openspec/specs/` and change A adds that capability
- **THEN** validation SHALL fail unless B lists A in `depends_on`
- **AND** the failure SHALL identify B, the capability, and A

#### Scenario: Dependency graph is invalid

- **WHEN** an active change declares an unknown change, itself, or a dependency cycle
- **THEN** validation SHALL fail with the involved change names

#### Scenario: Predecessor has been archived first

- **WHEN** an active change retains a dependency on predecessor A and A has moved to a date-prefixed OpenSpec archive directory
- **THEN** validation SHALL accept A's original change name as satisfied historical provenance
- **AND** a name absent from both active changes and date-prefixed archives SHALL remain unknown

#### Scenario: Dependency metadata is noncanonical

- **WHEN** an active change uses an inline `depends_on` list or quoted dependency item
- **THEN** validation SHALL fail with a deterministic change-scoped metadata error

#### Scenario: Modified capability is already current

- **WHEN** a change modifies a capability present under `openspec/specs/`
- **THEN** validation SHALL not require an active predecessor solely for that capability

### Requirement: Triggered distribution-contract design

For a Deep change that creates or modifies a command, initializer, installer, package/plugin distribution, symlink/submodule layout, generated project guidance, or shared filesystem artifact, Careful SHALL record bootstrap/discovery, consumer paths, source identity/versioning, interaction defaults, state ownership, and lifecycle recovery in the design. Each field SHALL contain a concrete decision or evidenced non-applicability.

#### Scenario: Designing an initializer

- **WHEN** a Deep design introduces an initializer command and linked or vendored files
- **THEN** the design SHALL define its bootstrap entry point, stable consumer path, cloneable source identity, deterministic and non-interactive behavior, tracked/local/private state, and repair/upgrade/migration/rollback boundaries

#### Scenario: Deep change has no distribution surface

- **WHEN** a Deep change affects no command, installer, distribution, generated guidance, or shared filesystem artifact
- **THEN** Careful SHALL not require the distribution-contract section

### Requirement: Clean closure after material review findings

After a material finding in a Deep specification or implementation review is corrected, Careful SHALL independently re-review the corrected artifact. Review closure requires a pass with no material actionable findings, or an explicit record that review was unavailable or residual risk was accepted.

#### Scenario: Correcting a material review finding

- **WHEN** a review finding changes a requirement, public contract, architecture, security/privacy boundary, compatibility claim, migration behavior, or verification conclusion
- **THEN** Careful SHALL correct or explicitly disposition the finding
- **AND** it SHALL obtain an independent review of the corrected artifact before claiming clean closure

#### Scenario: Corrected artifact produces another material finding

- **WHEN** the confirmation review produces another material actionable finding
- **THEN** Careful SHALL not claim review closure
- **AND** it SHALL repeat correction and independent review or record the residual risk/override

#### Scenario: Review is unavailable

- **WHEN** a clean independent re-review cannot run
- **THEN** the handoff SHALL report the unavailable clean pass and recovery path
- **AND** it SHALL not claim the review completed cleanly
