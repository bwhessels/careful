# Evidence Ledger

## Purpose

Define how Careful records, validates, and autonomously assesses consequential claims without making the ledger a second specification authority.

## Requirements

### Requirement: Consequential claims have inspectable records

Careful SHALL support a project-local evidence ledger for consequential claims. Each record SHALL contain a stable identifier, claim text, one of the four portable classifications, and evidence or an explicit unresolved reason appropriate to that classification.

#### Scenario: Recording a verified claim

- **WHEN** an agent or reviewer records a verified consequential claim
- **THEN** the record includes `Verified`, at least one evidence reference, and the date or context needed to assess freshness when relevant
- **AND** the record may link to affected paths, OpenSpec requirements, fixtures, or review findings.

#### Scenario: Recording an assumption or unknown

- **WHEN** a claim cannot be verified
- **THEN** the record uses `Assumption` or `Unknown`
- **AND** it states the reason, missing evidence, or unresolved question
- **AND** it does not represent the claim as verified by omission.

### Requirement: Evidence references are typed and bounded

Evidence records SHALL identify the kind and reference of supporting evidence. Supported evidence kinds SHALL include repository path, command result, test or fixture, review, and external source. Records SHALL not require or expose private `.careful/` content in tracked artifacts.

#### Scenario: Referencing consumer evidence

- **WHEN** a claim depends on an adapter or consumer-session result
- **THEN** the record identifies the fixture or session evidence separately from source-repository checks
- **AND** it identifies the affected adapter and source revision when available.

#### Scenario: Referencing external evidence

- **WHEN** a claim depends on an external source
- **THEN** the record retains a source reference and checked date when available
- **AND** it labels the claim according to what the source actually establishes.

### Requirement: Ledger records do not replace specifications

The evidence ledger SHALL link to the project’s declared specification authority when a requirement or decision is relevant, but SHALL NOT define or supersede requirements, designs, tasks, or change history.

#### Scenario: Project uses OpenSpec

- **GIVEN** the project declares OpenSpec as its specification authority
- **WHEN** a ledger record links to a requirement or change
- **THEN** the canonical requirement and decision remain under OpenSpec
- **AND** the ledger stores only the claim and its supporting evidence.

### Requirement: Ledger validation is deterministic

Careful SHALL validate record identifiers, classifications, required evidence or unresolved reasons, reference shape, duplicate identifiers, and supported evidence kinds. Validation SHALL report malformed or incomplete records without silently repairing them.

#### Scenario: Invalid record

- **WHEN** a record has an unsupported classification, duplicate identifier, missing required evidence, or malformed reference
- **THEN** validation fails with a record-scoped diagnostic
- **AND** no record is upgraded to a stronger classification.

### Requirement: Ledger use remains proportional and project-owned

Careful SHALL not require a ledger for every Quick task or low-consequence statement. Projects MAY configure when ledger records are required, and absent configuration SHALL preserve the existing workflow while allowing advisory reports.

#### Scenario: Ledger is not configured

- **WHEN** a project has no ledger configuration
- **THEN** Careful MAY report that consequential claims lack structured evidence
- **AND** it SHALL not create, overwrite, or require a ledger file without owner authorization.

### Requirement: Careful assesses ledger findings autonomously

Careful SHALL assess ledger records for evidence sufficiency, staleness, contradiction, materiality, and required follow-up. Assessment outcomes SHALL feed into workflow routing and SHALL not require the user to manually audit every record.

#### Scenario: Evidence is sufficient

- **WHEN** Careful verifies that a consequential claim has sufficient current evidence
- **THEN** it marks the finding `satisfied`
- **AND** it continues without asking the user to inspect the record.

#### Scenario: Evidence is stale or contradictory

- **WHEN** Careful detects stale or conflicting evidence for a material claim
- **THEN** it marks the finding `stale` or `contradiction`
- **AND** it adds verification or escalates/blocks according to the applicable risk boundary.

#### Scenario: User decision is required

- **WHEN** resolving a ledger finding requires owner authorization or an external action unavailable to Careful
- **THEN** it marks the finding `user-decision-needed`
- **AND** it flags the user with the evidence, consequence, recommended options, and unblock action.

### Requirement: Assessment state is retained and re-evaluated

Careful SHALL retain the latest assessment outcome for each task-scoped ledger finding and SHALL re-assess it after new evidence, corrections, overrides, or material changes to the analyzed work.

#### Scenario: New evidence resolves a finding

- **WHEN** new evidence addresses a previously unresolved ledger finding
- **THEN** Careful re-assesses the finding
- **AND** it removes the user flag or blocking state when the evidence satisfies the applicable requirement.
