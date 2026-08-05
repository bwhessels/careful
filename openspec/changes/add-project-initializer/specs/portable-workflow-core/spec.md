## MODIFIED Requirements

### Requirement: Canonical portable workflow contract
Careful SHALL maintain one tracked, versioned portable workflow contract that defines its shared observable behavior: work-depth selection, evidence labels, consequential-decision challenge and blocks, user overrides, documentation impact, independent Deep review, final handoff, and retrospective proposals. Supported adapters SHALL reference this contract rather than maintain independent copies of these policy rules. Consumer projects initialized by Careful SHALL resolve that contract through the common source root `vendor/careful/core/policy.md` in both linked and portable modes.

#### Scenario: Changing a shared policy rule
- **WHEN** a contributor changes an observable Careful policy rule
- **THEN** the contributor SHALL update the portable workflow contract and affected adapter mappings in the same change
- **AND** the change SHALL include adapter parity validation for every supported adapter

#### Scenario: Consuming the portable contract from an initialized project
- **WHEN** Careful initializes project guidance or a host adapter shim
- **THEN** the generated artifact SHALL resolve shared policy through `vendor/careful/core/policy.md`
- **AND** it SHALL not duplicate normative policy prose
- **AND** consumer validation SHALL fail when the reference does not resolve in the selected source mode
