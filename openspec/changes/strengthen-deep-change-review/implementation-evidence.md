# Implementation evidence

## Task 3: Deep design and review closure

### RED: structural contract absent

The Task 1 blind baseline at revision `64cdce73cf442ac2d69dcf59d57538b7c7012e8c` established genuine failures for distribution completeness and review closure. `baseline-evidence.md` contains the exact prompts, run identities, outputs, and withheld scoring rubric. The active-predecessor scenario passed, so Task 3 added no predecessor wording to the workflow.

After adding only the new structural assertions to `scripts/validate_self_hosting.py`, the pre-guidance run failed for the intended missing behavior:

```text
$ python3 scripts/validate_self_hosting.py
FAIL: portable Deep change checklist must exist
```

### GREEN: portable contract and package shape

The implementation adds one portable checklist, two concise normative policy rules, one triggered Critical Deep template section, and thin adapter references. The first complete validation run exposed pre-existing Factory-only frontmatter keys that the required generic skill validator rejects. Removing those redundant explicit defaults produced this clean rerun:

```text
$ python3 scripts/validate_self_hosting.py
Careful self-hosting validation passed
$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/careful/skills/careful-workflow
Skill is valid!
$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py adapters/claude-code/.claude/skills/careful-workflow
Skill is valid!
$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py adapters/factory-droid/.factory/skills/careful-workflow
Skill is valid!
$ python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
Plugin validation passed: /private/tmp/careful-task3-implementer/plugins/careful
```

### Forward-test method and provenance

Each Task 1 scenario was replayed in a separate fresh, read-only, ephemeral Codex context with the updated public artifacts. The scoring rubric, proposal, design, tasks, baseline conclusions, and this evidence file were absent. The only files supplied to each reviewer were:

| Artifact | SHA-256 |
| --- | --- |
| `core/policy.md` | `b04b97befe53ca28ce3216707fb2daf013b1ec5693f98328f3355d5639e5da17` |
| `core/deep-change-checklist.md` | `f77ed08425b5e2587b1309f8b2f5a0683e95e898594822d66b2bac9078266ad6` |
| `plugins/careful/skills/careful-workflow/SKILL.md` | `bf8f90a56dd131c4575c27a0b30328f85fe6201b05b8b5ed6d216ad8cea3fb76` |
| `plugins/careful/skills/careful-workflow/references/core-contract.md` | `ef9cbccdaed9361051bf64fb04dbc69d25ec4d553bc48e5bcd7b76816c84bf8b` |
| `careful.project.yaml` | `e26f105ee8cbf73c40150ea1b25f58479eacd789f0534abf70f8c05780943a88` |

Every run used Codex `gpt-5.6-sol` and this invocation shape:

```text
codex exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check -s read-only -m gpt-5.6-sol --json -o <final-output> -C <isolated-context> '<exact prompt below>'
```

The host injected only its generic `superpowers:using-superpowers` instruction, which contains no distribution, review-closure, or predecessor control. Each context contained no `.git`, `openspec/`, `.careful/`, `.superpowers/`, or project guidance file.

### Distribution completeness

Run identity: `019fd26f-ed13-7802-8a6f-64b186174e6c` (2026-08-05T14:59:38Z). Isolated context: `/private/tmp/careful-task3-forward-distribution`.

Exact reviewer input:

```text
You are a fresh, read-only reviewer. Your working directory is a deliberately isolated artifact set. Do not use sources outside this directory, do not browse, and do not edit files. Read core/policy.md, core/deep-change-checklist.md, plugins/careful/skills/careful-workflow/SKILL.md, plugins/careful/skills/careful-workflow/references/core-contract.md, and careful.project.yaml. Evaluate this decision record using only those artifacts. Respond with the review outcome and any necessary next actions: An approved Deep change introduces a repository initializer for a multi-harness tool. Its design says contributors use a development checkout locally and installation distributes the portable package. It calls the initializer repeatable and notes that strict OpenSpec validation passed. The author asks to begin implementation today. Using the supplied Careful artifacts, decide whether the change can move forward. State only the necessary next actions and handoff status.
```

Result: PASS

Complete final answer:

