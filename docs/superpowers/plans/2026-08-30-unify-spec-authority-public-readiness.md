# Unify Specification Authority and Public-Readiness Gates Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make OpenSpec-or-project-declared specification authority explicit, detect duplicate durable specifications, and enforce configurable public-readiness checks across Careful and its adopted projects.

**Architecture:** Careful will add a small standard-library validator that reads the project profile, checks authority/plan configuration, and reports competing durable specification paths without mutating them. Portable policy and skills will route durable artifacts through the declared authority, while project-specific checks and an independent reviewer remain separate concerns. The SBX consumer will declare OpenSpec authority and retain only OpenSpec changes plus linked execution plans.

**Tech Stack:** Python 3 standard library, Markdown/YAML project artifacts, Careful portable policy and Codex plugin skills, OpenSpec, existing self-hosting fixtures.

**Spec:** `openspec/changes/unify-spec-authority/` and `openspec/changes/add-public-readiness-gates/`

## Global Constraints

- OpenSpec is the sole durable specification authority for Careful and the SBX consumer.
- Execution plans remain under `docs/superpowers/plans/` and must link to the canonical specification.
- Do not create or maintain a parallel durable specification under `docs/superpowers/specs/` when OpenSpec is declared.
- Duplicate detection is non-destructive; no file is deleted, overwritten, archived, or merged without explicit owner direction.
- Project-specific public documents, checks, licenses, privacy decisions, and support promises remain project-owned.
- Validate every changed Careful skill with the skill-creator validator and the distributable Codex plugin with the plugin-creator validator.
- Preserve unrelated changes already present in both worktrees.

---

### Task 1: Define and test project-profile authority parsing

**Files:**
- Create: `/Users/hessels/projects/careful/scripts/validate_spec_authority.py`
- Create: `/Users/hessels/projects/careful/tests/test_validate_spec_authority.py`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-adopt/references/project-profile.md`

**Interfaces:**
- `parse_documentation_profile(path: Path) -> dict[str, object]`
- `find_specification_conflicts(root: Path, profile: dict[str, object]) -> list[str]`
- `validate_spec_authority(root: Path) -> list[str]`

- [ ] **Step 1: Write failing tests for supported authority modes**

Add fixtures asserting that `openspec`, `project-defined`, `none`, and absent authority are distinguished, that `execution_plans` is parsed, and that malformed authority values fail with a concrete error.

- [ ] **Step 2: Run the focused test and verify the expected failure**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest tests.test_validate_spec_authority -v`

Expected: test import or missing-function failures because the validator does not exist yet.

- [ ] **Step 3: Implement minimal standard-library profile parsing**

Parse only the documented `documentation:` block and its scalar/list fields. Return `authority: unknown` when the key is absent, reject unsupported values, and report malformed indentation rather than partially interpreting it.

- [ ] **Step 4: Run the focused tests and verify green**

Run the same unittest command. Expected: all profile-mode and malformed-profile tests pass.

### Task 2: Add non-destructive duplicate specification detection

**Files:**
- Modify: `/Users/hessels/projects/careful/scripts/validate_spec_authority.py`
- Modify: `/Users/hessels/projects/careful/tests/test_validate_spec_authority.py`

**Interfaces:**
- `looks_like_durable_spec(path: Path) -> bool`
- `is_explicit_pointer_or_history(path: Path) -> bool`
- `find_specification_conflicts(root: Path, profile: dict[str, object]) -> list[str]`

- [ ] **Step 1: Write failing tests for conflict and exemption cases**

Cover an OpenSpec project containing a durable Markdown file in `docs/superpowers/specs/`, a pointer document, a historical document, a valid execution plan, a project-defined authority, and a project with no authority.

- [ ] **Step 2: Run the focused tests and verify they fail for missing detection**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest tests.test_validate_spec_authority -v`

Expected: conflict assertions fail because detection is not implemented.

- [ ] **Step 3: Implement conservative detection**

Treat a Markdown file as durable-looking only when it is under a configured competing spec path or `docs/superpowers/specs/` and contains specification/design language such as `Status`, `Goals`, `Requirements`, `Decisions`, or `Non-goals`. Exempt files explicitly marked `historical`, `pointer`, or containing a canonical-spec link. Report path, declared authority, and owner-action requirement; never mutate files.

- [ ] **Step 4: Run focused tests and full validator tests**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest tests.test_validate_spec_authority -v && python3 -m unittest discover -s tests -v`

