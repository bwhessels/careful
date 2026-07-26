# Factory Droid adapter

Requires Factory Droid support for repository `AGENTS.md`, project skills, and custom droids. The adapter is **experimental** until its consumer fixture has been evaluated in a fresh authenticated Droid session.

Copy `AGENTS.md`, `.factory/skills/`, and `.factory/droids/` into an adopted project, preserving their relative paths to `core/policy.md` or copying the `core/` directory with them.

Controls map to skills: `careful-workflow` (baseline/depth), `careful-documentation`, `careful-retrospective`, and `careful-adopt`. Deep review uses the read-only `careful-independent-review` droid. If it is unavailable, state that in the final handoff and request an explicit second review.

Sources: [Factory project guidance](https://docs.factory.ai/cli/getting-started/how-to-talk-to-a-droid), [Factory skills](https://docs.factory.ai/cli/configuration/skills), and [Factory subagents](https://docs.factory.ai/cli/configuration/custom-droids).
