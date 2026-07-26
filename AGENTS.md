# Careful development guidance

Treat this repository as the source of truth for Careful, the shareable coding-agent harness.

The portable workflow policy is [core/policy.md](core/policy.md). Keep host-specific discovery and permissions in `adapters/`; do not duplicate shared policy in adapter files.

## Careful workflow

When the Careful plugin is installed, use `$careful-workflow` for substantive product, coding, debugging, and architecture tasks. Let it select Quick, Standard, or Deep depth; do not require a Careful command for normal work.

Use `$careful-documentation` for dedicated documentation audits or repairs. Use `$careful-retrospective` for an explicit, full learning review.

If the Careful plugin is unavailable, say so before claiming that Careful controls were applied.

- Keep skills concise and use references for detailed templates.
- Preserve the distinction between automated default behavior and explicit escape-hatch commands.
- Do not add organization governance or adapters beyond Codex, Claude Code, and Factory Droid without an approved design change.
- Validate every skill with the skill-creator validator and the plugin with the plugin-creator validator.
- Update `docs/design.md` when changing core workflow, artifact ownership, or learning behavior.
