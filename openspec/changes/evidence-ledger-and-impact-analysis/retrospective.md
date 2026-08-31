# Retrospective: Evidence Ledger and Change-Impact Analysis

## Observations and evidence

- A self-hosting validator integration initially referenced an uninitialized local variable; the fixture tests passed but the repository validator exposed the integration defect.
- A bundled portable policy copy failed its exact-render check after policy behavior changed; the existing validator caught the synchronization requirement.
- The first autonomous triage implementation treated routine `needs-verification` findings as user interruptions; focused tests and the intended workflow clarified that verification should be automatic whenever possible.

## Candidate learning

### Candidate: Add an assessment fixture to the standard workflow-contract checklist

- Scope: project-level Careful workflow.
- Smallest change: require one fixture that proves routine findings continue automatically and one that proves material findings become user flags.
- Benefit: catches accidental escalation or user-interruption regressions earlier.
- Trade-off: adds a small amount of fixture maintenance to future workflow changes.
- Confidence: high, based on the triage correction during this change.
- Validation condition: the fixture fails if a routine `needs-verification` state is surfaced as a user flag.

This candidate is recorded for user approval; it is not applied automatically.

