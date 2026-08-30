## 1. Portable authority contract

- [x] 1.1 Extend the project-profile schema and example with `documentation.spec_authority` and `documentation.execution_plans`.
- [x] 1.2 Add the authority-resolution and execution-plan separation rules to `core/policy.md`.
- [x] 1.3 Add the duplicate-detection and non-destructive migration guidance to the portable workflow references.

## 2. Distributed workflow guidance

- [x] 2.1 Update `careful-documentation` to route durable facts through the declared authority and to distinguish plans from specifications.
- [x] 2.2 Update `careful-workflow` and adoption guidance to detect unknown or conflicting specification authorities.
- [x] 2.3 Update the Codex plugin and supported adapter guidance without duplicating normative policy.

## 3. Verification and fixtures

- [x] 3.1 Add unit fixtures for OpenSpec, project-defined, none, unknown, linked-plan, duplicate, historical, and pointer cases.
- [x] 3.2 Add self-hosting consumer fixtures proving authority resolution from a fresh project context.
- [x] 3.3 Add validation that changed skills, plugin manifests, and adapter references remain consistent.

## 4. Migration and documentation

- [x] 4.1 Update Careful design, contributor, adoption, and release documentation with the single-authority rule.
- [x] 4.2 Migrate the SBX project’s public-readiness design into its OpenSpec authority and remove the duplicate Superpowers spec.
- [ ] 4.3 Obtain independent Deep specification-compliance and code/product-quality reviews; correct material findings and obtain a clean confirmation pass.
- [ ] 4.4 Record implementation evidence, documentation impact, retrospective outcome, and release checks before archival.
