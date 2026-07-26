## Context

Careful's public contract is already conceptually portable, but its source tree and adoption guidance are Codex-specific: the distribution is a Codex plugin, default activation is stated in `AGENTS.md`, and validation only models Codex consumers. This produces policy duplication if Claude Code and Factory Droid are added by copying the current skills.

The three hosts have overlapping but not identical primitives. Codex distributes plugin skills and reads project `AGENTS.md`. Claude Code reads `CLAUDE.md`, supports project/plugin skills, and documents an `@AGENTS.md` import for mixed-agent repositories ([memory](https://code.claude.com/docs/en/memory), [skills](https://code.claude.com/docs/en/skills)). Factory Droid reads `AGENTS.md`, discovers project skills in `.factory/skills/`, and supports automatic or slash invocation ([guidance](https://docs.factory.ai/cli/getting-started/how-to-talk-to-a-droid), [skills](https://docs.factory.ai/cli/configuration/skills)).

## Goals / Non-Goals

**Goals:**

- Preserve one canonical, versioned Careful policy across Codex, Claude Code, and Factory Droid.
- Deliver native-feeling adapters using each host's documented project guidance and skill mechanisms.
- Make adapter capability differences explicit and safely degradable.
- Keep public distributable artifacts, private `.careful/` context, specs, and consumer fixtures clearly separated.
- Make the adapter system extensible without promising unimplemented hosts.

**Non-Goals:**

- Cross-agent transcript sharing, background service orchestration, centralized governance, or telemetry.
- A generic compatibility claim for every agent that happens to read Markdown instructions.
- Forcing identical commands, subagent models, permission systems, or marketplaces across hosts.
- Replacing OpenSpec or each host's native planning/review features.

## Decisions

### 1. Adopt a core-plus-adapter layout

Create a tracked `core/` area containing a human-readable policy contract, reference templates, and a versioned adapter manifest. Create `adapters/codex/`, `adapters/claude-code/`, and `adapters/factory-droid/` as thin renderings of that contract. Each adapter may contain host-specific discovery metadata and instructions, but must link to the core for shared policy rather than copy it.

**Why:** One policy source prevents divergence while preserving native layouts. Both Claude and Factory support focused `SKILL.md` bundles with supporting resources, so shared references can remain concise and load on demand.

**Alternatives considered:**

- Copy three complete skill sets: rejected because fixes and policy updates would drift.
- A runtime generator that materializes adapter files during installation: rejected for the first release because it adds an execution dependency and makes review of shipped instructions harder.
- One universal `AGENTS.md` only: rejected because Claude Code needs a `CLAUDE.md` entry point and all hosts need explicit specialist-task discovery.

### 2. Define capability contracts, not fake parity

The adapter manifest SHALL declare, per adapter: project-guidance entry point, distribution mechanism, automatic baseline trigger, explicit controls, specialist-task trigger, independent-review mechanism, validation command(s), and any unavailable control. The common core specifies the observable outcome; the adapter defines how it reaches that outcome.

If a required control cannot be executed natively, the adapter SHALL state the limitation at handoff and provide the nearest supported recovery path. It SHALL not report a control as completed merely because similar prose was present in an instruction file.

**Why:** Factory supports project skills and custom review droids; Claude supports skills and custom subagents; their invocation/permission semantics differ. Compatibility must be evidence-based.

**Alternatives considered:**

- Require every host to expose exactly the same features: rejected because it would exclude supported hosts for incidental differences.
- Silently omit unsupported features: rejected because it violates Careful's evidence and handoff contract.

### 3. Use one shared project guidance source with host shims

The repository SHALL publish `AGENTS.md` as the tool-neutral project guidance. Codex and Factory adapters use it directly. The Claude adapter SHALL publish a small `CLAUDE.md` that imports `@AGENTS.md` and contains only Claude-specific activation notes. It SHALL not duplicate the common policy.

**Why:** Factory documents `AGENTS.md` as automatic project guidance, while Claude documents the import mechanism specifically for repositories that already use `AGENTS.md`.

### 4. Preserve three workflow depths and explicit controls semantically

Quick, Standard, Deep; evidence labels; blocks and overrides; documentation impact; independent Deep review; and retrospective proposals remain core semantics. Adapter command names may differ. Each adapter maps the core's explicit controls to documented host affordances (skill command, prompt phrase, or documented fallback) and documents the mapping.

**Why:** Workflow meaning is more important than command spelling. Factory maps commands into skills, and Claude exposes skill names as commands, but neither requires Careful to imitate Codex syntax.

### 5. Validate source, rendering, and behavior separately

Validation has three layers: (1) deterministic core/manifest checks, (2) adapter layout and syntax checks using each host's documented format where tooling exists, and (3) consumer fixtures that exercise a representative substantive request in a fresh host session. Fixtures record evidence of activated guidance, chosen depth, documentation outcome, review behavior, and any declared degradation.

**Why:** A valid Markdown file does not demonstrate automatic discovery or behavior. Fresh-session validation avoids relying on stale, already-loaded instructions.

### 6. Migrate Codex incrementally

Keep `plugins/careful/` as a compatibility package for the first multi-harness release, but make it a Codex adapter generated or maintained from the shared core. Mark the old direct layout as deprecated in release documentation, publish migration instructions, and remove compatibility only through a future approved OpenSpec change.

## Risks / Trade-offs

- **Host documentation or feature changes** → Pin verified support claims to documentation dates/version assumptions, expose an adapter compatibility matrix, and revalidate before releases.
- **Core becomes an oversized prompt** → Keep the core normative and concise; place detailed templates in referenced files and host-specific mechanics in adapters.
- **Adapters drift despite shared core** → Validate the manifest, require an adapter parity checklist, and require a fixture result for every changed shared policy rule.
- **Native automatic invocation is probabilistic** → Treat the guide/skill as an activation request, provide explicit controls, and report missing activation rather than silently asserting it.
- **Claude/Factory include tool semantics that do not map to Codex** → Keep permissions and subagent configuration adapter-local; core defines required outcomes and evidence, not tool grants.
- **Migration disrupts current Codex users** → Retain the existing package for one compatibility release and document direct migration/rollback.

## Migration Plan

1. Introduce the core contract, manifest, adapter directories, documentation, and fixtures without removing the existing Codex package.
2. Port Codex to consume the core while preserving its current installation path; validate fixture behavior in a fresh Codex thread.
3. Add Claude Code and Factory Droid adapters with pinned compatibility documentation and fixture validation.
4. Publish the compatibility matrix and migration guide; release all three adapters together.
5. On failure, retain the last released Codex package and mark an adapter unsupported rather than publishing a partial parity claim. No user project state is migrated automatically.

## Open Questions

- Which minimum Claude Code and Factory Droid versions will Careful support at initial release?
- Should adapters be manually maintained with parity tests or rendered from a checked-in source template? The first implementation should choose based on a prototype's reviewability and validation reliability.
- What is the smallest reliable fixture interaction that demonstrates actual automatic activation, rather than only file discovery, for each host?
- Should independent Deep review be a built-in host review feature, a custom subagent/droid, or a manual second-session procedure per adapter?
