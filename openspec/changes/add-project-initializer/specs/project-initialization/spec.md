## ADDED Requirements

### Requirement: Two-mode project initialization

Careful SHALL provide a documented, versioned `./bin/careful init <project>` command for preparing a Git repository to consume Careful. The command SHALL default to linked mode, SHALL support an explicit portable mode, and SHALL preserve an interface that can later be packaged as `careful init`.

The command SHALL define `--source`, `--revision`, `--adapters`, `--dry-run`, `--non-interactive`, and `--yes` consistently across applicable lifecycle operations. In linked mode, `--source` is a local Careful checkout and defaults to the checkout containing the invoked command. In portable mode, `--source` is a Git remote, and `--revision` SHALL resolve to a fetchable immutable commit before mutation.

#### Scenario: Initializing a project that does not exist

- **WHEN** the target path does not exist
- **THEN** the initializer SHALL preview creation of that directory and initialization of a Git repository within it
- **AND** an accepted run SHALL create no parent, sibling, remote, branch, commit, or push beyond that preview

#### Scenario: Initializing an existing non-Git directory

- **WHEN** the target exists, is not a Git repository, and contains project files
- **THEN** the initializer SHALL preserve those files and preview Git-repository initialization plus Careful artifacts
- **AND** it SHALL not mutate the directory until the preview is accepted

#### Scenario: Target is a subdirectory of an existing repository

- **WHEN** an existing target resolves inside a parent Git repository but is not that repository's root
- **THEN** the initializer SHALL fail before mutation
- **AND** it SHALL report the canonical target and discovered repository root so the caller can select the root explicitly

#### Scenario: Initializing a local project in linked mode

- **WHEN** a developer initializes a project without selecting a source mode
- **THEN** the initializer SHALL create `vendor/careful` as a symlink to the developer-selected Careful checkout
- **AND** it SHALL exclude that path and `careful.local.yaml` through local `.git/info/exclude`, not tracked `.gitignore`
- **AND** it SHALL not commit or generate a tracked absolute filesystem path
- **AND** it SHALL report how to repair the link if the checkout is moved

#### Scenario: Initializing a shareable project in portable mode

- **WHEN** a developer initializes a project with portable mode
- **THEN** the initializer SHALL add `vendor/careful` as a Git submodule sourced from the selected Careful remote at an explicit commit
- **AND** it SHALL default that remote to `https://github.com/bwhessels/careful.git` when `--source` is omitted
- **AND** it SHALL create tracked `careful.lock.yaml` identifying the remote, immutable commit, source-root path, and lock-format version
- **AND** it SHALL report that a fresh clone requires `--recurse-submodules`

#### Scenario: Resolving shared policy from either mode

- **WHEN** initialization generates project guidance or a host adapter shim
- **THEN** every shared-policy reference SHALL resolve to `vendor/careful/core/policy.md` from the generated artifact's consumer-project location
- **AND** generated shims SHALL not duplicate normative policy prose
- **AND** validation SHALL fail if any generated reference is missing in either source mode

#### Scenario: Previewing initialization

- **WHEN** a developer requests a dry-run for initialization
- **THEN** the command SHALL report every planned tracked-file, ignored-state, symlink, submodule, and guidance change
- **AND** it SHALL make no filesystem or Git-index mutation
- **AND** a subsequent accepted run against unchanged inputs SHALL apply the same mutation set

### Requirement: Project ownership and safe initialization

The initializer SHALL preserve project-owned source code, product documentation, OpenSpec artifacts, existing configuration, and private local context. It SHALL preview proposed changes and refuse collisions or mode replacement unless the user explicitly selects a merge or migration operation.

#### Scenario: Existing project guidance is present

- **WHEN** an existing project already contains host guidance or a Careful project profile
- **THEN** the initializer SHALL identify the conflict in its preview
- **AND** it SHALL not overwrite the file by default
- **AND** it SHALL offer an explicit merge or migration path that preserves the existing content

#### Scenario: Migrating between source modes

