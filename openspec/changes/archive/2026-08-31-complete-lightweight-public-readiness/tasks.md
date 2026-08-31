## 1. Configure the lightweight project contract

- [x] Update `careful.project.yaml` with `public_readiness.audience: public-intended`, required documents `README.md` and `LICENSE`, the configured validation commands, and `maintainer-review` publication/release gates.
- [x] Add tests proving Careful's profile passes lightweight public-readiness validation and does not require `SECURITY.md`.

## 2. Repair public orientation

- [x] Replace the README repository-owner placeholder with the canonical Careful repository URL.
- [x] Update the README with concise status, limitations, non-goals, and links to canonical adoption, compatibility, release, contribution, and license documentation.
- [x] Update contributor and release guidance to describe the lightweight maintainer-review gate without claiming independent review or formal certification.

## 3. Add repository enforcement

- [x] Add one GitHub Actions workflow that runs the configured tests and validators on pull requests and pushes to `main`.
- [x] Verify the workflow fails when a required command fails and does not execute undeclared arbitrary project commands.

## 4. Verify and record the release posture

- [x] Run the complete Careful validation suite, strict OpenSpec validation, plugin validation, and documentation/link checks.
- [x] Perform and record the lightweight maintainer review for first publication, including README accuracy, public claims, limitations, license presence, and documentation impact.
- [x] Record the accepted residual risk that formal independent review and a security-reporting process are intentionally out of scope; do not claim clean independent-review closure.
- [x] Archive the completed lightweight public-readiness change and update any superseded active-change evidence only after all verification records are present.
