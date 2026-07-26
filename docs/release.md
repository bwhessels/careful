# Releasing Careful

1. Run `python3 scripts/validate_self_hosting.py`.
2. Run `openspec validate --all --strict --no-interactive`.
3. Validate the distributable plugin with the Codex plugin validator when it is available in the development environment.
4. Install or reinstall the updated plugin from its marketplace.
5. Start a new Codex thread before evaluating updated skills. Existing threads retain already-loaded skill context and cannot prove the new behavior.

The adopted-project fixture is a consumer check. It must be validated separately from source-repository checks whenever plugin behavior, skill triggers, schemas, or installation guidance changes.
