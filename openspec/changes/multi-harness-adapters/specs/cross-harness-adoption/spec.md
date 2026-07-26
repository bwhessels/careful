## ADDED Requirements

### Requirement: Cross-harness project adoption
Careful SHALL provide documented adoption paths for Codex, Claude Code, and Factory Droid that share project-level policy while using only the host-specific files required for discovery. An adopted project SHALL remain usable when one supported adapter is absent.

#### Scenario: Project uses more than one supported harness
- **WHEN** a project adopts Careful for multiple supported harnesses
- **THEN** shared policy SHALL have one canonical tracked source
- **AND** each host-specific entry point SHALL be a minimal adapter rather than an independent policy document

### Requirement: Compatibility matrix
Careful SHALL publish a compatibility matrix that identifies every supported adapter, verified host assumptions, implemented core controls, intentional degradations, installation instructions, and fixture status.

#### Scenario: Evaluating a harness choice
- **WHEN** a prospective user evaluates Careful for Claude Code or Factory Droid
- **THEN** the documentation SHALL state whether each consequential Careful control is verified, degraded, or unsupported
- **AND** it SHALL link to the relevant adapter installation instructions

### Requirement: Consumer fixtures across adapters
Careful SHALL maintain a tracked consumer fixture or fixture variant for every supported adapter. A workflow, manifest, or shared-policy change SHALL validate the relevant fixture variants before release.

#### Scenario: Updating shared core behavior
- **WHEN** a change modifies the portable workflow contract or adapter manifest
- **THEN** maintainers SHALL validate every supported adapter fixture
- **AND** the evidence SHALL identify each adapter result separately
