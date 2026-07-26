# Careful

An evidence-led Codex plugin for exploration, implementation, review, documentation, and learning.

After installation and project adoption, the plugin applies a default Standard workflow automatically. It escalates to Deep work for risky, product, architecture, public-contract, data, security, privacy, reliability, and hard-to-reverse changes. Explicit controls exist, but ordinary requests should not need them.

## What it does

- Labels meaningful claims as verified, inferred, assumed, or unknown.
- Challenges consequential decisions and blocks only with material evidence, a recommendation, and an override path.
- Uses OpenSpec as the durable record for Deep changes.
- Updates documentation through an impact assessment rather than a separate manual chore.
- Runs retrospectives after high-signal work and proposes—not silently applies—improvements.

## Structure

- `plugins/careful/` — Codex plugin and skills.
- `examples/` — portable project-profile and OpenSpec schema examples.
- `docs/` — design notes for the harness itself.

## Status

This is an initial Codex-only implementation. It intentionally excludes workplace governance, non-Codex adapters, and automatic mutation of user projects.

## Contributing

Contributions are welcome through GitHub pull requests. The `main` branch is protected: changes require review and approval from the project maintainer before merging. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution and validation workflow.

## Try it locally

Clone this repository, add it as a local marketplace, then install the plugin:

```bash
git clone https://github.com/<OWNER>/careful.git
cd careful
codex plugin marketplace add "$PWD"
codex plugin add careful@careful
```

Replace `<OWNER>` with the GitHub account or organization that publishes Careful.

Start a new Codex thread after installation. The workflow skill should activate for substantive product and coding work; use `$careful-adopt` when onboarding a project and `$careful-retrospective` for an explicit learning pass.

To use the Deep OpenSpec workflow in a project, copy `examples/openspec-schemas/critical-deep` into that project's `openspec/schemas/` directory and set `schema: critical-deep` in `openspec/config.yaml`.