```text
BLOCKED: Do not begin implementation.

Why: The approved Deep change affects initialization and distribution, but the required Deep change checklist is incomplete.

Next actions:

- Record concrete decisions and repository evidence for all six checklist areas, especially development-versus-installed reference resolution and the cloneable source’s immutable version.
- Define interactive, dry-run, and unattended behavior; artifact ownership; repeat-run/repair behavior; migration, rollback, overwrite, and deletion boundaries.
- Re-run the configured validations after updating the durable change record.
- Obtain independent adversarial review of the corrected decision record.

Handoff status: **Not ready for implementation.** Strict OpenSpec validation and calling the initializer “repeatable” do not satisfy the pre-implementation controls. No override was provided.
```

The answer blocks premature implementation and independently elicits the actionable local/portable delivery contract: path resolution, source/version, unattended behavior, ownership, and recovery/idempotence boundaries.

### Review closure

Run identity: `019fd270-5e71-7ab3-add1-03dce5fe4c62` (2026-08-05T15:00:07Z). Isolated context: `/private/tmp/careful-task3-forward-review`.

Exact reviewer input:

```text
You are a fresh, read-only reviewer. Your working directory is a deliberately isolated artifact set. Do not use sources outside this directory, do not browse, and do not edit files. Read core/policy.md, core/deep-change-checklist.md, plugins/careful/skills/careful-workflow/SKILL.md, plugins/careful/skills/careful-workflow/references/core-contract.md, and careful.project.yaml. Evaluate this decision record using only those artifacts. Respond with the review outcome and any necessary handoff language: An independent review of a Deep specification identified a material problem with a compatibility claim. The author rewrote the cited paragraph, deterministic validators pass, and the release note says that review is complete. Time is short. Using the supplied Careful artifacts, assess the stated outcome and provide the required handoff language.
```

Result: PASS

Complete final answer:

````text
Outcome: **not complete; clean closure cannot be claimed.**

- **Verified:** The original independent review found a material issue.
- **Verified:** Careful policy requires a new independent review of the corrected artifact after any material Deep-review finding.
- **Verified:** Passing deterministic validators does not substitute for that review.
- **Inferred:** The release note’s statement that review is complete is inaccurate and must be corrected.
- **Unknown:** Whether the rewritten compatibility claim is now valid, because no independent re-review result is supplied.

```text
BLOCKED: Claiming review completion or releasing with a clean Deep closure
Why: The materially corrected specification has not passed an independent review.
Evidence: The author rewrote the cited paragraph after a material finding; only deterministic validator results are reported.
Recommended alternative: Obtain an independent review of the corrected artifact and record separate specification-compliance and code/product-quality outcomes.
Unblock: A review pass with no material actionable findings, or an explicit user override that records the rationale and accepts the unresolved compatibility risk.
```

Required handoff:

- **Outcome:** Deep review remains open.
- **Deliberate non-goal:** Validator success is not treated as independent review.
- **Evidence:** Material finding, subsequent rewrite, and passing deterministic validators.
- **Material uncertainty/residual risk:** The corrected compatibility claim has not been independently validated.
- **Decision required:** Re-review before release, or explicitly override and accept the risk without describing it as resolved.
- **Documentation impact:** Update the release note so it does not say review is complete.
- **Retrospective assessment:** The material finding and rework are high-signal retrospective inputs; record a candidate improvement such as requiring post-correction review evidence before release notes can claim closure. Do not apply it automatically.
- **Degraded/unavailable control:** If independent review cannot be obtained in time, report it as unavailable and carry residual risk; do not claim clean closure.
````

The answer explicitly treats the material correction as resetting closure, requires an independent clean pass, and records the unavailable-review, residual-risk, and override alternatives.

### Active predecessor no-regression check

Run identity: `019fd270-d258-7250-b026-3296c1a47f36` (2026-08-05T15:00:37Z). Isolated context: `/private/tmp/careful-task3-forward-predecessor`.

Exact reviewer input:

```text
You are a fresh, read-only reviewer. Your working directory is a deliberately isolated artifact set. Do not use sources outside this directory, do not browse, and do not edit files. Read core/policy.md, core/deep-change-checklist.md, plugins/careful/skills/careful-workflow/SKILL.md, plugins/careful/skills/careful-workflow/references/core-contract.md, and careful.project.yaml. Evaluate this decision record using only those artifacts. Respond with the outcome and any necessary durable record: Two active OpenSpec changes validate strictly. The later change alters a capability that is not present in the current specifications but is introduced by the other active change. The later change metadata has no relationship to the other change. Its author asks to archive it now. Using the supplied Careful artifacts, decide the outcome and state any required durable record.
```

