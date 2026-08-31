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

## Why Careful is different

Careful is designed to make the reasoning around a change inspectable:

- **Evidence before confidence.** Important claims are labeled as verified, inferred, assumed, or unknown, so gaps are visible instead of being hidden behind confident prose.
- **Proportional controls.** Quick, Standard, and Deep workflows match the amount of scrutiny to the risk. A README fix does not need the same process as a security, privacy, architecture, or public-contract change.
- **Useful blocks.** When a decision lacks evidence or could cause material harm, Careful can stop with the reason, evidence, recommended path, and explicit override route.
- **One durable record.** Projects choose one specification authority—OpenSpec for this repository—while execution plans remain plans. That prevents requirements and decisions from drifting across competing documents.
- **Documentation follows impact.** Careful routes behavior, architecture, contributor, operational, and public-contract facts to their canonical documents instead of treating documentation as an after-the-fact chore.
- **Honest portability.** Host adapters provide discovery and control mechanics, while fixtures and capability reporting distinguish verified behavior from static or experimental support.

## Structure

- `core/` — canonical portable workflow policy and adapter manifest.
- `plugins/careful/` — Codex adapter and compatibility package.
- `adapters/` — Claude Code and Factory Droid adapter layouts.
- `examples/` — portable project-profile and OpenSpec schema examples.
- `docs/` — design notes for the harness itself.

## Status and scope

Careful is a maintainer-led, experimental project. Codex is the verified static adapter; Claude Code and Factory Droid adapters are experimental until their authenticated fresh-session fixtures are recorded. Careful intentionally excludes workplace governance, hosted control planes, centralized telemetry, and automatic mutation of user projects. Passing repository checks does not certify a project’s public documentation, legal posture, security process, or production readiness.

The canonical documentation is split by purpose:

- [Adoption](docs/adoption.md) — install and add Careful to a project.
- [Compatibility](docs/compatibility.md) — adapter status and verification claims.
- [Release](docs/release.md) — maintainer validation and release procedure.
- [Contributing](CONTRIBUTING.md) — contributor workflow and checks.
- [License](LICENSE) — MIT license terms.

## Contributing

Contributions are welcome through GitHub pull requests. The `main` branch is protected: changes require review and approval from the project maintainer before merging. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution and validation workflow.

## License

[MIT](LICENSE)

## Try it locally

For Codex, clone this repository, add it as a local marketplace, then install the plugin:

```bash
git clone https://github.com/bwhessels/careful.git
cd careful
codex plugin marketplace add "$PWD"
codex plugin add careful@careful
```

Start a new Codex thread after installation. The workflow skill should activate for substantive product and coding work; use `$careful-adopt` when onboarding a project and `$careful-retrospective` for an explicit learning pass.

For Claude Code and Factory Droid, follow the adapter-specific paths in [docs/adoption.md](docs/adoption.md). Read [docs/compatibility.md](docs/compatibility.md) before relying on an adapter control.

To use the Deep OpenSpec workflow in a project, copy `examples/openspec-schemas/critical-deep` into that project's `openspec/schemas/` directory and set `schema: critical-deep` in `openspec/config.yaml`.
