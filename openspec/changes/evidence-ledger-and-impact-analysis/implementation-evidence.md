# Implementation Evidence: Evidence Ledger and Change-Impact Analysis

## Outcome

Implemented repository-local evidence records, deterministic change-impact analysis, and autonomous assessment routing. Careful now distinguishes routine findings from material user decisions and reports only the latter for interruption.

## Verification

- **Verified:** 60 repository unit tests pass.
- **Verified:** OpenSpec strict validation passes for all 11 current/change items.
- **Verified:** Dependency, specification-authority, public-readiness, and self-hosting validators pass.
- **Verified:** Four Careful skill directories pass the skill validator.
- **Verified:** The complete Codex plugin passes the plugin validator.
- **Verified:** The structural hygiene review executed against Careful and found no AI-slop, duplication, or unused-code candidates; it retained five minor large-file candidates and reported the static-analysis limitation.
- **Verified:** Adopted-project fixtures separately exercise current, stale, unknown, and public-documentation findings.
- **Verified:** Repeated analysis uses sorted paths and findings for deterministic output.
- **Verified:** Git assessment includes tracked, modified, renamed, and untracked paths; explicit project checks execute without shell evaluation and their results satisfy matching material surfaces.
- **Verified:** Evidence freshness is recomputed from observed dates, conflicting source revisions are detected, and private or out-of-root ledger references are rejected.
- **Verified:** Analysis and validation do not mutate source, project documentation, or specifications. The assessment runner writes only its configured private state path so later runs can replace prior task-scoped outcomes.

## Documentation impact

Updated `core/policy.md`, `docs/design.md`, `docs/adoption.md`, `docs/release.md`, `README.md`, `examples/project-profile.yaml`, adapter workflow skills, and the self-hosting profile. Added current OpenSpec capabilities under `openspec/specs/evidence-ledger/` and `openspec/specs/change-impact-analysis/`.

## Review and residual risk

- **Verified:** Local deterministic and structural review passed.
- **Unknown:** Authenticated fresh-session behavioral evidence for Claude Code and Factory Droid remains pending under the existing compatibility contract.
- **Residual risk:** Adapters rely on the adopted project copying the explicitly documented assessment engine scripts; when those scripts are unavailable, the adapter reports degraded coverage instead of claiming autonomous assessment.
- **Unknown:** Static hygiene cannot prove semantic cleanliness or the absence of unused behavior; the five large-file candidates require reviewer judgment.
- **Residual risk:** Path-to-surface matching remains conservative and may require explicit project mappings for custom repository layouts. Unknown and stale findings are surfaced rather than treated as verified.

## Deliberate non-goals

No hosted evidence store, centralized telemetry, automatic project-file migration, numeric trust score, or mandatory ledger for Quick work was added.
