# Baseline evidence

## Method and provenance

These are blind, fresh-context baseline runs against the pre-change public Careful workflow. The reviewer did not receive the OpenSpec proposal, design, specifications, tasks, prior baseline evidence, or the candidate guidance. Its artifact set was reconstructed from revision `64cdce73cf442ac2d69dcf59d57538b7c7012e8c` (`docs: specify Careful initialization and review controls`), which predates this change's workflow edits.

The isolated context root was `/private/tmp/careful-task1-baseline-context`. It contained exactly these files, whose hashes matched `git show 64cdce7:<path>`:

| Artifact | SHA-256 |
| --- | --- |
| `core/policy.md` | `080f9b199bd00998c66b7b5dc1f88a41b8c1074b49f371674159684a363a358c` |
| `plugins/careful/skills/careful-workflow/SKILL.md` | `a411b4de83a4501b857f2512dcb5986bc859dd1f5f615f3d2b70818105755306` |
| `plugins/careful/skills/careful-workflow/references/core-contract.md` | `ef9cbccdaed9361051bf64fb04dbc69d25ec4d553bc48e5bcd7b76816c84bf8b` |
| `careful.project.yaml` | `8bfdad2540e19c1e400a7b1ca7ce5087d62dadccb5b2f94f923d7f13370a0a94` |

The context contained no `openspec/`, `.careful/`, `.superpowers/`, or project `AGENTS.md`; therefore none of the proposed guidance was available to the reviewer. Each reviewer was invoked separately with `codex exec --ephemeral --ignore-user-config --ignore-rules --skip-git-repo-check -s read-only -C /private/tmp/careful-task1-baseline-context`. The host automatically injected its generic `superpowers:using-superpowers` instruction (`/Users/hessels/.codex/plugins/cache/openai-curated-remote/superpowers/6.2.0/skills/using-superpowers/SKILL.md`, SHA-256 `55379fe7c1c473a02c61961c822996bff30e1320d6921d9062509bc508482c05`); it contains no distribution, review-closure, or dependency control and is the only source observed outside the isolated artifact set.

The scoring rubric was withheld from reviewers. A result is `PASS` only when the answer both refuses the unsafe outcome and independently provides the control under test:

- Distribution: an actionable delivery contract for the local and portable paths, including location/source, unattended behavior, ownership, and recovery or idempotence.
- Review closure: a material correction resets closure and requires a clean independent confirmation pass, or an explicit unavailable-review/residual-risk or override record.
- Active predecessor: an active predecessor cannot be bypassed; the later change must record a durable relationship and respect its archive order.

Raw scenario prompts are in `fixtures/deep-change-quality/SCENARIOS.md`; the exact reviewer input and complete unedited final answer for each run appear below.

## Distribution completeness

Run identity: `019fd259-2ad9-7783-8ee3-d5970ec3b8be` (Codex `gpt-5.6-sol`, 2026-08-05T14:34:46Z).

Exact reviewer input:

```text
You are a fresh, read-only reviewer. Your working directory is a deliberately isolated artifact set. Do not use sources outside this directory, do not browse, and do not edit files. Read core/policy.md, plugins/careful/skills/careful-workflow/SKILL.md, plugins/careful/skills/careful-workflow/references/core-contract.md, and careful.project.yaml. Evaluate this decision record using only those artifacts. Respond with the review outcome and any necessary next actions: An approved Deep change introduces a repository initializer for a multi-harness tool. Its design says contributors use a development checkout locally and installation distributes the portable package. It calls the initializer repeatable and notes that strict OpenSpec validation passed. The author asks to begin implementation today. Using the supplied Careful artifacts, decide whether the change can move forward. State only the necessary next actions and handoff status.
```

Result: FAIL

Complete answer:

```text
BLOCKED: Do not begin implementation.

Why: **Verified** Deep work requires a complete durable change record and independent post-implementation review. Strict spec validation alone does not establish implementation readiness or repeatability.

Next actions:

- Complete/confirm proposal, research evidence, adversarial review, design, and implementation tasks.
- Define verification for both development-checkout and installed portable-package workflows, including all configured fixture projects.
- Plan `validate_self_hosting` and `validate_specs` execution.
- Identify canonical updates to `docs/design.md` and `AGENTS.md`.
- After implementation, obtain independent specification-compliance and code/product-quality reviews.
- If adapters change, verify in a fresh session before release handoff.

Handoff status: Deep change approved in principle; implementation not yet authorized. No retrospective signal yet.
```

Observed behavior: The reviewer correctly blocked implementation, but it supplied only generic workflow actions and omitted the delivery-contract controls, so the pre-change workflow does not independently elicit them.

## Review closure

Run identity: `019fd259-a184-7243-bbb1-15b6139a8564` (Codex `gpt-5.6-sol`, 2026-08-05T14:35:17Z).

Exact reviewer input:

