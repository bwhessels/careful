# Implementation Evidence: Unify Specification Authority

## Outcome

Implemented the authority-resolution contract, non-destructive duplicate detection, profile fields, portable policy guidance, adapter guidance, self-hosting fixture profile, and SBX consumer migration.

## Verification

- `python3 -m unittest discover -s tests -v` — 30 tests passed.
- `python3 scripts/validate_spec_authority.py` — passed for Careful.
- `python3 scripts/validate_spec_authority.py /Users/hessels/projects/sbx-session-evidence-collector` — passed for SBX consumer.
- `python3 scripts/validate_self_hosting.py` — passed.
- `openspec validate --changes` — 5 active changes passed.
- Skill validators passed for all changed Careful and adapter skills.
- Plugin validator passed for `plugins/careful`.
- SBX `npm test` — 36 tests passed.
- SBX `npm run openspec:validate` — 2 changes passed.
- `git diff --check` passed in both repositories.

The validator preserved the historical privacy retrospective while classifying it as non-authoritative context. No file migration or deletion was performed automatically.

## Documentation impact

Updated Careful’s portable policy, design, adoption, release, README, project profile, skills, adapter guidance, fixtures, and OpenSpec change records. Updated the SBX project profile and guidance to declare OpenSpec as the sole durable specification authority and marked the retained retrospective as historical.

## Review and residual risk

The independent review command was unavailable. The sandbox blocked in-process reviewer initialization, and the elevated retry was rejected because it would transmit the uncommitted Careful repository to an unspecified external reviewer. Deterministic validation and local self-review passed, but this does not constitute an independent clean review. Clean review, any material corrections, and archival remain open.
