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
  spec_authority: openspec
  execution_plans: docs/superpowers/plans/
```

`documentation.spec_authority` may be `openspec`, `project-defined`, or `none`. Use `project-defined` only when the project identifies its canonical specification location or command. Use `none` only when the project explicitly chooses not to maintain durable specifications. For an absent value, report the authority as unknown and ask the owner when it materially changes the workflow.

`documentation.execution_plans` identifies an execution-plan location. When a durable specification authority exists, execution plans must link to that authority and must not become a second source of requirements or decisions.

For existing projects, preserve conventions. Mark discovered values as verified only when supported by repository evidence; otherwise mark them inferred in the adoption summary and ask only material follow-up questions. If a declared authority has a competing durable-looking specification path, report the conflict and do not delete, overwrite, archive, or merge files without explicit owner direction.
