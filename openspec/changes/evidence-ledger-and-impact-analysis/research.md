# Research: Evidence Ledger and Change-Impact Analysis

## Repository evidence

- **Verified:** `core/policy.md` requires the classifications `Verified`, `Inferred`, `Assumption`, and `Unknown` for consequential claims.
- **Verified:** `plugins/careful/skills/careful-workflow/SKILL.md` requires documentation-impact assessment and a final handoff, but does not define a machine-readable evidence or impact artifact.
- **Verified:** `careful.project.yaml` identifies OpenSpec as the specification authority, `docs/superpowers/plans/` as the execution-plan location, and separate source, adapter, and fixture validation commands.
- **Verified:** `core/adapter-manifest.yaml` maps supported adapters to distribution paths, controls, validation, and fixtures.
- **Verified:** `scripts/validate_change_dependencies.py` already analyzes active OpenSpec change capabilities and dependencies, but its purpose is dependency correctness rather than complete file-to-surface impact analysis.
- **Verified:** `scripts/validate_spec_authority.py` detects competing durable-looking specifications without mutating them.
- **Verified:** `docs/release.md` requires separate source, skill, adapter, fixture, fresh-session, documentation, and review evidence.

## Design implications

- **Inferred:** The ledger should be additive and link to canonical artifacts; it must not become a parallel specification authority.
- **Inferred:** Impact analysis should produce explainable findings with evidence paths and confidence labels instead of opaque scores.
- **Assumption:** Initial impact rules can combine explicit project-profile mappings, OpenSpec capability identifiers, known adapter/fixture paths, and conservative path heuristics.

## Open questions retained for implementation

- Whether the ledger is stored as one change-scoped file, multiple records, or a project-configured location.
- Which path-to-capability mappings should be explicit in `careful.project.yaml` versus inferred from convention.
- How hosts provide a diff when the workflow is not running inside a Git checkout.

