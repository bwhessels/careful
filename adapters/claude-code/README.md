# Claude Code adapter

Requires Claude Code support for project `CLAUDE.md`, project skills, and custom subagents. The adapter is **experimental** until its consumer fixture has been evaluated in a fresh authenticated Claude Code session.

Copy `CLAUDE.md`, `AGENTS.md`, `.claude/skills/`, and `.claude/agents/` into an adopted project, preserving their relative paths to `core/policy.md` or copying the `core/` directory with them. `CLAUDE.md` imports the shared `AGENTS.md`; do not duplicate the policy in both files.

Controls map to skills: `careful-workflow` (baseline/depth), `careful-documentation`, `careful-retrospective`, and `careful-adopt`. Deep review uses the read-only `careful-independent-review` subagent. If it is unavailable, state that in the final handoff and request an explicit second review.

Sources: [Claude memory](https://code.claude.com/docs/en/memory), [Claude skills](https://code.claude.com/docs/en/skills), and [Claude subagents](https://code.claude.com/docs/en/sub-agents).
