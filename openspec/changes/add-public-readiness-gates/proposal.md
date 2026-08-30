# Proposal: Add Project-Specific Public-Readiness Gates

## Why

Careful currently assesses documentation impact, but it does not distinguish internal documentation completeness from readiness for external publication. A project can pass its implementation workflow while lacking the public orientation, usage, security, contribution, or legal information expected by its intended audience.

## What changes

- Add a project-configured public-readiness contract.
- Support project-specific audience modes, canonical public documents, checks, and publication/release gates.
- Require public-impact classification and evidence at change completion.
- Add mechanical checks for objective documentation invariants and an independent reviewer contract for semantic freshness and consequential decisions.
- Add whole-repository first-publication and release review guidance.

## Non-goals

- Automatically choose licenses, privacy notices, support promises, or publication status.
- Replace legal, security, code, or maintainer review.
- Require the same public documents for every project.
- Make a private project public or migrate documents without owner approval.

## Impact

This affects the portable workflow policy, project profile, documentation skill, distributed plugin guidance, fixtures, and Careful release documentation. It does not add a runtime service or external dependency.