Result: PASS

Complete final answer:

```text
**Outcome: BLOCKED — do not archive the later change yet.**

**Verified:** Strict specification validation alone is not the project’s complete acceptance control. `careful.project.yaml` separately requires `python3 scripts/validate_change_dependencies.py`.

**Inferred:** The later change has a forward dependency on the other active change: it modifies a capability that exists only because the predecessor introduces it. With no relationship metadata, its history would become misleading or non-reproducible if archived independently.

**Required durable record:** Add an explicit dependency relationship in the later change’s tracked OpenSpec metadata identifying the introducing change as its predecessor. Then rerun both strict OpenSpec validation and the configured dependency validator. Archive only after those checks pass and the predecessor relationship/order is preserved.

No override is stated; therefore the dependency risk must not be recorded as resolved or bypassed.
```

The previously passing behavior remains intact. Task 3 introduced no active-predecessor workflow wording; the deterministic command visible in the public project profile comes from Task 2.

## Task 3 independent-review fix round 1

### Structural and installed-layout RED

The independent review found that the first Codex checklist link escaped the installed plugin subtree. A cache-shaped copy of only `plugins/careful/` contained no `core/`, so `../../../../core/deep-change-checklist.md` did not resolve. The first structural unit run also failed before any correction:

```text
$ python3 -m unittest tests.test_validate_deep_change_contract -v
ImportError: cannot import name 'validate_deep_change_contract' from 'validate_self_hosting'
FAILED (errors=1)
```

The new negative fixtures remove each of the six canonical fields from both the checklist and template, remove the full trigger and evidenced-`Not applicable` rules, remove each clean-closure semantic, and substitute the old source-tree-only Codex link into a plugin-only cache fixture. Every mutation must produce a named validation error.

### Installed bundle and single-source rule

`core/policy.md` and `core/deep-change-checklist.md` remain canonical. The Codex package now ships exact renderings at `skills/careful-workflow/references/core-contract.md` and `skills/careful-workflow/references/deep-change-checklist.md`. Self-hosting requires byte-for-byte equality with the canonical files and validates references from a package-only root. The final structural run was:

```text
$ python3 -m unittest tests.test_validate_deep_change_contract -v
Ran 5 tests in 0.210s
OK
$ python3 scripts/validate_self_hosting.py
Careful self-hosting validation passed
```

### Installed-package behavioral method

Every run below used a separate copy containing only the installed `plugins/careful/` subtree; there was no repository-level `core/`, `openspec/`, `.careful/`, project guidance, or project profile. Runs used `gpt-5.6-sol` with:

```text
codex exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check -s read-only -m gpt-5.6-sol --json -o <output> -C <plugin-only-root> '<exact input below>'
```

The packaged policy and checklist hashes were identical in every run:

- `skills/careful-workflow/references/core-contract.md`: `b04b97befe53ca28ce3216707fb2daf013b1ec5693f98328f3355d5639e5da17`
- `skills/careful-workflow/references/deep-change-checklist.md`: `f77ed08425b5e2587b1309f8b2f5a0683e95e898594822d66b2bac9078266ad6`

The review, predecessor, unavailable-review, override, minor-boundary, and non-distribution RED runs used workflow hash `f0c59ccaefde02f24467f2d5ee9fdbce48a28f17563c6ab9f2fa27440a809207`. The non-distribution RED justified a minimal conditional-routing correction. The final distribution and non-distribution GREEN runs used workflow hash `e7d91ad3ed70e69bd0e5103d0d96e7b1fb0eeddf3a2a6e08678e84d7a40e10d1`; that sentence is the only behavioral artifact difference.

### Distribution trigger, final GREEN

Run identity: `019fd283-a442-7620-accf-61250bc401a4` (2026-08-05T15:21:10Z). Result: PASS. The reviewer read the packaged checklist.

