# Design: Evidence Ledger and Change-Impact Analysis

## Recommended design

Add two portable capabilities:

- `evidence-ledger` defines a change-scoped collection of consequential claim records. Each record has a stable identifier, claim, classification, evidence references, scope, freshness or checked date when relevant, and optional links to OpenSpec requirements, tasks, files, or review findings.
- `change-impact-analysis` defines a deterministic report over changed paths and project configuration. It maps affected paths to likely capabilities and validation surfaces, labels each mapping as verified or inferred, and reports missing or unresolved follow-up without mutating project files.

The ledger is authoritative only for the record of what the agent or reviewer asserted and cited. OpenSpec remains authoritative for requirements, design decisions, tasks, and history. Careful owns the assessment of ledger and impact findings: it evaluates their significance, feeds material outcomes back into workflow routing and verification, and presents the user only with prioritized findings requiring judgment, authorization, or unresolved external evidence. The impact report is advisory as a raw artifact, but its assessed outcomes participate in workflow decisions according to portable policy and project configuration.

## Boundaries and interfaces

### Evidence record

The portable logical shape is:

```yaml
id: claim-001
claim: "The Codex adapter activates the baseline workflow in a fresh consumer session."
classification: Verified
evidence:
  - kind: fixture
    ref: fixtures/adopted-project/codex
    observed: 2026-08-30
scope:
  paths: [plugins/careful/, fixtures/adopted-project/codex/]
  adapters: [codex]
links:
  requirements: [cross-harness-adoption]
status: current
```

Required fields are `id`, `claim`, `classification`, and at least one `evidence` item for `Verified` or `Inferred` claims. `Assumption` and `Unknown` records may use an empty evidence list but must include a reason or unresolved question. Implementations may serialize this shape as YAML or Markdown, provided the fields remain inspectable and project-owned configuration identifies the location.

Evidence kinds should include at least repository path, command result, test/fixture, review, and external source. External sources must retain a URL or equivalent reference and checked date when available. Records must not contain secrets or private `.careful/` content unless the project explicitly permits that local-only use.

### Impact report

The report accepts:

- changed paths or a repository diff;
- the project profile;
- the declared specification authority;
- current and active OpenSpec capabilities when available;
- adapter-manifest and fixture mappings when available.

It emits affected paths, matched capabilities, affected documentation and validation surfaces, mapping classification, evidence references, and unresolved follow-up. A report must distinguish:

- `verified` — directly matched by explicit project configuration or a canonical manifest;
- `inferred` — matched by a documented convention or conservative path rule;
- `unknown` — insufficient evidence to map the change.

The report must identify at least these surfaces when applicable: durable specification, execution plan, public documentation, adapter distribution, consumer fixture, project checks, and independent review. It may recommend a surface without claiming that an update is required unless a project rule or OpenSpec requirement establishes that obligation.

### Autonomous assessment loop

After generating ledger and impact findings, Careful SHALL assess each finding and assign an actionable state:

- `satisfied` — evidence and follow-up are sufficient; continue;
- `needs-verification` — Careful adds or runs an appropriate check;
- `stale` — Careful schedules or performs revalidation before relying on the claim;
- `contradiction` — conflicting evidence requires investigation and may escalate or block;
- `user-decision-needed` — the finding requires owner judgment, authorization, or an external action unavailable to Careful;
- `accepted-risk` — an authorized override records residual exposure without treating it as resolved.

The assessment SHALL feed back into the workflow. Material `needs-verification`, `stale`, or `contradiction` findings SHALL add verification work or escalate the task depth when the risk boundary requires it. A `user-decision-needed` finding SHALL be summarized as a concise user flag with the evidence, consequence, recommended options, and unblock action. Careful SHALL not require the user to manually audit all records before continuing when no material decision is present.

Careful SHALL retain assessment outcomes for the current task so later checks, reviews, and the final handoff use the latest known state. It SHALL re-assess findings after new evidence, corrections, overrides, or material changes to the diff.

### User-facing finding triage

User flags SHALL be prioritized by materiality and limited to findings that affect safety, public claims, compatibility, irreversible decisions, release readiness, or a decision reserved to the project owner. Informational findings MAY be retained in the task evidence without interrupting the user. A final handoff SHALL summarize unresolved and decision-worthy findings rather than emit an undigested ledger or impact report.

### Configuration

Add optional project-owned configuration for ledger and impact behavior. The first implementation should support a ledger location, enabled impact checks, explicit path-to-surface mappings, and whether unresolved unknown mappings fail a configured gate. Absent configuration means the capabilities can report findings but must not silently impose new repository artifacts on consumers.

## Consequences and reversibility

The design adds inspectable local artifacts and deterministic reports, plus an autonomous assessment loop. Existing projects can adopt it incrementally because the ledger and impact configuration are optional. Records can be deleted or regenerated by project owners, while OpenSpec and source files remain unchanged. The main irreversible risk is Careful silently accepting incomplete mappings; assessments therefore require explicit uncertainty, conservative escalation for material findings, and no claim of exhaustive coverage without evidence.

## Documentation impact

Update the portable policy, project-profile example, workflow/adoption guidance, release guidance, adapter manifest guidance if report capabilities differ, and the current OpenSpec capability specifications after implementation. Add validator and fixture documentation describing the boundary between source-repository evidence and consumer-session evidence.

## Related decisions

- Builds on the evidence classifications in `core/policy.md`.
- Builds on specification authority in the `unify-spec-authority` capability.
- Complements active-change dependency validation; it does not replace it.
- Builds on adapter and fixture mappings introduced by `multi-harness-adapters`.
- Preserves the private `.careful/` boundary from `self-hosting-careful`.
