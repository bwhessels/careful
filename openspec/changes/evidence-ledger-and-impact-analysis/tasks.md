## Implementation

- [x] 1. Add current OpenSpec capabilities for `evidence-ledger` and `change-impact-analysis` using the requirements in this change.
- [x] 2. Define and validate the portable evidence-record schema, including classification, evidence kinds, scope, freshness, links, and private-context handling.
- [x] 3. Implement repository-local ledger discovery and report generation without mutating project-owned files.
- [x] 4. Implement changed-path ingestion and deterministic impact mapping from project configuration, OpenSpec capabilities, adapter manifest, fixtures, and documented conventions.
- [x] 5. Add explicit uncertainty and unavailable-capability reporting; ensure unknown mappings are not presented as verified impact.
- [x] 6. Implement the autonomous assessment loop and actionable finding states, including routing into verification, escalation, blocking, user flags, and accepted-risk handling.
- [x] 7. Add prioritized user-facing finding triage and task-scoped assessment state so users are not required to manually audit every record.
- [x] 8. Add optional `careful.project.yaml` configuration and preserve proportional behavior when the configuration is absent.

## Verification

- [x] 9. Add unit tests for valid/invalid ledger records, missing evidence, stale records, duplicate identifiers, secret/private-context boundaries, and unknown classifications.
- [x] 10. Add unit tests for verified, inferred, and unknown impact mappings, changed paths spanning multiple surfaces, absent project configuration, malformed mappings, and deterministic report ordering.
- [x] 11. Add tests for every assessment state, feedback into depth/verification, materiality-based user flags, accepted-risk recording, re-assessment after new evidence, and concise final-handoff triage.
- [x] 12. Add adopted-project fixtures covering OpenSpec, project-defined, and no specification authority, plus Codex, Claude Code, and Factory Droid adapter surfaces where applicable.
- [x] 13. Run OpenSpec validation, repository tests, dependency/spec-authority/public-readiness/self-hosting validators, and changed skill/plugin validators.
- [x] 14. Record separate source-repository and consumer-fixture evidence, including fresh-session evidence for any affected adapter.

## Documentation

- [x] 15. Update `core/policy.md`, `docs/design.md`, `README.md`, adoption/release guidance, and the project-profile example.
- [x] 16. Document that Careful autonomously assesses findings and flags only decision-worthy items, while the ledger remains evidence metadata rather than a specification authority and impact analysis is not exhaustive without verified mappings.
- [x] 16.1. Add structural-hygiene review checks and reviewer guidance for complexity, AI filler, duplication, unused candidates, oversized files, cohesion, and behavior-focused tests.

## Independent review

- [ ] 17. Obtain independent Deep review of the specification and implementation, covering false completeness, autonomous-routing errors, missed user flags, duplicate authority, heuristic noise, privacy boundaries, host degradation, and proportionality.
- [ ] 18. After any material correction, obtain a clean independent re-review and record residual risk or an explicit override if clean review is unavailable.