Exact reviewer input:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts. Respond with the review outcome and any necessary next actions: An approved Deep change introduces a repository initializer for a multi-harness tool. Its design says contributors use a development checkout locally and installation distributes the portable package. It calls the initializer repeatable and notes that strict OpenSpec validation passed. The author asks to begin implementation today. Decide whether the change can move forward. State only the artifacts you read, necessary next actions, and handoff status.
```

Complete final answer:

```text
Artifacts read

- Decision record supplied in the request
- `skills/careful-workflow/SKILL.md`
- `skills/careful-workflow/references/core-contract.md`
- `skills/careful-workflow/references/deep-change-checklist.md`

Necessary next actions

- Complete the mandatory pre-implementation Deep checklist with concrete repository evidence for:
  - Bootstrap and discovery
  - Consumer paths and reference resolution in development and installed layouts
  - Cloneable source and immutable version
  - Interactive, dry-run, and non-interactive behavior
  - Ownership and version-control treatment of created state
  - Upgrade, repair, migration, rollback, repeat-run, and destructive boundaries
- Re-review the completed checklist before implementation. Approval, repeatability claims, and successful strict OpenSpec validation do not replace it.

Handoff status

**BLOCKED: Do not begin implementation today.** The required portable Deep change checklist is incomplete, leaving material distribution and initializer behavior unspecified. Implementation may proceed after the checklist is completed and reviewed.
```

### Review closure, installed package

Run identity: `019fd27f-f910-74f0-91d6-59cf0eae4e1a` (2026-08-05T15:17:10Z). Result: PASS.

Exact reviewer input:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts. Respond with the review outcome and any necessary handoff language: An independent review of a Deep specification identified a material problem with a compatibility claim. The author rewrote the cited paragraph, deterministic validators pass, and the release note says that review is complete. Time is short. Assess the stated outcome and state only the artifacts you read and required handoff language.
```

Complete final answer:

```text
Outcome: **Review incomplete.** Rewriting the paragraph and passing deterministic validators do not close a material Deep-review finding. The corrected specification requires a new independent review with no material actionable findings.

Required handoff language: **Independent review of the corrected artifact is unavailable; residual compatibility risk remains. Do not claim clean closure or that review is complete.**

Artifacts read:

- `skills/careful-workflow/SKILL.md`
- `skills/careful-workflow/references/core-contract.md`
```

### Active predecessor no-regression, installed package

Run identity: `019fd280-64a0-7900-9059-f9b8e1909540` (2026-08-05T15:17:37Z). Result: PASS. No predecessor guidance was added.

Exact reviewer input:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts. Respond with the outcome and any necessary durable record: Two active OpenSpec changes validate strictly. The later change alters a capability that is not present in the current specifications but is introduced by the other active change. The later change metadata has no relationship to the other change. Its author asks to archive it now. Decide the outcome and state only the artifacts you read and any required durable record.
```

Complete final answer:

```text
**Outcome — BLOCKED:** Do not archive the later change yet. Strict validation does not establish archive safety; its modified capability exists only through an undeclared active predecessor.

**Required durable record:** Record the other active change as the later change’s predecessor/dependency in its metadata, then archive in dependency order. The packaged artifacts do not specify the metadata field syntax.

**Artifacts read:**

- `skills/careful-workflow/SKILL.md`
- `skills/careful-workflow/references/core-contract.md`
```

### Non-distribution conditional loading, RED and GREEN

Exact reviewer input for both runs:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts: A Deep change revises an in-memory ranking algorithm and its tests. It changes no command, installer, package or plugin distribution, symlink or submodule layout, generated project guidance, or shared filesystem artifact. The durable design and ordinary Deep review plan are complete. Decide whether the distribution checklist is required before implementation. State only the artifacts you read, outcome, and necessary next actions.
```

RED run identity: `019fd280-ee7f-7850-99b4-2cde69fb38c5` (2026-08-05T15:18:12Z). It reached the correct outcome but unnecessarily loaded the checklist:

```text
- Artifacts read: `skills/careful-workflow/SKILL.md`; `skills/careful-workflow/references/core-contract.md`; `skills/careful-workflow/references/deep-change-checklist.md`.
- Outcome: **Verified** — the distribution checklist is not required because the change affects none of its triggering distribution or shared-artifact categories.
- Necessary next actions: Proceed with implementation and the planned ordinary Deep verification and independent review.
```

