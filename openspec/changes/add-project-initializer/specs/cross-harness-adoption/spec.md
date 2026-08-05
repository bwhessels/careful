## MODIFIED Requirements

### Requirement: Cross-harness project adoption
Careful SHALL provide documented initializer-driven adoption paths for Codex, Claude Code, and Factory Droid that share project-level policy while using only the host-specific files required for discovery. An adopted project SHALL remain usable when one supported adapter is absent. The initializer command SHALL own filesystem mutations, while `careful-adopt` SHALL guide or invoke that command and then perform evidence-led project profiling.

#### Scenario: Project uses more than one supported harness
- **WHEN** a project adopts Careful for multiple supported harnesses
- **THEN** shared policy SHALL have one canonical source under `vendor/careful/`
- **AND** each host-specific entry point SHALL be a minimal adapter rather than an independent policy document
- **AND** adapter status SHALL be derived from the resolved source's canonical manifest

#### Scenario: A host skill encounters an uninitialized project
- **WHEN** `careful-adopt` determines that the target project is uninitialized
- **THEN** it SHALL guide or invoke the canonical initializer command according to host capability and user authorization
- **AND** it SHALL not reproduce the command's filesystem mutation logic

### Requirement: Consumer fixtures across adapters
Careful SHALL maintain tracked consumer fixture variants for every supported adapter and for both linked and portable initializer source modes. An initializer, workflow, manifest, shared-policy, or adoption-contract change SHALL validate the relevant fixture variants before release.

#### Scenario: Updating initializer or shared adoption behavior
- **WHEN** a change modifies the initializer command, portable workflow contract, adapter manifest, project-facing guidance, or `careful-adopt`
- **THEN** maintainers SHALL validate linked and portable fixtures for every affected adapter
- **AND** the evidence SHALL identify each adapter and source-mode result separately
