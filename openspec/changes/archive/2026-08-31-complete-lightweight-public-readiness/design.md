# Design: Complete Lightweight Public Readiness for Careful

## Decisions

### 1. Use a deliberately modest publication posture

Careful declares `public_readiness.audience: public-intended`. This means the repository is prepared for public readers and reproducible checking, but does not claim production support, formal governance, or a mature community process.

The required public documents are only:

```yaml
public_readiness:
  audience: public-intended
  required_documents:
    - README.md
    - LICENSE
  checks:
    - python3 -m unittest discover -s tests -v
    - python3 scripts/validate_change_dependencies.py
    - python3 scripts/validate_spec_authority.py
    - python3 scripts/validate_public_readiness.py
    - python3 scripts/validate_self_hosting.py
    - openspec validate --all --strict --no-interactive
  gates:
    first_publication: maintainer-review
    release: maintainer-review
```

The profile does not require `SECURITY.md`. The absence of a security-reporting process remains an explicit project limitation, not an implied promise.

### 2. Keep public orientation in the README

The README remains the canonical orientation document. It must describe the project, basic installation/use, current adapter status, limitations, non-goals, and contribution path without placeholders or unsupported promises.

Existing detailed documents remain canonical for their subjects:

- `docs/compatibility.md` for adapter support claims;
- `docs/adoption.md` for installation and adoption paths;
- `docs/release.md` for the maintainer release procedure;
- `CONTRIBUTING.md` for contributor workflow.

The README links to those documents rather than duplicating their full content.

### 3. Enforce objective checks in one repository workflow

Add a single GitHub Actions workflow that runs the configured tests and validators on pull requests and pushes to `main`. The workflow is repository-owned and may execute the explicitly listed commands. The shared public-readiness validator continues to validate profile structure and required artifacts; it does not execute arbitrary profile commands.

The workflow must fail on command failure. It does not attempt to judge semantic accuracy, legal status, security policy, or maintainer intent.

### 4. Use maintainer review as the human gate

The first-publication and release gate requires the maintainer to verify:

- the README describes the current repository;
- public claims match `docs/compatibility.md` and the implementation;
- limitations and experimental status are visible;
- the MIT license is present;
- the automated checks pass;
- no unresolved change requires a documentation update.

This is intentionally a lightweight human check. It must not be described as independent review or formal certification.

### 5. Keep current Deep-review residual risk explicit

The existing public-readiness and spec-authority changes may record an accepted lightweight maintainer-review posture and unavailable independent review. They must not claim clean independent-review closure. Archival remains contingent on recording the residual risk and verification evidence.

## Verification approach

- Validate the project profile and required documents.
- Run the GitHub workflow commands locally.
- Run strict OpenSpec validation.
- Verify the README contains no repository-owner placeholder.
- Inspect the workflow for the required triggers and commands.
- Perform the maintainer review checklist and record its result in implementation evidence.