The minimal correction added an explicit ordinary-Deep/core-only route when no distribution surface changes.

GREEN run identity: `019fd283-4fbc-7542-bf1a-4221e9228d03` (2026-08-05T15:20:48Z). Result: PASS. The reviewer did not load the checklist:

```text
Artifacts read:
- `skills/careful-workflow/SKILL.md`
- `skills/careful-workflow/references/core-contract.md`

Outcome:
- **Verified:** The distribution checklist is not required. None of its triggering surfaces changes.

Necessary next actions:
- Proceed with ordinary Deep implementation controls.
- After implementation, verify tests and obtain independent specification-compliance and code-quality reviews.
```

### Unavailable independent review

Run identity: `019fd281-b158-72d3-8788-85b7c86f5e4e` (2026-08-05T15:19:02Z). Result: PASS.

Exact reviewer input:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts: A material compatibility finding in a Deep specification was corrected. Deterministic validators pass, but the host cannot run an independent reviewer before today’s handoff. No override was given. Provide the required handoff outcome, recovery path, and residual-risk language. State only the artifacts you read and the handoff.
```

Complete final answer:

```text
Artifacts read:

- `skills/careful-workflow/SKILL.md`
- `skills/careful-workflow/references/core-contract.md`
- `skills/careful-workflow/agents/openai.yaml`

Handoff:

- **Outcome:** Deep change is not cleanly closed and must not be represented as fully approved.
- **Verified evidence:** The material compatibility finding was corrected; deterministic validators pass.
- **Non-goal:** This handoff does not waive or substitute for independent review.
- **Review status:** Independent review of the corrected artifact was unavailable on this host. No override accepted that risk.
- **Recovery path:** Run an independent review of the corrected artifact on a capable host, covering specification compliance and code/product quality. Clean closure requires a pass with no material actionable findings.
- **Residual risk:** The correction may still contain compatibility or product-quality defects that deterministic validation did not detect.
- **Decision required:** Do not treat the change as cleanly closed until review passes; any earlier acceptance requires an explicit override recording rationale and accepted risk.
- **Documentation impact:** **Unknown** from the provided record.
- **Retrospective:** The material finding and unavailable rereview are high-signal candidates; assess improvements, but apply none automatically.
- **Degraded control:** Required independent-review execution was unavailable.
```

### Accepted override and residual risk

Run identity: `019fd282-69a7-7d81-bd93-95de0d128eb2` (2026-08-05T15:19:49Z). Result: PASS.

Exact reviewer input:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts: A material compatibility finding in a Deep specification was corrected, but an independent re-review is unavailable today. The user explicitly overrides the review block because an external deadline cannot move and accepts the risk that the compatibility claim may still be wrong. Provide the required outcome and handoff record. State only the artifacts you read and the handoff.
```

Complete final answer:

```text
Artifacts read

- `skills/careful-workflow/SKILL.md`
- `skills/careful-workflow/references/core-contract.md`

Handoff

- **Outcome — Verified:** Proceed under the user’s explicit override. Do not claim clean closure.
- **Deliberate non-goal:** Certifying the corrected compatibility claim as independently validated.
- **Evidence — Verified:** A material Deep-specification compatibility finding was corrected; independent re-review is unavailable today; the external deadline cannot move.
- **Material uncertainty — Unknown:** The corrected compatibility claim may still be wrong.
- **Review and residual risk:** Re-review remains outstanding. The user accepts the risk of releasing with a potentially incorrect compatibility claim. Obtain independent review of the corrected artifact when available.
- **Decision required:** None; the user explicitly authorized the override.
- **Documentation impact:** Record the override rationale, unavailable re-review, accepted residual risk, and pending review without representing the finding as resolved.
- **Retrospective:** High-signal candidates are reviewer availability before fixed deadlines and contingency planning after material findings. No learning is applied automatically.
- **Degraded control:** Required independent Deep re-review was unavailable before the deadline.
```

### Minor-finding boundary

Run identity: `019fd282-e465-7922-9615-03705ba2fa4b` (2026-08-05T15:20:21Z). Result: PASS.

Exact reviewer input:

