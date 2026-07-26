# Careful Default Skill Integration Specification

## Purpose

Define how Careful applies its baseline workflow automatically in a Codex project while retaining specialist skills for detailed documentation and retrospective work.
## Requirements
### Requirement: Main workflow owns baseline checks

The `careful-workflow` skill SHALL contain the baseline documentation-impact and retrospective-signal checks required for normal Careful work. The baseline checks SHALL run without requiring the user to invoke a documentation or retrospective command.

#### Scenario: Completing a behavior-affecting task

- **WHEN** Careful completes a task that changes behavior, a public contract, architecture, configuration, operations, or contributor workflow
- **THEN** `careful-workflow` SHALL assess documentation impact before finalizing the task
- **AND** it SHALL update the canonical public document or report an evidence-based no-impact conclusion

#### Scenario: Completing work with a learning signal

- **WHEN** a task includes a block, override, material review finding, failed verification, repeated rework, or direct durable user correction
- **THEN** `careful-workflow` SHALL perform a lightweight retrospective assessment before finalizing the task
- **AND** it SHALL report either no high-signal lesson candidates or the proposed candidate improvements

### Requirement: Specialist skills provide depth

The `careful-documentation` and `careful-retrospective` skills SHALL remain separate Codex skills. They SHALL provide detailed workflows for dedicated documentation work and full retrospective analysis without replacing the baseline checks in `careful-workflow`.

#### Scenario: Auditing an existing documentation system

- **WHEN** a user requests a documentation audit, information architecture redesign, or documentation repair
- **THEN** Codex SHALL use `careful-documentation` for the detailed workflow
- **AND** the workflow SHALL still preserve the one-canonical-home rule

#### Scenario: Reviewing accumulated learning

- **WHEN** a user requests a retrospective of a completed change or multiple prior changes
- **THEN** Codex SHALL use `careful-retrospective` for the full evidence and user-question workflow
- **AND** it SHALL not silently apply proposed improvements

### Requirement: Project guidance activates Careful by default

A project adopting Careful SHALL include tracked Codex guidance that instructs Codex to use `careful-workflow` as the default workflow for substantive product, coding, debugging, and architecture tasks when the Careful plugin is installed.

#### Scenario: Starting substantive work in an adopted project

- **WHEN** Codex receives a substantive product, coding, debugging, or architecture request in a project with Careful guidance and the Careful plugin installed
- **THEN** Codex SHALL use `careful-workflow` before beginning implementation
- **AND** it SHALL classify the task as Quick, Standard, or Deep without requiring a Careful command

#### Scenario: Careful is unavailable

- **WHEN** a project contains Careful guidance but the Careful plugin is not installed or enabled
- **THEN** Codex SHALL report that the workflow skill is unavailable before claiming that Careful controls were applied
- **AND** it MAY follow the visible project guidance directly where possible

### Requirement: Final handoff reports automatic checks

The final handoff for a substantive Careful task SHALL state the result of the documentation-impact assessment and the lightweight retrospective assessment when either check was applicable.

#### Scenario: Normal task with no learning candidate

- **WHEN** a Standard task has documentation impact but no high-signal retrospective event
- **THEN** the final handoff SHALL identify the documentation update or no-impact evidence
- **AND** it SHALL state that no high-signal lesson candidate was created

#### Scenario: Deep task with a candidate improvement

- **WHEN** a Deep task produces an evidence-backed learning candidate
- **THEN** the final handoff SHALL present the candidate, suggested scope, and trade-off
- **AND** it SHALL ask the user to approve, reject, defer, or retarget the proposed improvement

