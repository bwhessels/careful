## ADDED Requirements

### Requirement: Claude Code project entry point
Careful SHALL provide a tracked Claude Code adapter that exposes a `CLAUDE.md` project entry point importing the shared `AGENTS.md` guidance and adds only Claude-specific activation guidance. The Claude entry point SHALL NOT duplicate the portable workflow contract.

#### Scenario: Claude Code opens an adopted project
- **WHEN** Claude Code starts in a project adopted with the Careful Claude adapter
- **THEN** Claude Code SHALL load the adapter's `CLAUDE.md` entry point
- **AND** the entry point SHALL import the shared Careful project guidance

### Requirement: Claude Code skill mapping
The Claude Code adapter SHALL package the Careful baseline and specialist workflows as documented Claude skills or plugins and SHALL map explicit Careful controls to their Claude Code invocation path.

#### Scenario: User explicitly requests a retrospective
- **WHEN** a Claude Code user requests a Careful retrospective
- **THEN** the adapter documentation SHALL identify the Claude skill or fallback that performs the full retrospective workflow
- **AND** the workflow SHALL preserve user approval before applying a proposed improvement

### Requirement: Claude Code capability verification
The Claude Code adapter SHALL document its supported Claude Code version assumptions, cite official Claude documentation for its entry-point and skill mechanisms, and include a fresh-session consumer fixture validation.

#### Scenario: Releasing the Claude adapter
- **WHEN** the Claude Code adapter is released or its activation semantics change
- **THEN** maintainers SHALL run the Claude fixture in a fresh Claude Code session
- **AND** the release evidence SHALL distinguish verified behavior from any unverified host behavior
