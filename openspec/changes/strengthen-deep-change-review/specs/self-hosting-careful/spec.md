## MODIFIED Requirements

### Requirement: Public specification and change boundary

The repository SHALL track public current behavior in `openspec/specs/` and public proposed or completed changes in `openspec/changes/`. A public Careful change SHALL update the applicable current specification when it changes observable harness behavior. Active changes SHALL declare and validate any predecessor required to modify a capability not yet present in current specifications.

#### Scenario: Proposing a public workflow change

- **WHEN** a proposed change alters how Careful classifies work, blocks decisions, creates artifacts, validates documentation, reviews corrected material findings, or learns from retrospectives
- **THEN** the change SHALL contain public requirements, design rationale, tasks, and validation evidence in OpenSpec artifacts
- **AND** the change SHALL not copy private `.careful/` content into those artifacts without explicit user approval

#### Scenario: Modifying a capability introduced by another active change

- **WHEN** an active change modifies a capability absent from current specs but added by another active change
- **THEN** the modifying change SHALL declare the predecessor in machine-readable change metadata
- **AND** self-hosting validation SHALL fail when that dependency is missing or invalid

#### Scenario: Holding an unpublished idea

- **WHEN** a maintainer is exploring a sensitive or unpublished idea
- **THEN** the maintainer MAY retain the exploration in `.careful/` or a separate private workspace
- **AND** the idea SHALL become a tracked OpenSpec change only when it is intended for public project work
