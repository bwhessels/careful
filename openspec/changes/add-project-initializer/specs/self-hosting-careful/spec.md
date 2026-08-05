## MODIFIED Requirements

### Requirement: Consumer fixture validation
The repository SHALL maintain tracked fixture variants for every supported Careful adapter and both initializer source modes. Each fixture SHALL validate adoption, workflow, distribution, source resolution, and project/private artifact boundaries that cannot be proven by operating only in Careful's source repository.

#### Scenario: Changing the initializer or distributed adoption behavior

- **WHEN** a change modifies the initializer command, skill trigger, workflow contract, adapter manifest, OpenSpec schema, plugin manifest, source mount, receipt schema, or installation-facing documentation
- **THEN** the implementation plan SHALL include linked and portable validation for every affected adapter fixture
- **AND** the final evidence SHALL identify every adapter and source-mode result separately from source-repository validation

#### Scenario: Changing a distributed Careful skill

- **WHEN** a change modifies `careful-adopt` or another distributed skill
- **THEN** every changed skill SHALL pass the skill-creator validator
- **AND** the distributable Codex plugin SHALL pass the plugin-creator validator
