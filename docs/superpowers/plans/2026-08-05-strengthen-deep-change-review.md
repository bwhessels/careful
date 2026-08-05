# Strengthen Deep Change Review Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the three approved Careful retrospective lessons: active-change dependency validation, a triggered CLI/distribution design checklist, and a clean independent re-review gate after material Deep findings.

**Architecture:** Keep mechanically derivable OpenSpec relationships in a standard-library validator called by self-hosting validation. Keep normative judgment rules in the portable core policy and Critical Deep template, with Codex/Claude/Factory workflow skills remaining thin host adapters. Validate the skill behavior with baseline and forward pressure scenarios, then require a clean independent review of the complete change.

**Tech Stack:** Python 3 standard library, `unittest`, Markdown/YAML OpenSpec artifacts, Codex/Claude/Factory skill Markdown, existing Careful validation scripts.

## Global Constraints

- Do not read or modify `.careful/`; it is private maintainer context.
- Do not add a runtime Python or YAML dependency.
- `multi-harness-adapters` must be synced and archived before this change is archived or released.
- Normative shared behavior lives in `core/policy.md`; adapter skills stay thin.
- Run a failing test or baseline pressure scenario before production code or skill edits.
- A material correction resets the review gate; closure requires one clean independent pass or an explicit residual-risk/override record.

---

### Task 1: Baseline behavioral evidence

**Files:**
- Create: `fixtures/deep-change-quality/SCENARIOS.md`
- Create: `openspec/changes/strengthen-deep-change-review/baseline-evidence.md`
- Modify: `openspec/changes/strengthen-deep-change-review/tasks.md`

**Interfaces:**
- Consumes: Current `core/policy.md`, current `careful-workflow` skill, and raw scenario prompts.
- Produces: Three reproducible scenario definitions and verbatim baseline outcomes used to justify the minimal skill wording.

- [ ] **Step 1: Write three raw pressure scenarios**

Create `fixtures/deep-change-quality/SCENARIOS.md` with these scenarios, without including the intended answers:

```markdown
# Deep change quality scenarios

## Distribution completeness

An approved Deep change introduces a repository initializer for a multi-harness tool. Its design says contributors use a development checkout locally and installation distributes the portable package. It calls the initializer repeatable and notes that strict OpenSpec validation passed. The author asks to begin implementation today. Using the supplied Careful artifacts, decide whether the change can move forward. State only the necessary next actions and handoff status.

## Review closure

An independent review of a Deep specification identified a material problem with a compatibility claim. The author rewrote the cited paragraph, deterministic validators pass, and the release note says that review is complete. Time is short. Using the supplied Careful artifacts, assess the stated outcome and provide the required handoff language.

## Active predecessor

Two active OpenSpec changes validate strictly. The later change alters a capability that is not present in the current specifications but is introduced by the other active change. The later change's metadata has no relationship to the other change. Its author asks to archive it now. Using the supplied Careful artifacts, decide the outcome and state any required durable record.
```

- [ ] **Step 2: Run each scenario in an isolated fresh context without the proposed guidance**

For each raw scenario, create a separate ephemeral, read-only reviewer context from one exact pre-change revision. Include only the public `core/policy.md`, checked-in `careful-workflow` skill and its direct core-contract reference, and `careful.project.yaml`. Do not include an OpenSpec change, its plan, prior baseline evidence, scoring rubric, or any candidate guidance. Record the source revision; every included path and hash; the exact reviewer input; session/run identity and runtime; any automatic host instruction observed; and the complete unedited reviewer output. Prove the proposed guidance was excluded by recording the isolated context file list. Do not mention the expected omission or approved candidate to the reviewer.

- [ ] **Step 3: Verify the RED state**

Record `PASS` only when the current workflow both identifies the missing rule and refuses the unsafe completion claim. At least one scenario must fail for the approved skill change to proceed. If all pass, stop and retain only the mechanical validator candidate.

- [ ] **Step 4: Record baseline evidence**

Create `baseline-evidence.md` with this structure. For each scenario, write the literal result `PASS` or `FAIL`, then include the complete reviewer answer in a fenced block and identify the exact omission or rationalization in one sentence:

