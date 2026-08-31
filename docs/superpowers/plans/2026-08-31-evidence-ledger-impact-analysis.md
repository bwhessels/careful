# Autonomous Evidence and Impact Assessment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement repository-local evidence records, deterministic change-impact analysis, and autonomous assessment that routes verification and flags only material user decisions.

**Architecture:** Keep pure assessment logic in `scripts/careful_assessment.py`, with focused parsers and deterministic JSON-compatible result shapes. Expose read-only command-line entry points for ledger validation, impact analysis, and combined assessment. Integrate the commands into the Careful workflow guidance and validate them against source and adopted-project fixtures.

**Tech Stack:** Python 3 standard library, unittest, Markdown/YAML-shaped project configuration, Git diff metadata.

**Spec:** `openspec/changes/evidence-ledger-and-impact-analysis/`

## Global Constraints

- OpenSpec remains the sole durable specification authority.
- Quick work remains free of mandatory ledger creation.
- Unknown, stale, and contradictory findings must not be presented as verified.
- Analysis is read-only and must not read or write `.careful/`.
- Reports must be deterministic for identical inputs.
- Existing validators and fixtures must continue to pass.

### Task 1: Define portable assessment data and configuration

**Files:**
- Create: `scripts/careful_assessment.py`
- Test: `tests/test_careful_assessment.py`
- Modify: `examples/project-profile.yaml`
- Modify: `careful.project.yaml`

**Interfaces:**
- `EvidenceRecord`, `EvidenceReference`, `ImpactFinding`, and `AssessmentFinding` dataclasses.
- `load_project_assessment_config(path: Path) -> dict[str, object]`.
- `assessment_state_for(kind: str, material: bool, satisfied: bool, stale: bool, contradiction: bool, user_action: bool) -> str`.

- [ ] Write failing tests for parsing optional `assessment:` configuration, all action states, and JSON-serializable result records.
- [ ] Run `python3 -m unittest tests.test_careful_assessment -v`; expect import or assertion failures because the module is absent.
- [ ] Implement the dataclasses and strict small-subset configuration parser.
- [ ] Run the focused tests and the existing suite; expect all to pass.
- [ ] Commit `feat: define assessment records and states`.

### Task 2: Implement evidence ledger storage and validation

**Files:**
- Modify: `scripts/careful_assessment.py`
- Create: `scripts/validate_evidence_ledger.py`
- Modify: `tests/test_careful_assessment.py`
- Create: `tests/test_validate_evidence_ledger.py`

**Interfaces:**
- `parse_evidence_ledger(path: Path) -> list[EvidenceRecord]`.
- `validate_evidence_ledger(root: Path, ledger_path: Path | None = None) -> dict[str, object]`.
- CLI `python3 scripts/validate_evidence_ledger.py [root]`.

- [ ] Add failing tests for valid records, missing evidence/reason, duplicate IDs, unsupported kinds/classifications, malformed references, and `.careful/` exclusion.
- [ ] Run the focused tests and confirm feature-specific failures.
- [ ] Implement a deterministic Markdown-free YAML subset parser for the documented ledger shape, with record-scoped diagnostics.
- [ ] Implement the CLI with stable sorted diagnostics and exit code 1 on validation failure.
- [ ] Run focused and full tests.
- [ ] Commit `feat: validate evidence ledger records`.

### Task 3: Implement deterministic change-impact analysis

**Files:**
- Modify: `scripts/careful_assessment.py`
- Create: `scripts/analyze_change_impact.py`
- Create: `tests/test_change_impact.py`

**Interfaces:**
- `collect_changed_paths(root: Path, diff_file: Path | None = None) -> tuple[list[str], list[str]]`.
- `analyze_change_impact(root: Path, changed_paths: Sequence[str]) -> dict[str, object]`.
- CLI `python3 scripts/analyze_change_impact.py [root] [--paths ...] [--diff-file ...]`.

