---
name: careful-adopt
description: Initialize or adopt a project into Careful. Use for new projects, unfamiliar repositories, or explicit setup requests. For a new project, guide evidence-led exploration into a concise project profile. For an existing project, inspect it read-only, infer stack and conventions, validate only material uncertainty with the user, and create a minimal profile without inventing policies.
---

# Careful Adopt

Read `references/project-profile.md`.

## New project

Explore the problem before implementation. Challenge consequential product and technical assumptions, research externally verifiable claims, and propose one recommended direction. Once accepted, create a concise project profile and documentation map. Initialize OpenSpec only when the project has a durable behavior/change surface.

## Existing project

Inspect repository layout, build/test commands, dependencies, architecture clues, documentation, configuration, and recent changes. Mark discoveries as Verified or Inferred. Resolve or ask about the project’s durable specification authority when it materially changes the workflow, and inspect for competing durable-looking specification paths. Draft the smallest profile that explains commands, risk boundaries, document locations, specification authority, and execution-plan location; do not rewrite existing documentation merely to fit the harness. Add or merge tracked project guidance from `references/project-guidance.md` so Codex uses `careful-workflow` for substantive work when the plugin is installed.
