## Context

Careful needs a default operating contract and specialist playbooks. Skill discovery can make a specialist skill available, but a separate skill is not a reliable substitute for a baseline instruction inside the main workflow.

## Decisions

- Keep `careful-documentation` and `careful-retrospective` as dedicated skills for focused, deeper tasks.
- Put the minimal automatic checks directly in `careful-workflow`.
- Perform the retrospective signal assessment before the final handoff because the agent cannot begin new work after it sends a final response.
- Use tracked `AGENTS.md` guidance as the per-project activation point and avoid requiring users to invoke commands for normal work.
- Keep private `.careful/` context out of the activation path.

## Validation strategy

Validate skill structure and plugin manifest. Confirm the self-hosting `AGENTS.md` and the fixture project include the project-guidance template. Validate the modified OpenSpec capability and the full spec set.