- [ ] Add failing tests for explicit mappings, adapter manifest mappings, OpenSpec paths, public documentation, inferred matches, unknown mappings, unavailable diff input, and stable ordering.
- [ ] Run focused tests and confirm expected failures.
- [ ] Implement path matching from project configuration, canonical repository paths, adapter manifest, fixtures, and conservative conventions.
- [ ] Emit verified/inferred/unknown mappings with evidence sources and required versus advisory follow-up.
- [ ] Implement read-only CLI input handling and deterministic JSON/text output.
- [ ] Run focused and full tests.
- [ ] Commit `feat: add deterministic change impact analysis`.

### Task 4: Integrate autonomous assessment and workflow routing

**Files:**
- Modify: `scripts/careful_assessment.py`
- Create: `scripts/assess_careful.py`
- Create: `tests/test_assess_careful.py`
- Modify: `plugins/careful/skills/careful-workflow/SKILL.md`
- Modify: adapter workflow skill copies under `adapters/`

**Interfaces:**
- `assess_findings(ledger_result: dict, impact_result: dict, depth: str) -> dict[str, object]`.
- `prioritize_user_flags(findings: Sequence[AssessmentFinding]) -> list[dict[str, object]]`.
- `run_assessment(root: Path, depth: str, changed_paths: Sequence[str] | None = None) -> dict[str, object]`.
- CLI `python3 scripts/assess_careful.py [root] [--depth quick|standard|deep] [--paths ...]`.

- [ ] Add failing tests for satisfied findings, verification follow-up, stale/contradictory escalation, user-decision-needed flags, accepted-risk recording, and concise handoff summaries.
- [ ] Run focused tests and confirm failures.
- [ ] Implement materiality rules, routing decisions, task-scoped result retention in the generated report only, and non-interactive user flags.
- [ ] Wire the workflow guidance to invoke assessment at start, after material changes, and before final handoff; state that only material flags interrupt the user.
- [ ] Run focused and full tests.
- [ ] Commit `feat: integrate autonomous Careful assessment`.

### Task 5: Add fixtures and verification coverage

**Files:**
- Create: `fixtures/adopted-project/evidence-ledger.yaml`
- Create: `fixtures/adopted-project/assessment-fixture.yaml`
- Create: `tests/test_assessment_fixtures.py`
- Modify: `scripts/validate_self_hosting.py`
- Modify: `careful.project.yaml`

**Interfaces:**
- Fixture validation calls the same public parser and assessment functions as the CLI.
- Self-hosting validation reports source and consumer fixture evidence separately.

- [ ] Add failing fixture tests for current, stale, contradictory, unknown, and user-decision-needed records.
- [ ] Run fixture tests and confirm failures.
- [ ] Add representative fixture inputs and self-hosting checks without reading private context.
- [ ] Run all configured validators, OpenSpec validation, and full unit tests.
- [ ] Commit `test: cover autonomous assessment fixtures`.

### Task 6: Integrate documentation and release handoffs

**Files:**
- Modify: `core/policy.md`
- Modify: `docs/design.md`
- Modify: `docs/adoption.md`
- Modify: `docs/release.md`
- Modify: `README.md`
- Modify: `examples/project-profile.yaml`
- Modify: `openspec/changes/evidence-ledger-and-impact-analysis/tasks.md`

- [ ] Add canonical documentation for autonomous assessment, user flags, residual risk, and non-destructive behavior.
- [ ] Update release guidance with ledger/impact commands and separate fixture evidence.
- [ ] Mark only evidence-backed OpenSpec tasks complete.
- [ ] Run documentation/link and repository checks.
- [ ] Commit `docs: document autonomous assessment workflow`.

### Task 7: Independent review and closure evidence

**Files:**
- Create: `openspec/changes/evidence-ledger-and-impact-analysis/implementation-evidence.md`
- Create: `openspec/changes/evidence-ledger-and-impact-analysis/retrospective.md`
- Modify: `openspec/changes/evidence-ledger-and-impact-analysis/tasks.md`

- [ ] Run independent specification and product-quality review using the project’s available review mechanism.
- [ ] Correct material findings and run clean re-review if needed.
- [ ] Record verification, documentation impact, residual risk, and retrospective assessment.
- [ ] Run the complete release validation suite.
- [ ] Archive the OpenSpec change only after all required evidence exists.
- [ ] Commit `chore: close evidence and impact assessment change`.

