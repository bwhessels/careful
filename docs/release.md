# Releasing Careful

1. Run `python3 scripts/validate_self_hosting.py`.
2. Run `openspec validate --all --strict --no-interactive`.
3. Validate the Codex plugin with the Codex plugin validator when it is available in the development environment.
4. Run static validation for every adapter and compare it against `core/adapter-manifest.yaml`.
5. Install or reinstall each changed adapter.
6. Start a new session in every affected host before evaluating updated skills. Existing sessions retain already-loaded instruction context and cannot prove the new behavior.

The adopted-project fixture variants are consumer checks. They must be validated separately from source-repository checks whenever shared policy, adapter behavior, skill triggers, schemas, or installation guidance changes. Do not release an adapter as verified until its fresh-session fixture evidence is recorded.
