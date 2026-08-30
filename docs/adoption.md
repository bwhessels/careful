# Adopting Careful

Careful has one portable policy in `core/policy.md`. Keep it as the canonical source. `AGENTS.md`, `CLAUDE.md`, skills, and droids are small host adapters; do not copy policy prose into each.

## Shared project setup

1. Copy `core/` into the adopted project.
2. Add the shared `AGENTS.md` guidance appropriate to the project, referencing `core/policy.md`.
3. Add `careful.project.yaml` using [examples/project-profile.yaml](../examples/project-profile.yaml) as a starting point.
4. Keep personal notes, product context, and local event records in `.careful/`; add it to `.gitignore`.
5. Select only the adapters used in that project.

Declare the project’s durable specification authority in `documentation.spec_authority` and its execution-plan location in `documentation.execution_plans`. When OpenSpec is declared, keep proposals, designs, requirements, tasks, and history under `openspec/`; execution plans must link to those artifacts. During adoption, report competing durable-looking specification paths and ask before migrating them.

If the project is intended for external publication, configure `public_readiness` with its audience mode, required documents, project checks, and first-publication/release gates. Careful validates the objective parts; owners remain responsible for license, privacy, security-disclosure, support, and publication decisions.

## Codex

Install `careful@careful` from this repository's marketplace. Keep `AGENTS.md` tracked, then start a fresh Codex thread. The current plugin path remains supported for this compatibility release.

Rollback: remove the plugin with Codex's plugin command and return to the previously installed marketplace/plugin version. Project `AGENTS.md` remains readable guidance but must not be treated as proof that the plugin ran.

## Claude Code

Copy `adapters/claude-code/CLAUDE.md`, `AGENTS.md`, `.claude/skills/`, and `.claude/agents/` into the project together with `core/`. `CLAUDE.md` imports `AGENTS.md`, avoiding duplicate project policy. Start a new Claude Code session after installation.

Rollback: remove the copied `.claude/skills/careful-*` and `.claude/agents/careful-independent-review.md`, then remove the Claude-specific section from `CLAUDE.md`. Preserve the shared guidance only if another adapter still uses it.

## Factory Droid

Copy `adapters/factory-droid/AGENTS.md`, `.factory/skills/`, and `.factory/droids/` into the project together with `core/`. Start a new Droid session after installation.

Rollback: remove the copied `.factory/skills/careful-*` and `.factory/droids/careful-independent-review.md`. Preserve `AGENTS.md` only if another adapter still uses it.

## Adding another host

Another host is not supported merely because it can read Markdown. Propose an OpenSpec Deep change that demonstrates documented discovery, explicit-control mapping, capability reporting, static validation, a fresh-session fixture, documentation, and a migration path.
