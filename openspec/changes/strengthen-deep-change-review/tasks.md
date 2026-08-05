## 1. Dependency validator

- [ ] 1.1 Add failing unit fixtures for an undeclared predecessor, unknown dependency, self-dependency, and cycle; include passing current-spec and declared-predecessor cases.
- [ ] 1.2 Implement the minimal standard-library dependency parser and validator.
- [ ] 1.3 Integrate the validator into self-hosting validation and declare the initializer's predecessor in `.openspec.yaml`.

## 2. Triggered design completeness

- [x] 2.1 Run and record baseline pressure scenarios against the current workflow skill for distribution-contract omissions.
- [ ] 2.2 Add the triggered checklist to the portable core and Critical Deep design template without duplicating policy in adapters.
- [ ] 2.3 Forward-test the same scenarios in fresh contexts and tighten only observed gaps.

## 3. Clean review closure

- [x] 3.1 Run and record a baseline pressure scenario where material findings were fixed but no clean re-review occurred.
- [ ] 3.2 Add the material-finding clean-pass rule to portable policy and affected workflow adapters.
- [ ] 3.3 Forward-test clean closure, unavailable-review reporting, explicit override, and minor-finding behavior.

## 4. Documentation and verification

- [ ] 4.1 Update design, contributor, validation, and fixture documentation at their canonical locations.
- [ ] 4.2 Validate every changed skill with the skill-creator validator and the Codex plugin with the plugin-creator validator.
- [ ] 4.3 Run unit, self-hosting, strict OpenSpec, adapter parity, and affected fresh-session fixture checks.
- [ ] 4.4 Obtain independent spec-compliance and code/product-quality reviews, correct material findings, and obtain one clean confirmation pass.
- [ ] 4.5 Record implementation evidence, documentation impact, residual risk, and retrospective outcome before archival.
