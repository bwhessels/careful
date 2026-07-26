# Careful compatibility matrix

| Adapter | Status | Shared guidance | Baseline activation | Independent Deep review | Fixture evidence |
| --- | --- | --- | --- | --- | --- |
| Codex | Verified fixture | `AGENTS.md` + plugin skill | `careful-workflow` skill | Codex independent reviewer | Static repository/plugin validation and fresh read-only fixture evaluation on 2026-07-26 |
| Claude Code | Experimental static | `CLAUDE.md` importing `AGENTS.md` | Project skill discovery | `careful-independent-review` subagent | Static layout validation; authenticated fresh-session fixture pending |
| Factory Droid | Experimental static | `AGENTS.md` | `.factory/skills/` discovery | `careful-independent-review` droid | Static layout validation; authenticated fresh-session fixture pending |

“Experimental static” means repository structure and deterministic checks passed, but no authenticated fresh host session has yet proven activation. A fixture-verified adapter has also completed its recorded fresh-session scenario. The release process requires a fresh-session fixture for every affected adapter.

The adapter manifest is the machine-readable source for these claims: [core/adapter-manifest.yaml](../core/adapter-manifest.yaml). Claude and Factory assumptions are based on the official [Claude Code documentation](https://code.claude.com/docs/en/skills) and [Factory Droid documentation](https://docs.factory.ai/cli/configuration/skills), checked on 2026-07-26; their minimum CLI versions remain intentionally unpinned until authenticated fixture runs establish them.
