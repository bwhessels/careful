# Public Readiness

## ADDED Requirements

### Requirement: Project-specific public-readiness contract

Careful SHALL resolve public audience mode, required documents, canonical public documents, configured checks, and publication/release gates from project configuration or explicit adoption decisions.

#### Scenario: Public-intended project

- **GIVEN** a project declares `public_readiness.audience: public-intended`
- **WHEN** Careful handles a public-impact change or publication gate
- **THEN** it applies that project’s configured documents and checks
- **AND** does not substitute a universal document list.

#### Scenario: Unclassified project

- **GIVEN** no public audience mode is configured
- **WHEN** adoption determines that publication status materially affects the workflow
- **THEN** Careful reports the mode as unknown
- **AND** asks the owner for the decision rather than assuming `public`.

### Requirement: Public documentation impact

Careful SHALL require a documented public-documentation impact decision for changes affecting public behavior, installation, configuration, compatibility, security/privacy/operations, contributor workflow, or supported status.

#### Scenario: Updated public contract

- **GIVEN** a change affects a configured public contract
- **WHEN** the task is completed
- **THEN** the evidence names the updated canonical document and verification result.

#### Scenario: Deliberate no-impact result

- **GIVEN** a public-impact classification was considered
- **WHEN** no public document requires an update
- **THEN** the evidence identifies the checked contract and concrete reason
- **AND** does not rely only on a generic no-impact statement.

### Requirement: Mechanical documentation verification

Careful SHALL support project-configured checks for required artifacts, links, commands, generated references, and profile consistency.

#### Scenario: Failed configured check

- **GIVEN** a configured documentation check fails
- **WHEN** a publication or release gate runs
- **THEN** the gate reports the failure and does not pass without an explicit accepted-risk override.

### Requirement: Independent public-readiness review

Careful SHALL require independent review for Deep public-contract changes and configured first-publication or release gates.

#### Scenario: Semantic drift

- **GIVEN** configured mechanical checks pass
- **AND** public documentation overstates current behavior or omits material limitations
- **WHEN** independent review runs
- **THEN** the reviewer reports the concrete evidence, residual risk, and correction needed
- **AND** the gate does not claim clean closure.

### Requirement: Explicit owner decisions

Careful SHALL report unresolved license, privacy, security-disclosure, support-status, and publication-intent decisions without inventing or silently accepting them.

#### Scenario: Missing consequential decision

- **GIVEN** a first-publication gate lacks an owner-approved license or disclosure decision required by the project profile
- **WHEN** the gate runs
- **THEN** it reports the missing decision and unblock condition
- **AND** does not represent the project as public-ready.