```markdown
# Baseline evidence

## Method and provenance

For each reviewer run, record the exact pre-change revision, isolated artifact list and hashes, complete reviewer input, session/run identity, runtime, any automatic host instruction observed, and the complete unedited output. State how the isolated context excludes the OpenSpec change, its plan, prior evidence, scoring rubric, and proposed guidance. Raw prompts are in `fixtures/deep-change-quality/SCENARIOS.md`.

## Distribution completeness

Result: write PASS or FAIL from the scoring rule.

Complete answer: include the unedited reviewer output in a fenced text block.

Observed behavior: identify the specific required control found or omitted.

## Review closure

Use the same three fields and scoring rule.

## Active predecessor

Use the same three fields and scoring rule.

## Minimal guidance justified

- List only rules supported by a failing baseline.
```

- [ ] **Step 5: Mark task 2.1 and/or 3.1 complete only when evidence exists**

Update the OpenSpec task checkboxes corresponding to the actual scenarios run.

- [ ] **Step 6: Commit the baseline evidence**

```bash
git add fixtures/deep-change-quality/SCENARIOS.md openspec/changes/strengthen-deep-change-review/baseline-evidence.md openspec/changes/strengthen-deep-change-review/tasks.md
git commit -m "test: capture deep change review baselines"
```

### Task 2: Active-change dependency validator

**Files:**
- Create: `tests/test_validate_change_dependencies.py`
- Create: `scripts/validate_change_dependencies.py`
- Modify: `scripts/validate_self_hosting.py`
- Modify: `openspec/changes/add-project-initializer/.openspec.yaml`
- Modify: `careful.project.yaml`

**Interfaces:**
- Produces: `validate_change_dependencies(root: pathlib.Path) -> list[str]`, returning deterministic human-readable errors.
- Produces: CLI `python3 scripts/validate_change_dependencies.py [root]`, exit `0` with a success line or exit `1` with one line per error.
- Consumes: `openspec/specs/<capability>/spec.md`, active `openspec/changes/<name>/proposal.md`, and optional `.openspec.yaml` `depends_on` lists.

- [ ] **Step 1: Write the failing unit tests**

Create `tests/test_validate_change_dependencies.py` using `unittest` and temporary repositories. Cover these literal behaviors:

```python
def test_requires_provider_when_modified_capability_is_not_current(self):
    root = self.fixture(
        current=(),
        changes={
            "change-a": {"new": ("portable-core",)},
            "change-b": {"modified": ("portable-core",)},
        },
    )
    self.assertEqual(
        validate_change_dependencies(root),
        ["change-b modifies non-current capability portable-core; declare depends_on: change-a"],
    )

def test_accepts_declared_provider(self):
    root = self.fixture(
        current=(),
        changes={
            "change-a": {"new": ("portable-core",)},
            "change-b": {
                "modified": ("portable-core",),
                "depends_on": ("change-a",),
            },
        },
    )
    self.assertEqual(validate_change_dependencies(root), [])

def test_rejects_unknown_self_and_cycle_dependencies(self):
    cases = (
        (
            {"change-a": {"depends_on": ("missing-change",)}},
            ["change-a declares unknown dependency missing-change"],
        ),
        (
            {"change-a": {"depends_on": ("change-a",)}},
            ["change-a declares a dependency on itself"],
        ),
        (
            {
                "change-a": {"depends_on": ("change-b",)},
                "change-b": {"depends_on": ("change-a",)},
            },
            ["dependency cycle: change-a -> change-b -> change-a"],
        ),
    )
    for changes, expected in cases:
        with self.subTest(expected=expected):
            self.assertEqual(
                validate_change_dependencies(self.fixture(current=(), changes=changes)),
                expected,
            )

def test_current_capability_requires_no_predecessor(self):
    root = self.fixture(
        current=("portable-core",),
        changes={"change-b": {"modified": ("portable-core",)}},
    )
    self.assertEqual(validate_change_dependencies(root), [])
```

The fixture helper must write real proposal headings and `.openspec.yaml` files; it must not mock parser functions.

- [ ] **Step 2: Run the dependency tests and verify RED**

Run:

```bash
python3 -m unittest tests.test_validate_change_dependencies -v
```

Expected: import failure for `scripts.validate_change_dependencies` because production code does not exist.

- [ ] **Step 3: Implement the minimal parser and graph validation**

Create `scripts/validate_change_dependencies.py` with the exact public signatures `parse_capabilities(proposal: Path) -> tuple[set[str], set[str]]`, `parse_dependencies(metadata: Path) -> tuple[str, ...]`, `validate_change_dependencies(root: Path) -> list[str]`, and `main(argv: list[str] | None = None) -> int`.