Expected: all validator tests pass.

### Task 3: Integrate authority checks into Careful validation and policy

**Files:**
- Modify: `/Users/hessels/projects/careful/scripts/validate_self_hosting.py`
- Modify: `/Users/hessels/projects/careful/core/policy.md`
- Modify: `/Users/hessels/projects/careful/docs/design.md`
- Modify: `/Users/hessels/projects/careful/careful.project.yaml`
- Modify: `/Users/hessels/projects/careful/tests/test_validate_self_hosting.py` if present; otherwise add focused integration tests to `tests/test_validate_spec_authority.py`

- [ ] **Step 1: Add failing integration assertions**

Assert that self-hosting validation invokes the authority validator and that Careful’s own profile declares `spec_authority: openspec` and `execution_plans: docs/superpowers/plans/`.

- [ ] **Step 2: Run the integration test and verify the expected failure**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest discover -s tests -v`

Expected: the new integration assertion fails before integration/configuration is added.

- [ ] **Step 3: Integrate the validator into self-hosting validation**

Import `validate_spec_authority`, invoke it from `validate_self_hosting.py`, and surface each returned error. Keep the validator independent from OpenSpec’s own schema validator.

- [ ] **Step 4: Update the normative policy and design ownership table**

State that the project profile resolves durable specification authority before planning, OpenSpec is canonical when declared, execution plans link to it, and duplicate detection is non-destructive. Update `docs/design.md` so OpenSpec remains the durable owner and plans are execution artifacts.

- [ ] **Step 5: Run self-hosting validation and focused tests**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest discover -s tests -v && python3 scripts/validate_self_hosting.py`

Expected: tests and self-hosting validation pass.

### Task 4: Update distributed skills and fixture guidance

**Files:**
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-workflow/SKILL.md`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-documentation/SKILL.md`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-adopt/SKILL.md`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-adopt/references/project-profile.md`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-adopt/references/project-guidance.md`
- Modify: `/Users/hessels/projects/careful/fixtures/adopted-project/AGENTS.md`
- Modify: `/Users/hessels/projects/careful/fixtures/adopted-project/README.md`
- Modify: `/Users/hessels/projects/careful/fixtures/adopted-project/codex/AGENTS.md`
- Modify: `/Users/hessels/projects/careful/fixtures/adopted-project/claude-code/AGENTS.md`
- Modify: `/Users/hessels/projects/careful/fixtures/adopted-project/factory-droid/AGENTS.md`
- Modify: `/Users/hessels/projects/careful/fixtures/adopted-project/careful.project.yaml` if present, otherwise add it as part of the fixture profile

- [ ] **Step 1: Update workflow guidance**

Add authority resolution before creating durable specs, distinguish execution plans, require canonical links, and require duplicate-conflict reporting. Keep the normative rule concise and link to the portable policy.

- [ ] **Step 2: Update adoption/profile guidance**

Document `documentation.spec_authority` and `documentation.execution_plans`, including `unknown` handling and explicit owner decisions. Do not require OpenSpec for projects that choose another authority.

- [ ] **Step 3: Update adopted-project fixtures**

Declare OpenSpec authority in the fixture and add a scenario showing that a plan links to OpenSpec while `docs/superpowers/specs/` is not a second source of truth.

- [ ] **Step 4: Run skill and plugin validators**

Run the repository’s skill-creator validator against each changed skill and the plugin-creator validator against `plugins/careful`. Expected: no validation errors.

### Task 5: Implement configurable public-readiness checks and reviewer guidance

**Files:**
- Create: `/Users/hessels/projects/careful/scripts/validate_public_readiness.py`
- Create: `/Users/hessels/projects/careful/tests/test_validate_public_readiness.py`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-workflow/SKILL.md`
- Modify: `/Users/hessels/projects/careful/plugins/careful/skills/careful-documentation/SKILL.md`
- Modify: `/Users/hessels/projects/careful/core/policy.md`
- Modify: `/Users/hessels/projects/careful/docs/design.md`

