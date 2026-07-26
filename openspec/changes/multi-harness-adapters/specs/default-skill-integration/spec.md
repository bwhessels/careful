## MODIFIED Requirements

### Requirement: Main workflow owns baseline checks
The primary Careful workflow adapter SHALL contain the baseline documentation-impact and retrospective-signal checks required for normal Careful work. The baseline checks SHALL run without requiring the user to invoke a documentation or retrospective command when the host supports automatic workflow activation. When the host cannot verify automatic activation, the adapter SHALL expose the documented explicit activation path and report that limitation before claiming the baseline checks ran.

#### Scenario: Completing a behavior-affecting task

- **WHEN** Careful completes a task that changes behavior, a public contract, architecture, configuration, operations, or contributor workflow
- **THEN** the active adapter SHALL assess documentation impact before finalizing the task
- **AND** it SHALL update the canonical public document or report an evidence-based no-impact conclusion

#### Scenario: Completing work with a learning signal

- **WHEN** a task includes a block, override, material review finding, failed verification, repeated rework, or direct durable user correction
- **THEN** the active adapter SHALL perform a lightweight retrospective assessment before finalizing the task
- **AND** it SHALL report either no high-signal lesson candidates or the proposed candidate improvements

### Requirement: Specialist skills provide depth
Careful SHALL package separate documentation and retrospective specialist workflows for every supported harness using that host's documented skill, command, or explicit fallback mechanism. They SHALL provide detailed workflows for dedicated documentation work and full retrospective analysis without replacing the primary workflow's baseline checks.

#### Scenario: Auditing an existing documentation system

- **WHEN** a user requests a documentation audit, information architecture redesign, or documentation repair
- **THEN** the active adapter SHALL invoke or direct the user to its detailed documentation workflow
- **AND** the workflow SHALL still preserve the one-canonical-home rule

#### Scenario: Reviewing accumulated learning

- **WHEN** a user requests a retrospective of a completed change or multiple prior changes
- **THEN** the active adapter SHALL invoke or direct the user to its full evidence and user-question workflow
- **AND** it SHALL not silently apply proposed improvements

### Requirement: Project guidance activates Careful by default
A project adopting Careful SHALL include tracked guidance that activates the primary Careful workflow for substantive product, coding, debugging, and architecture tasks in each installed supported harness. The guidance SHALL have one canonical shared policy source and minimal host-specific entry points.

#### Scenario: Starting substantive work in an adopted project

- **WHEN** a supported harness receives a substantive product, coding, debugging, or architecture request in a project with its Careful adapter installed
- **THEN** the adapter SHALL activate the primary Careful workflow before beginning implementation when its host supports automatic activation
- **AND** it SHALL classify the task as Quick, Standard, or Deep without requiring a Careful command

#### Scenario: Careful is unavailable

- **WHEN** a project contains Careful guidance but a supported harness adapter is not installed, enabled, or verified
- **THEN** the harness SHALL report that the Careful workflow is unavailable or unverified before claiming that Careful controls were applied
- **AND** it MAY follow visible project guidance directly where possible

### Requirement: Final handoff reports automatic checks
The final handoff for a substantive Careful task SHALL state the result of the documentation-impact assessment and the lightweight retrospective assessment when either check was applicable. It SHALL also state any adapter control that was unavailable, degraded, or unverified.

#### Scenario: Normal task with no learning candidate

- **WHEN** a Standard task has documentation impact but no high-signal retrospective event
- **THEN** the final handoff SHALL identify the documentation update or no-impact evidence
- **AND** it SHALL state that no high-signal lesson candidate was created

#### Scenario: Deep task with a candidate improvement

- **WHEN** a Deep task produces an evidence-backed learning candidate
- **THEN** the final handoff SHALL present the candidate, suggested scope, and trade-off
- **AND** it SHALL ask the user to approve, reject, defer, or retarget the proposed improvement
