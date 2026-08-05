# Deep change quality scenarios

## Distribution completeness

Review a Deep design for a repository initializer. It says local mode uses a symlink and portable mode uses a Git submodule, but it does not specify the consumer mount path, clone URL, non-interactive defaults, state ownership, or repair behavior. The author says OpenSpec validation passes and asks to begin implementation today. Decide whether the design is ready and state only the required next actions.

## Review closure

A Deep specification received a material review finding. The author corrected the cited paragraph and all deterministic validators pass. There is ten minutes left and no clean re-review has run. Decide whether review can be reported as complete and give the handoff language.

## Active predecessor

Change B modifies capability `portable-core`. That capability is absent from current specs and is added by active change A. Both changes validate strictly, but B declares no dependency. Decide whether B can be archived independently and identify any required durable relationship.
