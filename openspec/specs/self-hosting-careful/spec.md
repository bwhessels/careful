# Careful Self-Hosting Specification

## Purpose

Define how Careful develops and validates its own public harness while keeping private maintainer context separate from the open-source project.
## Requirements
### Requirement: Tracked self-hosting profile

The repository SHALL provide a tracked, non-sensitive project profile that identifies Careful as a self-hosting project, identifies the distributable plugin, declares validation commands and risk boundaries, maps public documentation locations, and identifies fixture projects used for consumer validation.

#### Scenario: Working on a public Careful behavior change

- **WHEN** a contributor changes a Careful workflow, skill contract, schema, or distributable plugin behavior
- **THEN** the harness SHALL use the tracked self-hosting profile to classify the work as Deep
- **AND** the harness SHALL route public requirements, design, and validation evidence to tracked project artifacts

#### Scenario: Working on a non-sensitive contributor change

- **WHEN** a contributor changes a public document or fixture without affecting a declared risk boundary
- **THEN** the harness SHALL use the profile to identify the affected validation and documentation locations
- **AND** the harness MAY select Standard depth when the change is reversible and low-risk

### Requirement: Private maintainer context boundary

The repository SHALL reserve `.careful/` for local maintainer context, notes, event records, and local profiles. The repository SHALL ignore `.careful/` in Git and SHALL not require any file in that directory for public build, validation, or consumer use.

#### Scenario: Capturing private working context

- **WHEN** a maintainer records product-specific preferences, sensitive research, or conversation-derived notes
- **THEN** the maintainer SHALL store those records under `.careful/`
- **AND** Git status SHALL report that directory as ignored

#### Scenario: Operating on public Careful artifacts

- **WHEN** the harness works in the Careful repository without an explicit request for private context
- **THEN** it SHALL not read or modify `.careful/`
- **AND** it SHALL base public conclusions on tracked artifacts and verified repository evidence

### Requirement: Public specification and change boundary

The repository SHALL track public current behavior in `openspec/specs/` and public proposed or completed changes in `openspec/changes/`. A public Careful change SHALL update the applicable current specification when it changes observable harness behavior.

#### Scenario: Proposing a public workflow change

- **WHEN** a proposed change alters how Careful classifies work, blocks decisions, creates artifacts, validates documentation, or learns from retrospectives
- **THEN** the change SHALL contain public requirements, design rationale, tasks, and validation evidence in OpenSpec artifacts
- **AND** the change SHALL not copy private `.careful/` content into those artifacts without explicit user approval

#### Scenario: Holding an unpublished idea

- **WHEN** a maintainer is exploring a sensitive or unpublished idea
- **THEN** the maintainer MAY retain the exploration in `.careful/` or a separate private workspace
- **AND** the idea SHALL become a tracked OpenSpec change only when it is intended for public project work

### Requirement: Consumer fixture validation

The repository SHALL maintain at least one tracked fixture project that represents an external consumer of Careful. The fixture SHALL be used to validate adoption, workflow, and distribution behavior that cannot be proven by operating only in Careful's source repository.

#### Scenario: Changing a distributed skill or schema

- **WHEN** a change modifies a skill trigger, workflow contract, OpenSpec schema, plugin manifest, or installation-facing documentation
- **THEN** the implementation plan SHALL include validation against a fixture project
- **AND** the final evidence SHALL identify the fixture result separately from source-repository validation

### Requirement: Release and refresh boundary

The repository SHALL treat a released or installed Careful plugin as the baseline used to work on the next Careful change. After a distributable plugin update, the release process SHALL require a fresh Codex thread before evaluating the updated skill behavior.

#### Scenario: Evaluating an updated Careful skill

- **WHEN** a distributable Careful skill has been updated and installed
- **THEN** the evaluator SHALL begin a new Codex thread for the behavioral evaluation
- **AND** the evaluation SHALL not rely solely on the authoring thread's already-loaded skill context

