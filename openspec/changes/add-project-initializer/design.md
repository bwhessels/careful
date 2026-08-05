## Context

Careful currently has one canonical portable policy (`core/policy.md`) and thin host adapters, but consumer adoption copies those files into the project. The desired workflow is to improve Careful once and use those improvements immediately in local projects, while preserving a GitHub-compatible path for collaborators and CI.

The initializer changes distribution and adoption behavior, not project behavior. A project retains ownership of its product requirements, source code, `careful.project.yaml`, tracked guidance, OpenSpec artifacts, and any project-specific documentation. `.careful/` remains private and ignored.

This design is sequenced after the active `multi-harness-adapters` change. Implementation may be prototyped while that work remains open, but this change SHALL not sync or archive its modified capability deltas until the predecessor has established `portable-workflow-core`, `cross-harness-adoption`, and its updated `self-hosting-careful` requirements as current specifications.

## Decisions

### 1. Ship one deterministic command with two explicit source modes

The Careful repository SHALL ship a versioned, documented command at `./bin/careful`. Its first public workflow SHALL be `./bin/careful init <project>`, with `linked` as the default mode and `portable` as an explicit option. The command structure SHALL remain compatible with later packaging as `careful init` without making global installation part of this change.

If `<project>` does not exist, `init` SHALL preview creation of that single directory and initialization of a Git repository within it. If the directory exists but is not a Git repository, `init` SHALL preview `git init` without altering existing contents. If the canonical target path is already a Git repository root, the initializer SHALL use it. If an existing target resolves inside a parent Git repository but is not that repository's root, the initializer SHALL fail and report the discovered root so it never silently initializes only a subdirectory. The command SHALL never create a Git remote, branch, commit, or push as part of initialization.

The same entry point SHALL expose lifecycle operations using a consistent target-project argument:

```text
./bin/careful init <project> [--mode linked|portable]
    [--source <path-or-url>] [--revision <git-ref>]
    [--adapters codex,claude-code,factory-droid]
    [--dry-run] [--non-interactive --yes]
./bin/careful doctor <project>
./bin/careful repair <project> [--source <path>] [--dry-run]
./bin/careful upgrade <project> [--revision <git-ref>] [--dry-run]
./bin/careful migrate <project> --mode linked|portable
    [--source <path-or-url>] [--revision <git-ref>]
    [--dry-run] [--non-interactive --yes]
```

`--source` SHALL mean a local checkout path in linked mode and a Git remote URL in portable mode. When omitted in linked mode, it SHALL deterministically default to the Careful checkout containing the invoked `./bin/careful`. When omitted in portable mode, it SHALL deterministically default to Careful's canonical public remote. `--revision` SHALL resolve to an immutable commit before mutation; portable initialization SHALL fail if that commit cannot be fetched from the selected remote. When omitted, it SHALL deterministically use the commit containing the invoked command, but only after verifying that commit is reachable from the selected portable remote. These documented deterministic defaults remain valid in non-interactive mode and SHALL appear explicitly in its preview.

All mutating operations SHALL support `--dry-run`. `init` and `migrate` SHALL require interactive confirmation when they would merge project-owned guidance or change tracked Git state. `--non-interactive` SHALL disable prompts, and mutation in that mode SHALL require `--yes`; `--yes` SHALL accept only the fully resolved preview. It SHALL not resolve a collision or merge strategy, but documented deterministic defaults for source and revision are permitted and SHALL be shown in the preview. `doctor` SHALL be read-only and require neither confirmation flag.

| Mode | Source representation | GitHub / CI behavior | Intended use |
| --- | --- | --- | --- |
| `linked` | Git-ignored symlink to a local Careful checkout | Requires bootstrap on each machine; no developer path is committed | Active local Careful development |
| `portable` | Tracked Git submodule pinned to a selected Careful remote and commit; defaults to `https://github.com/bwhessels/careful.git` | Clone with `--recurse-submodules`; revision is reviewable and reproducible | Collaboration, CI, and durable projects |

The initializer SHALL refuse to silently replace a source managed by the other mode. It SHALL provide an explicit migration operation that describes the affected Git changes before making them.

Both modes SHALL expose the full Careful repository at the same consumer-relative source root, `vendor/careful/`. In linked mode, `vendor/careful` SHALL be a symlink excluded only through the consumer repository's local `.git/info/exclude`; the initializer SHALL not add that path to tracked `.gitignore`. In portable mode, `vendor/careful` SHALL be the tracked Git submodule path and SHALL not be locally excluded.

Project-facing guidance and adapter shims SHALL resolve portable policy from `vendor/careful/core/policy.md`. Any generated shim SHALL contain only project activation or host-discovery mechanics; it SHALL not copy normative policy prose. Validation SHALL resolve every generated policy/skill reference from its consumer-project location in both modes so successful initialization cannot leave a broken relative path.

**Why:** A symlink supplies the requested live, single local source of truth. A Git submodule keeps the same upstream source of truth while making its selected revision portable and reviewable. Copies are not the default because they reintroduce drift.

**Alternatives considered:**

- Commit an absolute or relative symlink: rejected because it breaks on a normal GitHub clone or silently assumes a neighboring checkout layout.
- Copy `core/` and adapters into each project: rejected as the default because it creates many independently editable policy copies.
- Package a global `careful` binary immediately: deferred because package distribution, installation, and cross-platform release policy would expand scope before the command contract is proven. The checked-in `./bin/careful` entry point preserves the intended interface.

