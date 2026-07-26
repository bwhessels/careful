## ADDED Requirements

### Requirement: Canonical portable workflow contract
Careful SHALL maintain one tracked, versioned portable workflow contract that defines its shared observable behavior: work-depth selection, evidence labels, consequential-decision challenge and blocks, user overrides, documentation impact, independent Deep review, final handoff, and retrospective proposals. Supported adapters SHALL reference this contract rather than maintain independent copies of these policy rules.

#### Scenario: Changing a shared policy rule
- **WHEN** a contributor changes an observable Careful policy rule
- **THEN** the contributor SHALL update the portable workflow contract and affected adapter mappings in the same change
- **AND** the change SHALL include adapter parity validation for every supported adapter

### Requirement: Versioned adapter manifest
Careful SHALL publish a versioned adapter manifest that lists each supported harness, its distribution and project-guidance entry points, explicit-control mapping, automatic-activation behavior, review mechanism, validation command(s), and unsupported controls.

#### Scenario: Selecting an adapter
- **WHEN** a user installs Careful for a supported harness
- **THEN** the adapter documentation SHALL identify the corresponding manifest entry
- **AND** it SHALL state the adapter's verified capability boundary

### Requirement: Capability-aware reporting
An adapter SHALL report a declared unavailable or unverified core control at final handoff and SHALL provide the nearest documented recovery path. An adapter SHALL NOT claim that a control executed without evidence that its host executed it.

#### Scenario: Deep review is unavailable
- **WHEN** a Deep task runs in an adapter whose independent-review mechanism is unavailable
- **THEN** the final handoff SHALL identify independent review as unavailable
- **AND** it SHALL offer the adapter's documented manual or explicit-review recovery path
