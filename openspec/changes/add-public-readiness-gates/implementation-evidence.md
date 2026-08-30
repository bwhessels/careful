# Implementation Evidence: Project-Specific Public-Readiness Gates

## Outcome

Implemented the project-profile public-readiness schema example, a standard-library mechanical verifier, portable policy guidance, reviewer guidance, release/adoption documentation, and self-hosting tests.

## Verification

- `python3 -m unittest discover -s tests -v` — 30 tests passed.
- `python3 scripts/validate_public_readiness.py` — passed for Careful with mode `unknown` because Careful has not declared a publication audience.
- `python3 scripts/validate_public_readiness.py /Users/hessels/projects/sbx-session-evidence-collector` — passed with a warning because the SBX consumer has not yet declared a public-readiness audience or required artifact set.
- `python3 scripts/validate_self_hosting.py` — passed.
- `openspec validate --changes` — 5 active changes passed.
- Skill validators passed for all changed Careful and adapter skills.
- Plugin validator passed for `plugins/careful`.
- `git diff --check` passed in both repositories.

The verifier intentionally checks objective project-owned configuration and artifact presence only; it does not execute arbitrary project commands or decide license, privacy, security-disclosure, support, or publication policy.

## Documentation impact

Updated Careful’s portable policy, project-profile example, design ownership documentation, README, adoption guide, release guide, reviewer guidance, fixtures, and OpenSpec change records.

## Review and residual risk

The independent review command was unavailable. The sandbox blocked in-process reviewer initialization, and the elevated retry was rejected because it would transmit the uncommitted Careful repository to an unspecified external reviewer. Deterministic validation and local self-review passed, but this does not constitute an independent clean review. Clean review, any material corrections, and archival remain open.
