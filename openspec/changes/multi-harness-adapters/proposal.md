## Why

Careful currently ships only as a Codex plugin, even though its workflow contract—evidence labels, proportional review, blocks and overrides, documentation impact, and retrospectives—is largely agent-independent. Claude Code and Factory Droid both support repository guidance and reusable skills, but use different discovery paths and adapter features. Careful needs a portable core with deliberately thin, tested adapters so one behavior does not drift into three separate harnesses.

## What Changes

- Introduce a tool-neutral Careful core contract and a versioned adapter manifest that declares each supported harness’s capabilities, installation layout, activation mechanism, and validation requirements.
- Add first-class Claude Code and Factory Droid adapters alongside the existing Codex distribution, while retaining Codex as a supported adapter rather than the canonical source of workflow behavior.
- Define common project guidance and harness-specific entry points so adopted projects activate the same baseline automatically without duplicating policy.
- Define capability-aware degradation: when a host cannot provide an automatic trigger, independent reviewer, or supported command, Careful reports that limitation rather than claiming the control ran.
- Expand the documentation model with cross-harness installation, compatibility, adapter-authoring, and consumer-adoption guidance.
- Expand fixture validation to prove the shared core and every supported adapter in representative consumer projects.
- **BREAKING**: Reorganize the distributable layout and public naming from a Codex-only plugin structure to a multi-harness distribution. Existing Codex installation instructions will change, with a migration path retained for the initial compatibility release.

Explicit non-goals: workplace governance, centralized telemetry, a hosted control plane, automatic conversion of arbitrary third-party prompts, and support for agents beyond Codex, Claude Code, and Factory Droid in this change.

## Capabilities

### New Capabilities

- `portable-workflow-core`: A single, versioned Careful policy contract and adapter manifest that supported harnesses implement without policy duplication.
- `claude-code-adapter`: Installation, activation, controls, and validation for Careful in Claude Code.
- `factory-droid-adapter`: Installation, activation, controls, and validation for Careful in Factory Droid.
- `cross-harness-adoption`: Project-level adoption, compatibility reporting, and consumer fixtures across supported harnesses.

### Modified Capabilities

- `default-skill-integration`: Generalize default activation, specialist workflows, availability reporting, and final-handoff requirements from Codex-only behavior to capability-aware supported-harness behavior.
- `self-hosting-careful`: Extend the self-hosting profile, fixture obligations, release boundary, and public documentation map to cover all distributed adapters.

## Impact

- Affects the distributable layout currently rooted at `plugins/careful/`, root `AGENTS.md`, marketplace metadata, project profile, fixtures, validation scripts, documentation, and OpenSpec schemas/examples.
- Requires official compatibility research and version-pinned adapter documentation for Claude Code and Factory Droid.
- Does not require a new runtime service or external dependency; consumers install tracked repository artifacts using their chosen agent’s supported discovery mechanism.
