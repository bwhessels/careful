# Specification Authority

## ADDED Requirements

### Requirement: Project specification authority

Careful SHALL resolve a project’s durable specification authority from its project profile or explicit adoption decision before creating durable proposal, design, requirement, or change artifacts.

#### Scenario: OpenSpec authority

- **GIVEN** a project declares `documentation.spec_authority: openspec`
- **WHEN** Careful plans or records a Deep change
- **THEN** the durable proposal, design, requirements, tasks, and change history are stored under the project’s OpenSpec locations
- **AND** any execution plan links to the OpenSpec artifact
- **AND** Careful does not create a parallel durable specification under `docs/superpowers/specs/`.

#### Scenario: Project-defined authority

- **GIVEN** a project declares `documentation.spec_authority: project-defined`
- **AND** identifies its canonical specification location or command
- **WHEN** Careful records a durable change
- **THEN** it uses that authority
- **AND** reports any competing durable specification location for owner review.

#### Scenario: No authority

- **GIVEN** a project declares `documentation.spec_authority: none`
- **WHEN** Careful handles a change
- **THEN** it does not require a durable specification system
- **AND** it records the project’s explicit decision and continues to apply ordinary documentation-impact controls.

### Requirement: Execution-plan separation

Careful SHALL distinguish execution plans from durable specifications. An execution plan SHALL identify the canonical specification it implements when a project has a durable specification authority.

#### Scenario: Linked execution plan

- **GIVEN** a project has a durable specification authority
- **WHEN** an execution plan is created
- **THEN** it is stored in the project’s configured execution-plan location
- **AND** it links to the canonical specification
- **AND** it does not become an independent source of requirements or decisions.

### Requirement: Duplicate specification detection

Careful SHALL detect a durable-looking specification outside the declared authority and report it without deleting, overwriting, or silently merging it.

#### Scenario: Competing specification path

- **GIVEN** a project declares OpenSpec as its authority
- **AND** `docs/superpowers/specs/` contains a durable-looking specification
- **WHEN** adoption, Deep planning, completion, or release review runs
- **THEN** Careful reports the declared authority and competing path
- **AND** identifies the owner decision required for migration, archival, deletion, or pointer conversion.

#### Scenario: Historical or pointer document

- **GIVEN** a competing path is explicitly marked as historical or as a pointer to the canonical specification
- **WHEN** duplicate detection runs
- **THEN** it reports the path as non-authoritative context
- **AND** does not treat it as an unresolved duplicate.

### Requirement: Non-destructive migration

Careful SHALL require explicit owner direction before changing, deleting, archiving, or merging a competing durable specification.

#### Scenario: Migration requires approval

- **GIVEN** duplicate specification content is found
- **WHEN** no explicit owner migration decision exists
- **THEN** the workflow reports the conflict and recommended next action
- **AND** does not mutate either specification.

### Requirement: Adapter and fixture parity

The portable authority-resolution rule SHALL be available to all supported Careful adapters and SHALL be validated with adopted-project fixtures.

#### Scenario: Fresh adopted consumer

- **GIVEN** an adopted consumer project declares OpenSpec authority
- **WHEN** a fresh Careful session handles a Deep change
- **THEN** it resolves OpenSpec as canonical
- **AND** preserves execution-plan separation
- **AND** reports duplicate durable specifications consistently with the source policy.
