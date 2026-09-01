# Change-Impact Analysis

## Purpose

Define how Careful maps repository changes to workflow surfaces, assesses the consequences, and flags only material unresolved decisions.

## Requirements

### Requirement: Impact analysis maps changes to workflow surfaces

Careful SHALL provide a deterministic impact report that accepts changed paths or a repository diff and identifies potentially affected specifications, execution plans, documentation, adapters, fixtures, project checks, and independent review requirements.

#### Scenario: Workflow skill changes

- **WHEN** a changed path is within a distributed workflow skill
- **THEN** the report identifies the affected adapter distribution and relevant consumer fixtures
- **AND** it recommends fresh-session validation for affected hosts when the adapter contract requires it.

#### Scenario: Public behavior changes

- **WHEN** a changed path affects public behavior, installation, configuration, compatibility, security/privacy claims, operations, or contributor workflow
- **THEN** the report identifies the configured canonical public document or reports that the mapping is unknown
- **AND** it identifies the applicable public-readiness or release check when configured.

### Requirement: Mappings expose their confidence and evidence

Every impact mapping SHALL be classified as `verified`, `inferred`, or `unknown` and SHALL include the configuration, manifest, convention, or missing evidence that produced the classification.

#### Scenario: Explicit project mapping

- **GIVEN** a project explicitly maps a path or pattern to a documentation or validation surface
- **WHEN** that path changes
- **THEN** the report marks the mapping as verified
- **AND** it identifies the mapping source.

#### Scenario: No reliable mapping

- **WHEN** changed content cannot be mapped reliably
- **THEN** the report marks the affected surface as unknown
- **AND** it does not claim that the surface is unaffected.

### Requirement: Impact analysis preserves specification authority

Careful SHALL resolve and honor the project’s declared specification authority when reporting specification impact. Impact analysis SHALL not create a parallel durable specification or silently migrate competing documents.

#### Scenario: OpenSpec project

- **GIVEN** a project declares OpenSpec as its specification authority
- **WHEN** a changed path may alter a capability or requirement
- **THEN** the report points to the applicable OpenSpec spec or change
- **AND** it keeps any execution-plan recommendation separate from the durable specification.

### Requirement: Impact analysis distinguishes recommendations from obligations

The report SHALL distinguish a surface that is probably relevant from a project-configured requirement or gate that must be satisfied. Heuristic or inferred matches SHALL not fail a workflow unless the project explicitly configures them as enforceable.

#### Scenario: Inferred documentation match

- **WHEN** a path convention suggests a documentation impact but no project rule requires a particular update
- **THEN** the report emits an inferred recommendation
- **AND** it does not claim a documentation failure solely from that recommendation.

#### Scenario: Configured required surface

- **GIVEN** a project configures an impact mapping or release gate as required
- **WHEN** the affected surface has no corresponding evidence or follow-up
- **THEN** the configured check fails or reports a blocking finding according to project policy
- **AND** the report identifies the missing evidence and unblock action.

### Requirement: Reports are non-destructive and capability-aware

Impact analysis SHALL be read-only with respect to project-owned specifications, documentation, source, and private context. When a host cannot provide a diff, manifest, fixture, or other required input, it SHALL report the unavailable input and degraded analysis rather than infer completeness.

#### Scenario: Host cannot provide changed paths

- **WHEN** the active adapter cannot provide a reliable repository diff
- **THEN** the report identifies changed-path input as unavailable
- **AND** it does not claim exhaustive impact coverage.

### Requirement: Reports are reproducible

For the same repository inputs, project configuration, source revision, and changed-path set, impact analysis SHALL produce deterministic findings and ordering.

#### Scenario: Re-running analysis

- **WHEN** the same impact inputs are analyzed twice
- **THEN** the affected surfaces, classifications, diagnostics, and ordering are equivalent
- **AND** timestamps or environment details do not alter the substantive result.

### Requirement: Impact findings drive workflow follow-up

Careful SHALL assess impact findings and use their outcomes to add verification work, escalate workflow depth, block completion, or continue without interruption according to materiality, portable policy, and project configuration.

#### Scenario: Material adapter impact

- **WHEN** impact analysis identifies a material change to an adapter or shared workflow contract
- **THEN** Careful adds the relevant adapter validation and consumer-fixture checks
- **AND** it escalates to Deep when the applicable risk boundary requires Deep work.

#### Scenario: Informational inferred match

- **WHEN** an inferred impact mapping is informational and does not affect safety, public claims, compatibility, release readiness, or an owner decision
- **THEN** Careful retains the finding in task evidence
- **AND** it continues without requiring user review.

#### Scenario: Configured check satisfies an affected surface

- **GIVEN** the project explicitly enables a check for an affected surface
- **WHEN** Careful executes that check successfully
- **THEN** the matching material impact finding is marked `satisfied`
- **AND** Careful retains the command result as assessment evidence without asking the user to repeat the check.

### Requirement: Material unresolved findings are flagged to the user

Careful SHALL prioritize and flag findings that require project-owner judgment, authorization, external evidence, or acceptance of material residual risk. The flag SHALL state the finding, evidence, consequence, recommended options, and unblock action.

#### Scenario: Public claim lacks current evidence

- **WHEN** a changed surface affects a public compatibility or security claim and current supporting evidence is unavailable
- **THEN** Careful marks the finding as `user-decision-needed` or `stale`
- **AND** it flags the user rather than presenting the raw impact report for manual audit.

#### Scenario: Accepted risk

- **WHEN** the user explicitly accepts a documented residual risk
- **THEN** Careful records the rationale and marks the finding `accepted-risk`
- **AND** it does not describe the risk as resolved.

### Requirement: Final handoffs summarize assessment outcomes

Careful SHALL use the latest impact assessments in its final handoff. The handoff SHALL summarize unresolved, blocked, accepted-risk, and user-decision-needed findings, while omitting routine satisfied findings unless they are material evidence for completion.

#### Scenario: No material findings remain

- **WHEN** all material impact findings are satisfied or verified through configured checks
- **THEN** Careful reports that no user decision is required
- **AND** it does not require a manual audit of the complete impact report.

### Requirement: Independent review includes structural hygiene

Independent code/product-quality review SHALL assess unnecessary complexity or boilerplate, AI-generated filler, duplicated logic, likely unused code, oversized files, naming/cohesion issues, and whether tests demonstrate behavior. Static hygiene checks SHALL report evidence-backed candidates and limitations rather than claim that no findings proves semantic cleanliness.

#### Scenario: Hygiene candidate is found

- **WHEN** a structural hygiene check identifies a likely duplication, unused definition, placeholder, filler, or oversized file
- **THEN** Careful records the category, severity, confidence, path, and concrete evidence
- **AND** it routes material candidates for correction or user decision according to workflow policy.

#### Scenario: Hygiene review finds no candidates

- **WHEN** the configured hygiene checks produce no findings
- **THEN** Careful reports the checks and their scope as evidence
- **AND** it states that static cleanliness does not prove the absence of semantic duplication or unused behavior.
