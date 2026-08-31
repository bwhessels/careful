# lightweight-public-readiness Specification

## Purpose
TBD - created by archiving change complete-lightweight-public-readiness. Update Purpose after archive.
## Requirements
### Requirement: Careful declares a lightweight public posture

Careful SHALL declare `public_readiness.audience: public-intended` in its own project profile and SHALL require only `README.md` and `LICENSE` as public-readiness artifacts.

#### Scenario: Profile is evaluated

- **GIVEN** Careful's project profile is loaded
- **WHEN** the public-readiness validator runs
- **THEN** the audience mode is `public-intended`
- **AND** `README.md` and `LICENSE` are required
- **AND** `SECURITY.md` is not required

### Requirement: Public orientation is accurate

Careful SHALL maintain a README that provides accurate public orientation, basic usage or installation guidance, current adapter status, limitations, non-goals, and links to canonical detailed documentation.

#### Scenario: Public reader follows the README

- **GIVEN** a reader starts at `README.md`
- **WHEN** they follow the documented basic path
- **THEN** the repository identity and installation path contain no unresolved owner placeholder
- **AND** the reader can find compatibility, adoption, release, contribution, and license information

### Requirement: Objective checks run in repository CI

Careful SHALL provide one repository-owned GitHub Actions workflow that runs the configured public-readiness checks for pull requests and pushes to `main`.

#### Scenario: A check fails

- **GIVEN** a configured test or validator exits unsuccessfully
- **WHEN** the GitHub workflow runs
- **THEN** the workflow fails
- **AND** the change is not represented as mechanically verified

### Requirement: Maintainer review remains the human gate

Careful SHALL use a documented maintainer review for first publication and releases.

#### Scenario: Maintainer reviews a release

- **GIVEN** the automated checks pass
- **WHEN** the maintainer performs the release review
- **THEN** they verify README accuracy, public claims, limitations, license presence, and documentation impact
- **AND** the result is recorded as maintainer review, not independent review or formal certification

### Requirement: Lightweight scope is explicit

Careful SHALL document that the lightweight public-readiness posture does not establish a security-reporting process, support promise, community governance, or production certification.

#### Scenario: Reader assesses project maturity

- **GIVEN** a reader consults the public project documentation
- **WHEN** they assess project maturity or support expectations
- **THEN** the documentation identifies Careful as maintainer-led and experimental where applicable
- **AND** does not imply that omitted governance artifacts or security processes exist

