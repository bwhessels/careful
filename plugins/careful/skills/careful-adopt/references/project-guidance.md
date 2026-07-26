# Project guidance template

Add this concise section to the project's tracked `AGENTS.md`, preserving its existing instructions:

```markdown
## Careful workflow

When the Careful plugin is installed, use `$careful-workflow` for substantive product, coding, debugging, and architecture tasks. Let it select Quick, Standard, or Deep depth; do not require a Careful command for normal work.

Use `$careful-documentation` for dedicated documentation audits or repairs. Use `$careful-retrospective` for an explicit, full learning review.

If the Careful plugin is unavailable, say so before claiming that Careful controls were applied.
```

Do not add the section to untracked local instructions. The project guidance is the public activation point; `.careful/` remains private local context.
