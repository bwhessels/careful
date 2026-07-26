## ADDED Requirements

### Requirement: Factory Droid project entry point
Careful SHALL provide a tracked Factory Droid adapter that uses documented `AGENTS.md` guidance and `.factory/skills/` discovery paths. The adapter SHALL reference the portable workflow contract rather than duplicate it.

#### Scenario: Droid opens an adopted project
- **WHEN** Factory Droid starts in a project adopted with the Careful Factory adapter
- **THEN** the project guidance SHALL identify Careful as the default workflow for substantive work
- **AND** the adapter SHALL make baseline and specialist skills discoverable through Factory's documented project skill layout

### Requirement: Factory explicit controls and review mapping
The Factory Droid adapter SHALL document the Droid skill or custom-droid mapping for each Careful explicit control and for independent Deep review. Where model invocation is unsuitable for a side-effecting control, the adapter SHALL require explicit user invocation.

#### Scenario: Triggering an explicit Deep review
- **WHEN** a Factory user requests a Careful Deep review
- **THEN** the adapter SHALL invoke or direct the user to the documented read-only review skill or custom droid
- **AND** the final handoff SHALL include its result or an evidence-based unavailability notice

### Requirement: Factory capability verification
The Factory Droid adapter SHALL document its supported Droid version assumptions, cite official Factory documentation for project guidance, skills, and any custom droids used, and include fresh-session consumer fixture validation.

#### Scenario: Updating Factory adapter behavior
- **WHEN** a change affects Factory Droid skill discovery, custom-droid use, or explicit-control mapping
- **THEN** maintainers SHALL validate the affected Factory fixture in a fresh Droid session
- **AND** record any unsupported or degraded control in the adapter compatibility matrix