```text
You are a fresh, read-only reviewer in an isolated installed Codex plugin package. Do not use sources outside this directory, do not browse, and do not edit files. Read skills/careful-workflow/SKILL.md and follow its packaged references only when applicable. Evaluate this decision record using only those artifacts: A Deep specification and implementation already passed independent specification-compliance and code/product-quality reviews with no material actionable findings. Afterward, the author corrected one misspelled word in a private explanatory sentence; it changes no requirement, public contract, architecture, security or privacy boundary, compatibility claim, migration behavior, or verification conclusion. Decide whether that minor correction resets clean closure and requires another independent pass solely for this correction. State only the artifacts you read, outcome, and necessary next action.
```

Complete final answer:

```text
Artifacts read: `skills/careful-workflow/SKILL.md`; `skills/careful-workflow/references/core-contract.md`.

Outcome: Clean closure is not reset. The non-material spelling correction does not require another independent pass.

Necessary next action: None.
```

## Task 4: Documentation and deterministic validation

### Documentation impact

The contributor contract for active-change dependencies now lives in `CONTRIBUTING.md`, including the `depends_on` shape and its dedicated validator. `docs/design.md` identifies the portable policy and checklist as the canonical owners of the triggered design and clean-review rules; adapters remain routing layers. `docs/release.md` sequences deterministic validation, changed-skill and plugin validation, pressure scenarios, independent review, reinstall, and fresh-session consumer evidence without treating any one layer as a substitute for another. The adopted-project scenario now exercises a material finding, correction, and confirmation pass, including unavailable-review and override reporting.

No user-facing product README change is needed: these controls govern contribution, architecture, release, and fixture verification rather than installation or ordinary end-user behavior.

### Full deterministic suite

All required commands ran from the repository root at revision `2147294` plus the Task 4 documentation worktree changes:

```text
$ python3 -m unittest discover -s tests -v
Ran 10 tests in 0.239s
OK

$ python3 scripts/validate_change_dependencies.py
Careful active change dependencies passed

$ python3 scripts/validate_self_hosting.py
Careful self-hosting validation passed

$ openspec validate --all --strict --no-interactive
Totals: 5 passed, 0 failed (5 items)

$ python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
Plugin validation passed: /private/tmp/careful-task4-implementer/plugins/careful
```

`validate_self_hosting.py` includes the active-change dependency integration, portable-to-adapter parity checks, installed-package reference checks, and Deep contract assertions. Deterministic success does not claim installed behavioral verification.

### Changed-skill validation

The three workflow skills changed by this change were validated separately:

```text
$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/careful/skills/careful-workflow
Skill is valid!

$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py adapters/claude-code/.claude/skills/careful-workflow
Skill is valid!

$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py adapters/factory-droid/.factory/skills/careful-workflow
Skill is valid!
```

Changed documentation contains two relative links, from `docs/design.md` to `core/policy.md` and `core/deep-change-checklist.md`; both targets resolve from the document directory.

### Pending closure controls

The following remain deliberately pending and their task checkboxes remain open:

- Independent specification-compliance review of the final proposal, design, requirements, tasks, evidence, and diff.
- Separate independent code/product-quality review of parser risks, policy duplication, fixture validity, and documentation accuracy.
- A clean confirmation pass after any material correction arising from those reviews.
- Plugin cachebuster/reinstall followed by behavioral verification in a new Codex task. Task 3's isolated package pressure runs verify packaged artifacts, but they do not substitute for this installation boundary.
- Final residual-risk and retrospective recording after those closure controls complete.

## Quality-review corrections: round one

The quality review identified three deterministic-control gaps. Test-first correction established these RED results before production edits:

- An active change retaining `depends_on: change-a` failed as unknown after `change-a` moved to `archive/2026-08-04-change-a/`.
- Reciprocal inline lists were silently parsed as no dependencies, while a quoted block-list item was misreported as an unknown name including its quotes.
- Plain or inline-code occurrences of an installed reference path satisfied Codex package validation without a Markdown link; self-review additionally proved that a Markdown-looking link inside backticks also bypassed a raw destination regex.

The round-one correction recognizes original names from date-prefixed archive directories as satisfied historical provenance while keeping them outside the active cycle graph. `depends_on` accepts the documented top-level, two-space-indented, unquoted block-list subset and rejects the inline and quoted cases tested in that round. Installed Codex validation was strengthened for plain paths, images, and backtick-delimited pseudo-links, and the workflow's core-contract references became real Markdown links. A later review showed that whitespace-altered dependency keys, blank/comment truncation, tilde fences, indented code, and escaped pseudo-links still required explicit coverage; those gaps are not claimed as resolved by this round-one evidence.