**Interfaces:**
- `parse_public_readiness(path: Path) -> dict[str, object]`
- `validate_public_readiness(root: Path) -> dict[str, object]`

- [ ] **Step 1: Write failing tests for audience modes and required artifacts**

Cover `private`, `internal`, `public-intended`, and `public`; missing required documents; configured command presence; invalid configuration; and a passing result shape with `status`, `mode`, `checked_documents`, `failed_checks`, and `warnings`.

- [ ] **Step 2: Run focused tests and verify failure**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest tests.test_validate_public_readiness -v`

Expected: missing-module or missing-function failures.

- [ ] **Step 3: Implement minimal project-configured verifier**

Parse the project-owned `public_readiness` block, resolve required paths, validate configured command declarations without executing arbitrary commands from the shared validator, and return the standard result shape. Leave command execution to the project’s own CI/task command.

- [ ] **Step 4: Run focused tests and full Python tests**

Run: `cd /Users/hessels/projects/careful && python3 -m unittest tests.test_validate_public_readiness -v && python3 -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 5: Add reviewer and release-gate guidance**

Document that mechanical checks cover objective invariants while independent review covers semantic drift, public claims, limitations, privacy/security communication, license, support, disclosure, and publication decisions. Require whole-repository review for first publication and configured releases, with explicit overrides and residual risk.

### Task 6: Migrate and validate the SBX consumer

**Files:**
- Modify: `/Users/hessels/projects/sbx-session-evidence-collector/careful.project.yaml`
- Modify: `/Users/hessels/projects/sbx-session-evidence-collector/AGENTS.md`
- Modify: `/Users/hessels/projects/sbx-session-evidence-collector/README.md` if needed to link the authority rule
- Create or modify: `/Users/hessels/projects/sbx-session-evidence-collector/docs/superpowers/plans/2026-08-30-unify-spec-authority-public-readiness.md` only if an execution plan is needed

- [ ] **Step 1: Verify the consumer has no durable duplicate spec**

Run: `cd /Users/hessels/projects/sbx-session-evidence-collector && find docs/superpowers/specs -type f -print` and confirm no durable spec remains.

- [ ] **Step 2: Validate the consumer authority declaration**

Run: `cd /Users/hessels/projects/sbx-session-evidence-collector && npm run openspec:validate && npm test`

Expected: OpenSpec validation and existing tests pass.

- [ ] **Step 3: Add a canonical link from any execution plan**

Ensure each changed `docs/superpowers/plans/` document names its OpenSpec source. Do not duplicate requirements or design decisions in the plan.

- [ ] **Step 4: Run final cross-repository checks**

Run Careful OpenSpec validation, self-hosting validation, all Python tests, changed skill/plugin validators, SBX OpenSpec validation, SBX tests, and `git diff --check` in both repositories.

### Task 7: Independent review and evidence

**Files:**
- Modify: `/Users/hessels/projects/careful/openspec/changes/unify-spec-authority/tasks.md`
- Modify: `/Users/hessels/projects/careful/openspec/changes/add-public-readiness-gates/tasks.md`
- Create: implementation evidence records under the corresponding Careful OpenSpec changes
- Modify: Careful current specifications only after implementation is accepted

- [ ] **Step 1: Obtain independent specification-compliance review**

Check each requirement for authority resolution, non-destructive conflict handling, plan separation, project-specific public-readiness configuration, mechanical checks, reviewer gates, and explicit owner decisions.

- [ ] **Step 2: Obtain independent code/product-quality review**

Review parser ambiguity, false-positive duplicate detection, command execution boundaries, fixture coverage, adapter parity, and consumer migration safety.

- [ ] **Step 3: Correct material findings and obtain a clean confirmation pass**

Do not claim clean closure until the corrected artifact receives a pass with no material actionable findings.

- [ ] **Step 4: Record evidence and documentation impact**

Include exact verification commands, changed canonical documents, residual risks, and the retrospective assessment before closing or archiving the changes.

## Plan self-review

- Covers both approved OpenSpec changes and the SBX consumer migration.
- Separates the durable authority fix from the public-readiness capability.
- Uses TDD for new validators and keeps project command execution outside shared validation.
- Preserves non-destructive behavior and explicit owner decisions.
- Contains no unresolved `TODO`, `TBD`, or placeholder implementation steps.
