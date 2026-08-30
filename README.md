# Careful

An evidence-led, multi-harness workflow for exploration, implementation, review, documentation, and learning.

After installation and project adoption, Careful applies a default Standard workflow automatically where the host supports automatic activation. It escalates to Deep work for risky, product, architecture, public-contract, data, security, privacy, reliability, and hard-to-reverse changes. Explicit controls exist, but ordinary requests should not need them.

## What it does

- Labels meaningful claims as verified, inferred, assumed, or unknown.
- Challenges consequential decisions and blocks only with material evidence, a recommendation, and an override path.
- Uses OpenSpec as the durable record for Deep changes.
- Resolves a project-declared specification authority so durable specs are not duplicated across OpenSpec and execution-planning folders.
- Updates documentation through an impact assessment rather than a separate manual chore.
- Supports project-specific public-readiness checks and publication/release review gates.
- Runs retrospectives after high-signal work and proposes—not silently applies—improvements.

## Structure

- `core/` — canonical portable workflow policy and adapter manifest.
- `plugins/careful/` — Codex adapter and compatibility package.
- `adapters/` — Claude Code and Factory Droid adapter layouts.
- `examples/` — portable project-profile and OpenSpec schema examples.
- `docs/` — design notes for the harness itself.

## Status

Codex is the verified static adapter. Claude Code and Factory Droid adapters are experimental until their authenticated fresh-session fixtures are recorded. Careful intentionally excludes workplace governance, hosted control planes, centralized telemetry, and automatic mutation of user projects.

## Contributing

Contributions are welcome through GitHub pull requests. The `main` branch is protected: changes require review and approval from the project maintainer before merging. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution and validation workflow.

## Try it locally

For Codex, clone this repository, add it as a local marketplace, then install the plugin:

```bash
git clone https://github.com/<OWNER>/careful.git
cd careful
codex plugin marketplace add "$PWD"
codex plugin add careful@careful
```

Replace `<OWNER>` with the GitHub account or organization that publishes Careful.

Start a new Codex thread after installation. The workflow skill should activate for substantive product and coding work; use `$careful-adopt` when onboarding a project and `$careful-retrospective` for an explicit learning pass.

For Claude Code and Factory Droid, follow the adapter-specific paths in [docs/adoption.md](docs/adoption.md). Read [docs/compatibility.md](docs/compatibility.md) before relying on an adapter control.

To use the Deep OpenSpec workflow in a project, copy `examples/openspec-schemas/critical-deep` into that project's `openspec/schemas/` directory and set `schema: critical-deep` in `openspec/config.yaml`.
