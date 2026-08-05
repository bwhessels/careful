## 0. Predecessor and change sequencing

- [ ] 0.1 Complete the remaining `multi-harness-adapters` fixture evidence, sync its durable specifications, and archive that change before syncing, archiving, or releasing `add-project-initializer`.
- [ ] 0.2 Rebase the initializer's three modified capability deltas against the archived predecessor specifications and validate that no predecessor requirement is lost.

## 1. Contract and initializer

- [ ] 1.1 Define tracked `careful.lock.yaml` for portable source identity and ignored `careful.local.yaml` for linked source state; keep selected adapters in `careful.project.yaml` and derive status from the resolved adapter manifest.
- [ ] 1.2 Implement the versioned `./bin/careful init <project>` command with dry-run preview, linked default, portable submodule mode, adapter selection, collision detection, and explicit confirmation for merges or migration.
- [ ] 1.3 Implement `doctor`, `repair`, `upgrade`, and `migrate` operations through the same command entry point without automatic remote writes or destructive cleanup.
- [ ] 1.4 Implement and document `--source`, `--revision`, `--adapters`, `--dry-run`, `--non-interactive`, and `--yes`, including immutable portable-revision resolution and fail-closed collision behavior.
- [ ] 1.5 Implement the common `vendor/careful` source root, linked-mode `.git/info/exclude` handling, portable submodule mount, and resolvable project-facing guidance paths.
- [ ] 1.6 Implement safe absent-directory, non-Git-directory, existing-repository, and nested-repository target handling without creating remotes, branches, commits, or pushes.

## 2. Adapter and project setup

- [ ] 2.1 Generate or merge only the selected host guidance and adapter setup while preserving existing project-owned files.
- [ ] 2.2 Read supported adapters and status from `core/adapter-manifest.yaml`; emit capability and recovery guidance without overclaiming plugin or fixture execution.
- [ ] 2.3 Preserve the boundary between tracked project configuration, linked local state, and private `.careful/` context.
- [ ] 2.4 Update `careful-adopt` for all three hosts to recognize initializer state and guide or invoke the command without duplicating its mutation logic.

## 3. Validation and fixtures

- [ ] 3.1 Add deterministic tests for command parsing, target/repository boundary handling, mode selection, dry-run fidelity, source receipts, collision refusal, preview, non-interactive failure, migration, repair, upgrade behavior, and reference resolution from generated consumer artifacts.
- [ ] 3.2 Add clean consumer fixtures for linked and portable setup across Codex, Claude Code, and Factory Droid, including expected capability reporting.
- [ ] 3.3 Extend self-hosting validation to check the initializer, receipt boundaries, documentation, fixture declarations, and manifest-driven status handling.
- [ ] 3.4 Validate every changed Careful skill with the skill-creator validator and validate the distributable Codex plugin with the plugin-creator validator.
- [ ] 3.5 Run OpenSpec validation, self-hosting validation, adapter-specific static checks, and the fresh-session fixture process required for changed host behavior.

## 4. Documentation and release

- [ ] 4.1 Update adoption, compatibility, release, README, examples, and migration/rollback guidance with linked and portable GitHub workflows.
- [ ] 4.2 Document the exact GitHub lifecycle: Careful source update, linked local use, portable submodule pin, clone, upgrade, and recovery.
- [ ] 4.3 Obtain independent Deep review of source boundaries, Git safety, adapter claims, migration safety, and documentation completeness.
- [ ] 4.4 Record implementation evidence and retrospective assessment, update durable current specifications, and archive the change only after required fixtures are recorded.