- **WHEN** a user requests migration from linked to portable mode or the reverse
- **THEN** the initializer SHALL display the Git and filesystem effects before changing state
- **AND** it SHALL not automatically delete copied or obsolete harness artifacts

#### Scenario: Running non-interactively with an unresolved decision

- **WHEN** initialization runs non-interactively and encounters a collision, merge choice, source-path choice, or migration decision that was not explicitly provided
- **THEN** it SHALL fail without partial mutation
- **AND** it SHALL report the missing explicit option needed to continue

#### Scenario: Accepting a fully specified non-interactive preview

- **WHEN** a caller supplies `--non-interactive --yes` and all options required to resolve the preview without a prompt
- **THEN** the command SHALL apply only the previewed mutation set
- **AND** documented deterministic defaults for source and revision MAY be used only when shown in that preview
- **AND** `--yes` SHALL not authorize an unspecified collision resolution or merge strategy

#### Scenario: Portable revision is not fetchable

- **WHEN** portable initialization or upgrade resolves a revision that is not fetchable from the selected remote
- **THEN** the command SHALL fail before changing the target project
- **AND** it SHALL report the remote and unresolved revision

### Requirement: Adapter-aware initialization and truthful capability reporting

The initializer SHALL support setup selection for Codex, Claude Code, and Factory Droid. It SHALL obtain each adapter's status and available controls from the canonical adapter manifest and SHALL not represent setup as evidence that a host control executed.

Selected adapters SHALL be recorded in tracked `careful.project.yaml`. A portable source lock SHALL not cache adapter verification status; `init` and `doctor` SHALL derive current status from the manifest in the resolved Careful source.

#### Scenario: Selecting all supported adapters

- **WHEN** a user requests initialization for Codex, Claude Code, and Factory Droid
- **THEN** the initializer SHALL configure only the selected adapters' project-facing artifacts
- **AND** it SHALL report each adapter's canonical status and any required installation or fresh-session step
- **AND** it SHALL preserve experimental status for adapters not marked verified by the manifest

#### Scenario: A required host component is unavailable

- **WHEN** the initializer cannot verify an installed host plugin, marketplace dependency, or fresh-session fixture
- **THEN** it SHALL report the unavailable control and its recovery step
- **AND** it SHALL not claim the control has completed

### Requirement: Command and skill responsibility boundary

The Careful command SHALL be the sole owner of initialization, source-mode, receipt, repair, migration, upgrade, and verification mutations. `careful-adopt` SHALL act as an evidence-led conversational entry point that recognizes initializer state and guides or invokes the command without independently reproducing its filesystem logic.

#### Scenario: Adopting an uninitialized project through a host skill

- **WHEN** `careful-adopt` determines that a project has not been initialized
- **THEN** it SHALL recommend or invoke the canonical initializer command according to host capability and user authorization
- **AND** it SHALL not simulate the initializer by independently creating harness files
- **AND** after successful initialization it SHALL continue with project profiling and documentation mapping

#### Scenario: Initializer command is unavailable

- **WHEN** an adapter can discover `careful-adopt` but cannot locate or execute the Careful command
- **THEN** the skill SHALL report the unavailable command and the exact recovery path
- **AND** it SHALL not claim the project is initialized

### Requirement: Reviewable portable source lifecycle

Careful SHALL document and support explicit inspection, upgrade, and recovery for an initialized project's source. It SHALL not automatically update a portable project's pinned Careful revision or write to any remote repository.

#### Scenario: Upgrading a portable project

- **WHEN** a maintainer requests an upgrade of a portable Careful source
- **THEN** the initializer SHALL show the current and proposed Careful revisions before modifying the submodule pointer
- **AND** it SHALL require the resulting project Git change to be reviewed and committed by the maintainer

#### Scenario: Repairing a local linked source

- **WHEN** a linked project no longer resolves its Careful symlink
- **THEN** the initializer SHALL diagnose the missing local source
- **AND** it SHALL recreate only the ignored link after the user provides or confirms a replacement checkout
- **AND** it SHALL not modify tracked project artifacts
