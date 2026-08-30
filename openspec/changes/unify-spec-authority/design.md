# Design: Unify Durable Specification Authority

## Context

Careful’s current project profile identifies documentation locations but not which location owns durable specifications. Its policy says OpenSpec is the durable Deep-change record, while generic architectural planning guidance can independently require a design file under `docs/superpowers/specs/`. The absence of an authority-resolution rule allows duplicate specifications without violating either workflow in isolation.

## Decisions

### 1. Declare the authority in the project profile

Add an optional `documentation.spec_authority` field and an optional `documentation.execution_plans` field:

```yaml
documentation:
  specs: openspec/specs/
  changes: openspec/changes/
  spec_authority: openspec
  execution_plans: docs/superpowers/plans/
```

Supported authority values are `openspec`, `project-defined`, and `none`. `project-defined` requires a configured canonical path or command; `none` means the project does not maintain durable specifications and must still record that decision during adoption. An unconfigured project remains `Unknown` until adoption evidence or owner direction establishes the authority.

### 2. Make authority resolution normative

The portable policy SHALL resolve the project’s declared authority before creating a proposal, design, requirements document, or change record. When `spec_authority: openspec` is present, OpenSpec owns durable specifications and change history. Careful and Superpowers execution plans may link to OpenSpec but SHALL NOT create a second durable specification under `docs/superpowers/specs/`.

When no durable authority is configured, the workflow may use the project’s existing convention or create the adapter’s normal design artifact, but it must record that choice in the project profile. This preserves compatibility for projects without OpenSpec.

### 3. Separate durable specifications from execution plans

`docs/superpowers/plans/` remains a supported location for bite-sized implementation plans. Plans SHALL identify the canonical specification they implement. They may summarize constraints needed for execution, but the canonical requirements and decisions remain in the authority document.

`docs/superpowers/specs/` is not a default Careful location. If an existing project uses it as its declared authority, Careful may preserve that convention through `project-defined`; if another authority is declared, adoption and review report the path as a possible duplicate.

### 4. Detect conflicts without destructive migration

Adoption, Deep planning, and public/release review SHALL inspect configured and conventional specification locations. A conflict exists when a project declares one authority and contains another durable-looking specification that is not explicitly marked as historical, a pointer, or an execution plan.

The workflow SHALL report the conflict with:

- declared authority;
- discovered competing path;
- evidence that the path contains durable specification content;
- recommended migration or pointer action;
- owner decision required before deletion or archival.

Careful SHALL not delete, overwrite, or silently merge the competing document.

### 5. Keep distributed adapters thin

The normative authority-resolution rule belongs in `core/policy.md` and the portable workflow/reference material. The Careful plugin’s documentation skill and host adapters SHALL point to that rule and shall not copy competing policy prose. Adapter-specific guidance may explain how to locate the project profile and OpenSpec, but it must not introduce a second canonical location.

### 6. Test at source and consumer boundaries

Tests and fixtures SHALL cover:

- OpenSpec as declared authority;
- a project-defined authority;
- no durable authority;
- an unclassified project requiring adoption clarification;
- a valid execution plan linking to OpenSpec;
- a conflicting `docs/superpowers/specs/` artifact;
- an explicitly historical or pointer document that is not treated as a conflict;
- refusal to perform destructive automatic migration.

Self-hosting validation SHALL exercise the real project profile and at least one adopted consumer fixture.

## Risks and mitigations

- **Existing projects rely on `docs/superpowers/specs/`.** Preserve it when declared as `project-defined`; only report conflicts when another authority is declared.
- **Plans duplicate requirements.** Require a canonical-spec link and have review treat unlinked durable-looking plan content as a drift risk.
- **Generic external workflow guidance remains inconsistent.** Add an explicit project-profile authority rule and adapter guidance; a separate Superpowers source change may be proposed if its maintainers want the generic convention changed.
- **Detection produces false positives.** Use configured paths, explicit historical/pointer markers, and reviewer confirmation rather than filename-only deletion or migration.
