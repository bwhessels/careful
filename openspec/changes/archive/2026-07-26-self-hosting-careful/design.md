## Decisions

- Keep `careful.project.yaml` tracked and portable; it must not reference a developer-specific filesystem location.
- Put deterministic repository checks in a standard-library Python script so the self-hosting contract can be validated without a framework-specific runtime.
- Treat `.careful/` as an ignored, optional local context boundary and state that boundary in the main workflow.
- Validate activation guidance in both Careful's root and an external adopted-project fixture.
- Document the fresh-thread rule as a release step because loaded skills cannot be behaviorally re-evaluated in their authoring thread.

## Validation

Run the portable self-hosting validator, strict OpenSpec validation, plugin validation where available, and Git ignored-file inspection.
