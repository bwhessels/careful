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