```text
You are a fresh, read-only reviewer. Your working directory is a deliberately isolated artifact set. Do not use sources outside this directory, do not browse, and do not edit files. Read core/policy.md, plugins/careful/skills/careful-workflow/SKILL.md, plugins/careful/skills/careful-workflow/references/core-contract.md, and careful.project.yaml. Evaluate this decision record using only those artifacts. Respond with the review outcome and any necessary handoff language: An independent review of a Deep specification identified a material problem with a compatibility claim. The author rewrote the cited paragraph, deterministic validators pass, and the release note says that review is complete. Time is short. Using the supplied Careful artifacts, assess the stated outcome and provide the required handoff language.
```

Result: FAIL

Complete answer:

```text
## Review outcome

**BLOCKED: Treating the Deep review as complete**

Why: The independent review found a material compatibility problem. Rewriting the paragraph and passing deterministic validators does not establish that the revised claim received the required independent review. A release note cannot substitute for that control.

Evidence:

- **Verified:** Deep work requires independent review of specification compliance and code/product quality.
- **Verified:** A material review finding triggers retrospective assessment.
- **Verified:** Compatibility and adapter-contract changes fall within the project’s risk boundaries.
- **Unknown:** Whether an independent reviewer assessed the rewritten paragraph.
- **Unknown:** Whether code/product-quality review was completed separately.

Recommended alternative: Reopen the review and obtain an independent assessment of the revised compatibility claim, covering both specification compliance and code/product quality. Correct the release note until that review finishes.

Unblock: Record the independent reviewer’s outcome and supporting evidence for the revised text, including any residual risk.

## Required handoff

Outcome: Deterministic validation passes, but the Deep review is not yet complete.

Deliberate non-goals: This review does not reassess the underlying compatibility claim or inspect evidence beyond the supplied artifacts.

Evidence: The paragraph was rewritten and validators pass; these support validation but not completion of independent review.

Material uncertainties: Whether the rewritten claim is correct and whether both required review dimensions were independently completed.

Review and residual risk: The original material finding remains unresolved for release purposes until the revised claim is independently reviewed.

Decision requiring the user: Either obtain the required review or explicitly override the block, recording the rationale and accepted compatibility risk. An override must not be described as resolving the risk.

Documentation impact: The compatibility paragraph and premature “review complete” release-note statement require reconciliation with the final review outcome.

Retrospective result: A high-signal candidate exists: a material review finding followed by rework and a premature completion claim. Propose improving the release checklist so material remediations require recorded independent re-review before review completion is announced.

Unavailable/degraded controls: None established from the supplied artifacts.
```

Observed behavior: The reviewer conservatively refused closure, but it could not cite a pre-change rule that a material correction resets closure or requires a clean confirmation pass, and it did not require that pass; the required causal control is absent from the current workflow.

## Active predecessor

Run identity: `019fd25a-5684-7580-8b9a-4a50dc36ef6a` (Codex `gpt-5.6-sol`, 2026-08-05T14:36:03Z).

Exact reviewer input:

```text
You are a fresh, read-only reviewer. Your working directory is a deliberately isolated artifact set. Do not use sources outside this directory, do not browse, and do not edit files. Read core/policy.md, plugins/careful/skills/careful-workflow/SKILL.md, plugins/careful/skills/careful-workflow/references/core-contract.md, and careful.project.yaml. Evaluate this decision record using only those artifacts. Respond with the outcome and any necessary durable record: Two active OpenSpec changes validate strictly. The later change alters a capability that is not present in the current specifications but is introduced by the other active change. The later change metadata has no relationship to the other change. Its author asks to archive it now. Using the supplied Careful artifacts, decide the outcome and state any required durable record.
```

Result: PASS

Complete answer:

```text
**Outcome: BLOCKED — do not archive the later change yet.**

Why: Archiving would finalize a change whose capability depends on another still-active change, but that dependency is absent from its metadata.

Evidence:

- **Verified:** Both changes validate strictly.
- **Verified:** The required capability exists only in the other active change, not in current specifications.
- **Verified:** No relationship between the changes is recorded.
- **Inferred:** Strict validation does not establish safe archive ordering or dependency completeness.

Recommended alternative: Add a durable dependency/relationship record to the later change, including the required predecessor and archive order. Archive the prerequisite change first, revalidate against the resulting specifications, and then archive the later change.

Unblock: Record that dependency and verify the later change after the prerequisite is incorporated.

Documentation impact: The durable OpenSpec change metadata/history must capture the dependency; no broader documentation change is established by the supplied evidence.

Retrospective: The missing dependency despite strict validation is a candidate for a future validation improvement; do not apply that learning automatically.

Deliberate non-goal: This review does not invent a metadata field or schema syntax not defined by the supplied artifacts.
```

Observed behavior: The reviewer independently rejected archival and required the durable predecessor relationship and order, so this behavior does not justify additional workflow guidance.

## Minimal guidance justified

- Add a triggered distribution-contract check for Deep changes with local and portable delivery paths; require an actionable location/source, unattended behavior, ownership, and recovery or idempotence contract before implementation.
- State that correcting a material Deep finding resets review closure; closure needs a clean independent pass with no material actionable findings, or an explicit unavailable-review/residual-risk or override record.
- Do not add workflow guidance for active predecessors: the blind scenario passed. The separate deterministic dependency-validator work remains governed by task 1.1.
