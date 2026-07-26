## MODIFIED Requirements

### Requirement: Tracked self-hosting profile
The repository SHALL provide a tracked, non-sensitive project profile that identifies Careful as a self-hosting project, identifies every distributable adapter, declares validation commands and risk boundaries, maps public documentation locations, and identifies fixture projects used for consumer validation.

#### Scenario: Working on a public Careful behavior change

- **WHEN** a contributor changes a Careful workflow, portable core contract, adapter mapping, schema, or distributable adapter behavior
- **THEN** the harness SHALL use the tracked self-hosting profile to classify the work as Deep
- **AND** the harness SHALL route public requirements, design, and validation evidence to tracked project artifacts

#### Scenario: Working on a non-sensitive contributor change

- **WHEN** a contributor changes a public document or fixture without affecting a declared risk boundary
- **THEN** the harness SHALL use the profile to identify the affected validation and documentation locations
- **AND** the harness MAY select Standard depth when the change is reversible and low-risk

### Requirement: Consumer fixture validation
The repository SHALL maintain at least one tracked fixture project or fixture variant for every supported Careful adapter. Each fixture SHALL be used to validate adoption, workflow, and distribution behavior that cannot be proven by operating only in Careful's source repository.

#### Scenario: Changing a distributed adapter or schema

- **WHEN** a change modifies a skill trigger, workflow contract, adapter manifest, OpenSpec schema, plugin manifest, or installation-facing documentation
- **THEN** the implementation plan SHALL include validation against every affected adapter fixture
- **AND** the final evidence SHALL identify every fixture result separately from source-repository validation

### Requirement: Release and refresh boundary
The repository SHALL treat each released or installed Careful adapter as the baseline used to work on the next Careful change. After a distributable adapter update, the release process SHALL require a fresh session in the affected host before evaluating the updated behavior.

#### Scenario: Evaluating an updated Careful adapter

- **WHEN** a distributable Careful adapter has been updated and installed
- **THEN** the evaluator SHALL begin a new session in the affected supported harness for behavioral evaluation
- **AND** the evaluation SHALL not rely solely on the authoring session's already-loaded instruction context
