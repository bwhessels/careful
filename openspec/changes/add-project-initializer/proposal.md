## Why

Careful's current adoption guide asks consumers to copy the portable core and adapter files into each project. That creates drift: a harness improvement must be manually propagated to every adopted repository, and it is unclear which Careful revision a project uses. A developer-local symlink solves fast iteration but cannot be committed safely because its filesystem path is not portable to GitHub, collaborators, or CI.

Careful needs a deliberate initializer that supports both local shared-source development and reproducible GitHub repositories without making private local context or project-specific decisions shared artifacts.

## What Changes

- Add a project initializer command that configures an existing or new Git repository for Careful without overwriting project-owned files. The first release is invoked from a Careful checkout as `./bin/careful init <project>` and exposes the same command model intended for a future packaged `careful init` executable.
- Make **linked mode** the default local-development mode. It creates a Git-ignored symlink to a developer-selected Careful checkout so local harness changes are immediately visible to linked projects.
- Add **portable mode**, which adds a pinned Git submodule from the selected Careful remote, defaulting to `https://github.com/bwhessels/careful.git`, so the repository can be cloned, reviewed, and used on another machine with `--recurse-submodules`.
- Define a tracked source lock for portable installs and an ignored local receipt for linked installs. The portable lock identifies the Careful remote and immutable source revision; selected adapters remain in the project profile, while current capability status is read from the locked source's adapter manifest rather than copied into stale metadata. No tracked artifact stores an absolute local path.
- Support Codex, Claude Code, and Factory Droid setup in one initializer. Adapter status remains governed by the canonical adapter manifest; initialization must not upgrade an experimental adapter into a verified claim.
- Add upgrade, repair, verification, migration, fixture, and GitHub documentation for the two modes.
- Update `careful-adopt` to recognize initializer state, guide or invoke the deterministic command where the host permits it, and continue with evidence-led project profiling after filesystem setup. Do not create a second skill that duplicates initializer mutation or safety logic.

Explicit non-goals: a hosted control plane, automatic updates to consumer repositories, copying product context into Careful, reading or writing `.careful/` private context, a package-manager-distributed global CLI in the first release, duplicated mutation logic in a separate initializer skill, or a claim that all three host adapters have identical capabilities.

## Dependency and sequencing

This change depends on `multi-harness-adapters`. That predecessor introduces `portable-workflow-core` and `cross-harness-adoption` and modifies `self-hosting-careful`; it SHALL be completed, synced into current specifications, and archived before this change is synced, archived, or released. The delta specifications here modify the post-`multi-harness-adapters` capability state and SHALL NOT be applied independently to the pre-adapter current specs.

## Capabilities

### New Capabilities

- `project-initialization`: Safe, repeatable setup of a project with either a local linked Careful source or a portable, pinned GitHub source.

### Modified Capabilities

- `portable-workflow-core`: Define how a project consumes a versioned portable source without duplicating core policy.
- `cross-harness-adoption`: Define per-adapter initialization, status reporting, migration, and consumer-fixture validation.
- `self-hosting-careful`: Extend source validation and fixtures to cover the initializer and its public/ignored artifact boundaries.

## Impact

Affected core adoption documentation, adapter manifest semantics, examples, fixtures, self-hosting validation, release guidance, and the project-initialization script. The first implementation is a versioned script in the Careful repository; it does not introduce a global executable or external runtime service.