Parse only `### New Capabilities`, `### Modified Capabilities`, and backticked bullet identifiers. Parse only a top-level `depends_on:` followed by two-space-indented `- <change-name>` values. Ignore `archive/`. Return errors sorted lexically. Detect unknown dependencies, self-dependencies, cycles, and missing providers for non-current modified capabilities.

- [ ] **Step 4: Run the unit tests and verify GREEN**

Run:

```bash
python3 -m unittest tests.test_validate_change_dependencies -v
```

Expected: all dependency tests pass.

- [ ] **Step 5: Integrate with self-hosting validation**

Import `validate_change_dependencies` in `scripts/validate_self_hosting.py`, call it from `main()`, and fail with all returned errors before printing the success line. Add `validate_change_dependencies: python3 scripts/validate_change_dependencies.py` under `commands:` in `careful.project.yaml`.

- [ ] **Step 6: Apply the convention to the initializer**

Add to `openspec/changes/add-project-initializer/.openspec.yaml`:

```yaml
depends_on:
  - multi-harness-adapters
```

- [ ] **Step 7: Run integration validation**

Run:

```bash
python3 scripts/validate_change_dependencies.py
python3 scripts/validate_self_hosting.py
openspec validate --all --strict --no-interactive
```

Expected: all three commands exit `0`; the first prints `Careful active change dependencies passed`.

- [ ] **Step 8: Commit the validator**

```bash
git add tests/test_validate_change_dependencies.py scripts/validate_change_dependencies.py scripts/validate_self_hosting.py careful.project.yaml openspec/changes/add-project-initializer/.openspec.yaml
git commit -m "feat: validate active OpenSpec dependencies"
```

### Task 3: Triggered design checklist and clean review gate

**Files:**
- Create: `core/deep-change-checklist.md`
- Modify: `core/policy.md`
- Modify: `examples/openspec-schemas/critical-deep/templates/design.md`
- Modify: `plugins/careful/skills/careful-workflow/SKILL.md`
- Modify: `adapters/claude-code/.claude/skills/careful-workflow/SKILL.md`
- Modify: `adapters/factory-droid/.factory/skills/careful-workflow/SKILL.md`
- Modify: `scripts/validate_self_hosting.py`

**Interfaces:**
- Produces: One portable checklist reference loaded only for qualifying Deep distribution changes.
- Produces: One material-finding review-closure rule shared by all adapters.
- Consumes: Baseline failures recorded in Task 1; do not add guidance for scenarios that already passed.

- [ ] **Step 1: Add a failing structural validation assertion**

Extend `scripts/validate_self_hosting.py` expectations only after a baseline failure justifies the guidance. The validator must require `core/deep-change-checklist.md`, require the Critical Deep design template to contain `## Distribution contract`, and require each workflow adapter to reference the portable policy/checklist rather than duplicate the six checklist fields.

- [ ] **Step 2: Run self-hosting validation and verify RED**

Run:

```bash
python3 scripts/validate_self_hosting.py
```

Expected: failure naming the missing checklist/template contract.

- [ ] **Step 3: Write the minimal portable checklist**

Create `core/deep-change-checklist.md` with a trigger paragraph and six required fields: bootstrap/discovery; consumer path/reference resolution; cloneable source/version; interaction defaults; tracked/local/private state; upgrade/repair/migration/rollback. Each field accepts a concrete decision or a `Not applicable` statement followed by concrete repository evidence.

- [ ] **Step 4: Update normative portable policy**

In `core/policy.md`, add two concise rules:

```markdown
For a Deep change affecting commands, installation, distribution, generated project guidance, or shared filesystem artifacts, complete [the Deep change checklist](deep-change-checklist.md) before implementation.

After correcting a material Deep review finding, obtain an independent review of the corrected artifact. Claim clean closure only after a pass with no material actionable findings; otherwise report unavailable review, residual risk, or an accepted override.
```

- [ ] **Step 5: Add the structural design slots**

Append this triggered section to the Critical Deep design template:

```markdown
## Distribution contract

Include this section only for commands, initializers, installers, packaging, generated guidance, or shared filesystem artifacts. Complete every field with a decision or a `Not applicable` statement followed by concrete repository evidence.

- Bootstrap and discovery:
- Consumer path and reference resolution:
- Cloneable source and immutable version:
- Interactive, dry-run, and non-interactive defaults:
- Tracked, ignored, local, and private state:
- Upgrade, repair, migration, rollback, and destructive boundaries:
```

