# Releasing Careful

1. Run `python3 -m unittest discover -s tests -v`, `python3 scripts/validate_change_dependencies.py`, `python3 scripts/validate_self_hosting.py`, and `openspec validate --all --strict --no-interactive`.
2. Run the skill validator separately for every changed skill directory, then validate the complete Codex plugin with the plugin validator.
3. Run static validation for every adapter and compare it against `core/adapter-manifest.yaml`.
4. For changed workflow guidance, record the blind baseline and fresh-context forward pressure scenarios in the change evidence.
5. Obtain independent specification-compliance and code/product-quality reviews. If a material finding is corrected, repeat independent review until one pass has no material actionable findings, or record the unavailable pass, override, and residual risk without claiming clean closure.
6. Install or reinstall each changed adapter using its documented installation boundary.
7. Start a new session in every affected host before evaluating updated skills. Existing sessions retain already-loaded instruction context and cannot prove the new behavior.

The adopted-project fixture variants are consumer checks. They must be validated separately from source-repository checks whenever shared policy, adapter behavior, skill triggers, schemas, or installation guidance changes. Do not release an adapter as verified until its fresh-session fixture evidence is recorded. Passing deterministic, skill, and plugin validators proves structure; it does not replace pressure scenarios, independent review, reinstall, or fresh-session consumer evidence.
