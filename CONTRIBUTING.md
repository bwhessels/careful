# Contributing to Careful

Thanks for considering a contribution. Careful is intentionally small and opinionated: changes should preserve its evidence-led, proportional workflow.

## Before opening a pull request

1. Fork the repository and create a focused branch from `main`.
2. Make the smallest change that solves the stated problem.
3. Update the relevant documentation and OpenSpec artifact when the change affects a workflow, public contract, or architecture.
4. Run the validation commands from the repository root:

   ```bash
   python3 -m unittest discover -s tests -v
   python3 scripts/validate_change_dependencies.py
   python3 scripts/validate_public_readiness.py
   python3 scripts/validate_spec_authority.py
   python3 scripts/validate_self_hosting.py
   python3 /path/to/plugin-creator/scripts/validate_plugin.py plugins/careful
   openspec validate --all --strict --no-interactive
   ```

5. Open a pull request using the template and describe the motivation, trade-offs, validation, and any documentation impact.

For this maintainer-led project, the configured public-readiness gate is a lightweight maintainer review. It checks that public orientation, status and limitation claims, the MIT license, and documentation impact remain accurate. It is not independent review or formal certification.

OpenSpec's generated `.codex/skills/` wrappers are local development convenience files and are intentionally ignored. The tracked `openspec/` artifacts and the OpenSpec CLI are the contributor-facing source of truth.

An active change that builds on another active change declares its direct predecessor in the change's `.openspec.yaml`:

```yaml
depends_on:
  - predecessor-change-name
```

Use this when the later change modifies a capability that is not yet current and the predecessor adds it. Keep this canonical top-level, two-space-indented block-list form with unquoted, unique change names. Blank and comment-only separators are allowed between items. Inline lists, quoted items, whitespace-altered keys, malformed indentation, duplicates, and empty lists fail validation rather than being guessed at. When a predecessor is archived first, retain its original name in `depends_on`: the validator recognizes the date-prefixed OpenSpec archive directory as durable provenance. Names absent from both active changes and date-prefixed archives remain unknown. `scripts/validate_change_dependencies.py` also checks required declarations, self dependencies, and active dependency cycles; it complements rather than replaces strict OpenSpec validation.

## Review and merging

Pull requests are welcome, but only project writers can merge them. Public contributors should use forks and pull requests; `main` remains protected and pull-request-only. Please keep PRs focused so they can be evaluated carefully.

## Design changes

For a risky, architectural, product, or public-contract change, begin with the Careful Deep workflow and record the decision in OpenSpec. Do not silently broaden Careful's scope into workplace governance or non-Codex adapters.
