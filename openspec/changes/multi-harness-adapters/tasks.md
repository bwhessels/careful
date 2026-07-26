## 1. Compatibility baseline and portable contract

- [x] 1.1 Verify and record the supported Claude Code and Factory Droid versions, discovery paths, skill metadata, project-guidance behavior, and review/subagent capabilities from official documentation.
- [x] 1.2 Create the versioned portable workflow contract, reference templates, and adapter manifest with required capability declarations.
- [x] 1.3 Extract shared Careful policy from the Codex skill references into the portable contract without changing its observable semantics.
- [x] 1.4 Add deterministic validation that detects missing manifest fields, duplicated policy blocks, unsupported capability claims, and adapter/core version mismatches.

## 2. Codex migration and compatibility

- [x] 2.1 Reorganize the existing Codex plugin as the Codex adapter while preserving its current installation path for the compatibility release.
- [x] 2.2 Map Codex automatic activation, explicit controls, specialist skills, independent Deep review, and handoff reporting to the adapter manifest.
- [x] 2.3 Update Codex installation and migration documentation, including rollback to the prior plugin layout.
- [x] 2.4 Validate the Codex plugin with the plugin validator and evaluate the updated workflow in a fresh Codex thread using the consumer fixture.

## 3. Claude Code adapter

- [x] 3.1 Add a minimal `CLAUDE.md` entry point that imports the shared `AGENTS.md` guidance and contains only Claude-specific activation notes.
- [x] 3.2 Package the baseline workflow and specialist documentation/retrospective workflows in Claude Code's supported skill or plugin layout.
- [x] 3.3 Define and document Claude mappings for Quick/Standard/Deep selection, explicit controls, blocks/overrides, independent review, and degraded-control reporting.
- [x] 3.4 Add Claude adapter validation for layout, frontmatter, import integrity, manifest parity, and no duplicated core policy.
- [ ] 3.5 Run a fresh Claude Code consumer-fixture evaluation and record the activation, depth, documentation-impact, review, and handoff evidence.

## 4. Factory Droid adapter

- [x] 4.1 Add Factory project guidance and `.factory/skills/` artifacts that reference the shared Careful contract.
- [x] 4.2 Package baseline and specialist workflows using Factory's supported skill frontmatter and supporting-file layout.
- [x] 4.3 Define and document Factory mappings for Quick/Standard/Deep selection, explicit controls, blocks/overrides, independent review via a read-only skill or custom droid, and degraded-control reporting.
- [x] 4.4 Add Factory adapter validation for layout, frontmatter, manifest parity, and no duplicated core policy.
- [ ] 4.5 Run a fresh Factory Droid consumer-fixture evaluation and record the activation, depth, documentation-impact, review, and handoff evidence.

## 5. Cross-harness adoption and documentation

- [x] 5.1 Create a cross-harness adoption guide that separates shared project policy, host-specific entry points, private `.careful/` context, and per-user installation steps.
- [x] 5.2 Publish a compatibility matrix with verified version assumptions, control status, intentional degradations, installation instructions, and fixture evidence for Codex, Claude Code, and Factory Droid.
- [x] 5.3 Update the README, design documentation, release guide, project profile, marketplace metadata, and examples to describe Careful as a multi-harness project without promising unsupported agents.
- [x] 5.4 Add migration and rollback guidance for existing Codex users and a clear non-goals section for future adapter requests.

## 6. Fixtures, verification, and release readiness

- [x] 6.1 Add or extend tracked consumer fixture variants for Codex, Claude Code, and Factory Droid using a common substantive-task scenario and adapter-specific entry points.
- [x] 6.2 Extend `scripts/validate_self_hosting.py` to validate the portable core, adapter manifest, all adapter layouts, shared guidance imports, documentation links, and fixture declarations.
- [x] 6.3 Run source validation, Codex plugin validation, adapter-specific static checks, and `openspec validate --all --strict --no-interactive`.
- [x] 6.4 Perform independent adversarial review of parity, unsupported-control reporting, migration safety, private-context boundaries, and documentation claims.
- [ ] 6.5 Update durable OpenSpec specifications, capture implementation evidence and retrospective candidates, and archive the change only after all supported-adapter fixture results are recorded.
