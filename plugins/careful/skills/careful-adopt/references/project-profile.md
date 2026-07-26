# Project profile

Keep profiles small and factual. Store a project profile only after the user accepts it.

```yaml
version: 1
project:
  name: <name>
  maturity: new | adopted
commands:
  test: <command>
  lint: <command>
  typecheck: <command>
risk_boundaries:
  - <public_api | data | security | architecture | product>
documentation:
  readme: README.md
  specs: openspec/specs/
  changes: openspec/changes/
  architecture: docs/architecture/
  decisions: docs/architecture/decisions/
  development: docs/development/
  reference: docs/reference/
```

For existing projects, preserve conventions. Mark discovered values as verified only when supported by repository evidence; otherwise mark them inferred in the adoption summary and ask only material follow-up questions.
