# Adversarial Review: Evidence Ledger and Change-Impact Analysis

## Material risks

1. **False completeness:** A ledger can make weak evidence look authoritative. Mitigation: records must preserve source references, classification, scope, and freshness; reviewers still inspect evidence.
2. **Specification duplication:** A ledger could accidentally become a second requirements store. Mitigation: claims and impact findings link to, but do not define, OpenSpec requirements or project specifications.
3. **Heuristic noise:** Filename-based impact detection may produce excessive warnings. Mitigation: distinguish verified mappings from inferred candidates and allow project-owned mappings.
4. **Workflow burden:** Requiring records for trivial work would undermine proportionality. Mitigation: require ledger and impact enforcement only when configured or when Standard/Deep work has consequential claims or affected public/contract surfaces.
5. **Host inconsistency:** Adapters may not expose identical diff or filesystem capabilities. Mitigation: define a portable report format and require adapters to report unavailable inputs rather than claim complete analysis.

## Recommendation

Proceed with a repository-local, report-oriented contract. Keep recording and analysis separate: the evidence ledger answers “what supports this claim?”, while impact analysis answers “what may this change affect?”. Make both explainable, non-destructive, and capability-aware.