- [ ] **Step 6: Keep adapter skills thin**

Update the Codex workflow skill to load `core/deep-change-checklist.md` only when the trigger applies and to enforce the clean-pass gate. Update Claude and Factory workflow skills to reference the portable policy/checklist and their existing independent reviewer; do not copy the six checklist fields into adapter skills.

- [ ] **Step 7: Run structural validation and skill validators**

Run:

```bash
python3 scripts/validate_self_hosting.py
python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/careful/skills/careful-workflow
python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py adapters/claude-code/.claude/skills/careful-workflow
python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py adapters/factory-droid/.factory/skills/careful-workflow
python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
```

Expected: all commands exit `0`.

- [ ] **Step 8: Forward-test the pressure scenarios**

Run every Task 1 scenario in a fresh context with the updated skill. Record complete outputs in `openspec/changes/strengthen-deep-change-review/implementation-evidence.md`. The distribution and review-closure scenarios must now pass. If a new rationalization appears, make the smallest wording correction and rerun that scenario.

- [ ] **Step 9: Commit the workflow controls**

```bash
git add core/policy.md core/deep-change-checklist.md examples/openspec-schemas/critical-deep/templates/design.md plugins/careful/skills/careful-workflow/SKILL.md adapters/claude-code/.claude/skills/careful-workflow/SKILL.md adapters/factory-droid/.factory/skills/careful-workflow/SKILL.md scripts/validate_self_hosting.py openspec/changes/strengthen-deep-change-review/implementation-evidence.md
git commit -m "feat: strengthen Deep design and review closure"
```

### Task 4: Documentation, complete validation, and independent closure

**Files:**
- Modify: `docs/design.md`
- Modify: `docs/release.md`
- Modify: `CONTRIBUTING.md`
- Modify: `fixtures/adopted-project/SCENARIO.md`
- Modify: `openspec/changes/strengthen-deep-change-review/tasks.md`
- Modify: `openspec/changes/strengthen-deep-change-review/implementation-evidence.md`

**Interfaces:**
- Consumes: Implemented validator and workflow controls from Tasks 2–3.
- Produces: Canonical contributor/release guidance, fixture coverage, and clean independent review evidence.

- [ ] **Step 1: Update canonical documentation**

Document `.openspec.yaml` `depends_on` and the validator command in `CONTRIBUTING.md`; document checklist ownership and clean review closure in `docs/design.md`; add dependency, skill/plugin, pressure-scenario, and clean-pass checks to `docs/release.md`; update the adopted-project scenario to include a material-finding confirmation pass.

- [ ] **Step 2: Run the full deterministic suite**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_change_dependencies.py
python3 scripts/validate_self_hosting.py
openspec validate --all --strict --no-interactive
python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
```

Expected: zero failures and clean exit for every command.

- [ ] **Step 3: Validate every changed skill**

Run `quick_validate.py` separately against each changed skill folder. Record the exact commands and exit results in `implementation-evidence.md`.

- [ ] **Step 4: Obtain independent specification-compliance review**

Give a fresh reviewer the proposal, design, requirements, tasks, and final diff. Ask only whether every approved candidate is implemented and evidenced. Correct every material finding and rerun this review until one pass has no material actionable findings.

- [ ] **Step 5: Obtain independent code/product-quality review**

Give a separate fresh reviewer the final diff and test outputs. Ask for parser correctness, false-positive/negative risks, skill duplication, fixture validity, and documentation accuracy. Correct material findings and rerun until clean or record residual risk/override.

- [ ] **Step 6: Complete implementation evidence and task state**

Record outcome, RED/GREEN evidence, full validation, documentation impact, reviewer identities/results, residual risk, deliberate non-goals, and retrospective result. Mark only evidence-backed task checkboxes complete.

- [ ] **Step 7: Commit documentation and evidence**

```bash
git add docs/design.md docs/release.md CONTRIBUTING.md fixtures/adopted-project/SCENARIO.md openspec/changes/strengthen-deep-change-review
git commit -m "docs: record Deep change quality controls"
```

- [ ] **Step 8: Reinstall boundary for Codex behavioral verification**

After all source validation passes, use the plugin-creator cachebuster/reinstall flow for the local Careful plugin, then start a new Codex task before claiming the updated Codex skill behavior is verified. Do not edit marketplace files manually.
