## Why

Careful has a self-hosting specification, but its profile was not fully actionable and the repository lacked a portable check proving the public/private boundary and external-consumer fixture contract. The specification must describe current reality before it can be treated as a living main spec.

## What Changes

- Make the tracked self-hosting profile portable and declare its fixture project.
- Teach the main workflow to consume the profile and avoid private `.careful/` context by default.
- Add deterministic self-hosting validation and release guidance.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `self-hosting-careful`: Implement the profile, private-context boundary, fixture validation, and release refresh requirements.

## Impact

Affected project profile, main workflow, public design/release documentation, validation scripts, and the self-hosting specification.
