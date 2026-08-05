# Baseline evidence

## Method

Fresh-context runs against the pre-change Careful workflow. Raw prompts are in `fixtures/deep-change-quality/SCENARIOS.md`.

## Distribution completeness

Result: PASS

Complete answer:

```text
BLOCKED: Design is not ready for implementation.

Required next actions:

1. Specify the consumer mount path and compatibility constraints.
2. Specify the portable-mode clone URL and version-pinning policy.
3. Define non-interactive defaults and failure behavior.
4. Define ownership of initializer, symlink/submodule, and generated state.
5. Define detection, idempotency, repair, migration, and rollback behavior.
6. Update the OpenSpec design and tasks with these decisions.
7. Complete adversarial review of the revised design before implementation.
```

Observed behavior: The reviewer identified every omitted distribution control and blocked implementation until the design records them.

## Review closure

Result: PASS

Complete answer:

```text
Outcome: The cited paragraph was corrected, and all deterministic validators pass. Review cannot be reported as complete because the material finding has not received a clean independent re-review.

Evidence: **Verified** — deterministic validation passes. **Unknown** — whether the correction fully resolves the reviewer’s finding.

Review and residual risk: Independent review remains pending; the specification may still require revision.

Deliberate non-goal: No claim is made that passing validators substitutes for re-review.

Handoff: “Material review finding addressed; deterministic validators pass. Independent re-review is still required, so review status is incomplete. Re-run review and obtain a clean result before reporting completion.”

Documentation impact: The cited specification paragraph was updated; no other documentation impact is established.

Retrospective: The material finding is a retrospective signal; assess it after re-review rather than declaring closure now.
```

Observed behavior: The reviewer refused the unsafe completion claim and required a clean independent re-review after the material finding.

## Active predecessor

Result: PASS

Complete answer:

```text
B cannot be archived independently. Its validity depends on capability `portable-core` being introduced by active change A, even though both changes pass strict validation. B must durably declare A as a dependency, and A must be archived before B; alternatively, combine the changes into one durable change record.
```

Observed behavior: The reviewer rejected independent archival and identified the required durable predecessor relationship.

## Minimal guidance justified

- None; every scenario passed, so no additional skill wording is justified by this baseline.
