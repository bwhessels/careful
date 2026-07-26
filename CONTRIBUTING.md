# Contributing to Careful

Thanks for considering a contribution. Careful is intentionally small and opinionated: changes should preserve its evidence-led, proportional workflow.

## Before opening a pull request

1. Fork the repository and create a focused branch from `main`.
2. Make the smallest change that solves the stated problem.
3. Update the relevant documentation and OpenSpec artifact when the change affects a workflow, public contract, or architecture.
4. Run the validation commands from the repository root:

   ```bash
   python3 scripts/validate_self_hosting.py
   python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/careful
   openspec validate --all --strict --no-interactive
   ```

5. Open a pull request using the template and describe the motivation, trade-offs, validation, and any documentation impact.

OpenSpec's generated `.codex/skills/` wrappers are local development convenience files and are intentionally ignored. The tracked `openspec/` artifacts and the OpenSpec CLI are the contributor-facing source of truth.

## Review and merging

Pull requests are welcome, but only project writers can merge them. Public contributors should use forks and pull requests; `main` remains protected and pull-request-only. Please keep PRs focused so they can be evaluated carefully.

## Design changes

For a risky, architectural, product, or public-contract change, begin with the Careful Deep workflow and record the decision in OpenSpec. Do not silently broaden Careful's scope into workplace governance or non-Codex adapters.
