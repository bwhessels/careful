# Proposal: Add Evidence Ledger and Change-Impact Analysis

## Why

Careful requires evidence-led claims and documentation-impact assessment, but the current contract leaves both activities primarily in agent prose. Evidence can be repeated without a stable source, become stale, or disappear between a design, implementation, review, and final handoff. Separately, Careful can detect some specification-authority and active-change dependency problems, but it does not provide a general impact map from changed files to capabilities, documentation, adapters, or consumer fixtures.

This makes the workflow inspectable in principle but difficult for Careful to audit autonomously, reuse across review and release steps, or use as feedback for its own decisions.

## What Changes

Add two related capabilities:

1. An optional, repository-local evidence ledger that records consequential claims, their classification, supporting evidence, scope, freshness, and linked OpenSpec requirements.
2. Deterministic change-impact analysis that identifies affected capabilities and validation surfaces from the repository diff and project profile, then reports missing or stale specification, documentation, adapter, and fixture updates.

The capabilities should let Careful audit its own claims and affected surfaces, incorporate assessment outcomes into routing and verification, and flag only material findings or decisions that require the user. They should improve final handoffs, Deep reviews, public-readiness checks, and release preparation while preserving project ownership and the existing proportional Quick/Standard/Deep workflow.

## Non-goals

- A hosted evidence database, centralized telemetry, or cross-project learning service.
- Automatic trust scoring or a numeric probability assigned to claims.
- Treating an evidence record as proof without inspecting its referenced source.
- Requiring the user to manually inspect every ledger record or impact mapping.
- Automatically editing, deleting, migrating, or archiving project specifications or documentation.
- Replacing OpenSpec, project-defined specification authorities, project tests, or independent review.
- Requiring a ledger for every Quick task or every low-consequence statement.
- Inferring semantic impact solely from filenames when stronger repository evidence is unavailable.

## Impact

This is a public workflow-contract change affecting the portable policy, project profile/documentation model, OpenSpec integration, distributed skills, validation scripts, release guidance, and consumer fixtures. It adds repository-local artifacts and reports but no runtime service or external dependency.

## Assumptions and unknowns

- **Verified:** Careful already defines four claim classifications, documentation-impact checks, OpenSpec authority, adapter manifests, fixture requirements, and public-readiness checks.
- **Verified:** Careful projects may use OpenSpec, another project-defined authority, or no durable specification authority.
- **Inferred:** A structured ledger is most useful when created only for consequential claims, linked to existing change artifacts rather than becoming a second requirements system, and evaluated by Careful as part of the workflow.
- **Assumption:** A normalized YAML or Markdown-ledger representation is sufficient for the first release; the exact serialization should follow the project’s configured conventions.
- **Unknown:** Whether future hosts can expose a reliable machine-readable changed-file set; the first contract must support an explicit diff input or repository working-tree inspection.