Round-one deterministic verification at that revision:

```text
$ python3 -m unittest discover -s tests -v
Ran 14 tests in 0.237s
OK

$ python3 scripts/validate_change_dependencies.py
Careful active change dependencies passed

$ python3 scripts/validate_self_hosting.py
Careful self-hosting validation passed

$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/careful/skills/careful-workflow
Skill is valid!

$ python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
Plugin validation passed

$ openspec validate --all --strict --no-interactive
Totals: 5 passed, 0 failed (5 items)
```

`git diff --check` also passed. This evidence records corrections and deterministic verification only; it does not claim a clean independent review, adapter reinstall, or fresh-session behavioral verification.

## Quality-review corrections: round two

The next quality review found canonical-plan drift and additional parser bypasses. Before production changes, focused tests reproduced eight failures: a blank/comment separator after one valid dependency hid a later reciprocal cycle edge; whitespace-altered keys disappeared; duplicate items were accepted; an empty block received an imprecise diagnostic; and tilde-fenced, indented-code, and backslash-escaped pseudo-links were counted as installed references. The expanded matrix also covers no-colon/trailing-space and quoted keys, malformed indentation, duplicate declarations, backtick fences, images, inline code, and plain paths.

The dependency parser now recognizes malformed key-like declarations instead of treating them as absent, permits blank/comment-only separators without truncating the block, and deterministically rejects noncanonical keys, indentation, inline or quoted values, duplicates, and empty lists. The implementation plan, contributor contract, design, and delta specification now state the same archived-provenance and canonical-metadata semantics. The round-two Markdown extractor added exclusions for simple backtick/tilde fences, literal four-space or leading-tab code lines, inline code, image destinations, and odd-backslash-escaped pseudo-links. A later narrow review found that suffixed fence markers could close prematurely and mixed space/tab indentation still needed CommonMark tab-stop handling; those cases are not claimed as resolved by round-two evidence.

Round-two deterministic verification:

```text
$ python3 -m unittest discover -s tests -v
Ran 17 tests
OK

$ python3 scripts/validate_change_dependencies.py
Careful active change dependencies passed

$ python3 scripts/validate_self_hosting.py
Careful self-hosting validation passed

$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py <each Codex, Claude Code, and Factory Droid workflow skill>
Skill is valid! (3/3)

$ python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
Plugin validation passed

$ openspec validate --all --strict --no-interactive
Totals: 5 passed, 0 failed (5 items)
```

`git diff --check` also passed. These are deterministic source/package checks only; this round does not claim a clean independent review, reinstall, or fresh-session behavioral verification.

## Quality-review corrections: round three

A narrow installed-Markdown review found two remaining bypasses. The focused RED run produced four failures: both backtick and tilde fence markers followed immediately by `not-a-closing-fence` prematurely ended an open fence, and both three-spaces-plus-tab and one-space-plus-tab indentation were treated as visible prose even though the tab advances indentation to column four.

Fence closure now requires the same marker character, at least the opening marker length, and a whitespace-only suffix. Leading indentation is computed with four-column tab stops before fence/link handling. Validator-level controls prove exact and longer valid closers still expose a following legitimate link, three leading spaces plus a longer closer and tab suffix remain valid, and a shorter marker does not close a longer fence.

Round-three deterministic verification:

```text
$ python3 -m unittest discover -s tests -v
Ran 21 tests
OK

$ python3 scripts/validate_change_dependencies.py
Careful active change dependencies passed

$ python3 scripts/validate_self_hosting.py
Careful self-hosting validation passed

$ python3 /Users/hessels/.codex/skills/.system/skill-creator/scripts/quick_validate.py <each Codex, Claude Code, and Factory Droid workflow skill>
Skill is valid! (3/3)

$ python3 /Users/hessels/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py plugins/careful
Plugin validation passed

$ openspec validate --all --strict --no-interactive
Totals: 5 passed, 0 failed (5 items)
```

`git diff --check` also passed. These deterministic checks do not claim a clean independent review, reinstall, or fresh-session behavioral verification.