### 2. Keep project artifacts project-owned and source receipts truthful

The initializer SHALL create or merge only a minimal tracked project profile, host guidance, and thin adapter shims required for host discovery. It SHALL not overwrite an existing `AGENTS.md`, `CLAUDE.md`, `.factory/`, `careful.project.yaml`, OpenSpec artifact, or project documentation without an explicit user-selected merge or migration operation.

For portable mode, tracked `careful.lock.yaml` SHALL identify the source remote, immutable commit, source-root path, and lock-format version. For linked mode, the local source path and observed commit SHALL be written only to `careful.local.yaml`, excluded through local `.git/info/exclude` alongside the source symlink. Selected adapters SHALL remain in tracked `careful.project.yaml`, which is project configuration rather than source resolution. A tracked file SHALL never contain an absolute developer filesystem path.

Adapter status and available controls SHALL be computed when `init` or `doctor` runs from the resolved source's `core/adapter-manifest.yaml`; status SHALL not be copied into the source lock. Codex may be reported as verified only when the resolved manifest says so; Claude Code and Factory Droid must retain their declared experimental status until their fixture evidence changes that status.

### 3. Keep skills advisory and command mutations deterministic

`careful-adopt` SHALL recognize whether the target is uninitialized, linked, portable, or inconsistent. When command execution is available and authorized, the skill MAY guide or invoke `./bin/careful init`; otherwise it SHALL provide the exact command and explain the expected preview. After successful initialization, `careful-adopt` SHALL continue its existing evidence-led project-profile workflow.

The command owns filesystem inspection, collision detection, symlink/submodule changes, receipts, repair, migration, and verification. Skills SHALL not reimplement those mutations in prose or host-specific scripts. This keeps the safety behavior testable and identical across Codex, Claude Code, and Factory Droid.

**Why:** A skill cannot reliably exist before a repository or plugin is installed, and prose-driven filesystem changes are harder to test. The skill is the conversational guide; the command is the deterministic mechanism.

### 4. Support all three adapters through an adapter-aware plan

The initializer SHALL accept a selection for Codex, Claude Code, and Factory Droid, defaulting to all currently supported adapters when no selection is made. It SHALL install or reference only the selected adapter files and produce a capability report based on the canonical manifest.

The initializer SHALL not claim a host plugin, marketplace dependency, fresh-session check, or independent-review control has run merely because project files were generated. It SHALL provide the required next command or manual recovery step for each selected adapter.

### 5. Make GitHub and local lifecycle operations explicit

The public workflow SHALL document:

1. Developing Careful in `bwhessels/careful`, committing and pushing a harness change there.
2. Initializing a local consumer in linked mode and repairing its ignored link when the checkout moves.
3. Initializing a shareable consumer in portable mode, committing both the project change and submodule pointer, and cloning with `--recurse-submodules`.
4. Reviewing and applying an explicit update to a portable project's Careful pin.
5. Migrating between modes with a preview and without loss of project-owned files.

No mode performs automatic remote pushes, automatic consumer upgrades, or unrequested changes to another repository.

### 6. Validate the contract at source and consumer boundaries

Deterministic validation SHALL confirm command parsing, dry-run fidelity, the initializer's mode rules, ignored/tracked boundaries, receipt shape, adapter selection/status reporting, lifecycle operations, and migration safeguards. Fixtures SHALL cover a clean linked project and a clean portable project for each selected host adapter. Host behavior requiring a fresh session remains subject to the existing fixture and capability policy.

## Risks and mitigations

- **A linked project breaks when its local checkout moves.** Provide a diagnose/repair operation; preserve the project and recreate only the ignored link after confirmation.
- **A portable project falls behind Careful.** Record the pinned upstream commit and provide a reviewable upgrade operation; do not auto-update.
- **Submodules are unfamiliar to collaborators.** Keep clone, update, and recovery instructions concise and test them in fixtures.
- **Adapters drift or overclaim support.** Read adapter status from the manifest, validate it, and require fresh-session fixture evidence before changing a status.
- **An initializer overwrites a project.** Default to preview and refusal on collisions; require explicit user action for merges or migration, and test that dry-run output matches the eventual mutation set.
- **A skill and command drift apart.** Make the command the sole mutation owner and validate that `careful-adopt` delegates to its documented interface.

## Migration plan

1. Add the initializer, receipt schema, fixtures, validation, and documentation without changing existing adopted projects.
2. Offer a migration from copied-core projects to either linked or portable source mode; it must identify obsolete copies and never delete them automatically.
3. Validate a fresh consumer repository in each mode and each selected adapter before release.
4. Update adoption documentation to recommend the initializer; retain manual adoption guidance for one compatibility release with a rollback path.

## Open questions resolved for this change

- All currently supported adapters are in scope. Their verified/experimental status is not changed by initialization.
- The first release exposes `./bin/careful` from the repository, not a separately packaged global CLI.
- Portable GitHub mode uses a pinned Careful Git submodule rather than a copied policy tree; its default remote is `https://github.com/bwhessels/careful.git`, with explicit fork or mirror overrides supported by `--source`.
