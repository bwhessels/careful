# Design: Project-Specific Public-Readiness Gates

## Decisions

### 1. Configure public audience and canonical documents per project

Add an optional project-profile section:

```yaml
public_readiness:
  audience: public-intended
  required_documents:
    - README.md
    - LICENSE
    - SECURITY.md
    - CONTRIBUTING.md
  canonical_documents:
    orientation: README.md
    development: CONTRIBUTING.md
    security: SECURITY.md
    public_contract: docs/reference/
  checks:
    - npm run docs:check
  gates:
    first_publication: independent-review
    release: independent-review
```

Supported modes are `private`, `internal`, `public-intended`, and `public`. An unclassified project remains `Unknown` until adoption evidence or owner direction establishes its audience. Careful must not silently classify a project as public.

Required documents and checks are project-owned. Careful validates their configuration and records results; it does not impose a universal file list.

### 2. Add a change-time public documentation decision

For Standard and Deep work, classify whether the change affects public behavior, installation, configuration, compatibility, security/privacy/operational claims, contributor workflow, or supported status. When it does, name the affected canonical document or record an evidence-backed no-impact result.

For `public` and `public-intended` projects, a no-impact result must identify the checked public contract and evidence; the phrase “no README change required” alone is insufficient.

### 3. Combine mechanical checks with independent review

The mechanical verifier checks configured paths/URLs, links, commands, generated references, and profile consistency. The independent reviewer evaluates semantic accuracy, usability, limitations, risk communication, license/support/disclosure decisions, and drift from repository behavior.

Neither layer substitutes for the other. Missing required evidence or failed configured checks block the gate. Semantic uncertainty is recorded as residual risk or an unresolved owner decision.

### 4. Gate first publication and releases using whole-repository evidence

First-publication and release review evaluates the repository as a whole, not only the current diff. It verifies required artifacts, configured checks, public claims, limitations, and explicit owner decisions. Overrides require rationale and accepted risk; they do not claim the risk is resolved.

### 5. Preserve project ownership

Careful may identify missing legal, privacy, support, or product-positioning decisions, but it must not invent them. It must not create, delete, overwrite, merge, or publish project artifacts without explicit authorization.

## Verification approach

Fixtures must cover all audience modes, custom document locations, missing documents, broken links, failed checks, updated and no-impact public changes, unresolved decisions, overrides, first publication, and release gates. The mechanical verifier must be testable independently from the semantic reviewer.
