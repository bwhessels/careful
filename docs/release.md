# Releasing Careful

1. Run `python3 -m unittest discover -s tests -v`, `python3 scripts/validate_change_dependencies.py`, `python3 scripts/validate_self_hosting.py`, and `openspec validate --all --strict --no-interactive`.
2. Run `python3 scripts/validate_spec_authority.py` and `python3 scripts/validate_public_readiness.py` for the project being released. Resolve or explicitly record any authority conflict; do not treat a passing mechanical check as semantic public-readiness approval.
3. Run the skill validator separately for every changed skill directory, then validate the complete Codex plugin with the plugin validator.
4. Run static validation for every adapter and compare it against `core/adapter-manifest.yaml`.
5. For changed workflow guidance, record the blind baseline and fresh-context forward pressure scenarios in the change evidence.
6. Obtain independent specification-compliance and code/product-quality reviews. If a material finding is corrected, repeat independent review until one pass has no material actionable findings, or record the unavailable pass, override, and residual risk without claiming clean closure.
7. Install or reinstall each changed adapter using its documented installation boundary.
8. Start a new session in every affected host before evaluating updated skills. Existing sessions retain already-loaded instruction context and cannot prove the new behavior.

The adopted-project fixture variants are consumer checks. They must be validated separately from source-repository checks whenever shared policy, adapter behavior, skill triggers, schemas, or installation guidance changes. Do not release an adapter as verified until its fresh-session fixture evidence is recorded. Passing deterministic, skill, and plugin validators proves structure; it does not replace pressure scenarios, independent review, reinstall, or fresh-session consumer evidence.

For `public-intended` and `public` projects, the release owner must also complete the configured whole-repository public-readiness gate. Missing required artifacts or failed project checks block the gate; semantic, legal, privacy, security, support, and publication decisions require explicit owner or independent-review evidence.
