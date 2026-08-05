# Deep change checklist

Complete this checklist before implementing a Deep change that creates or modifies a command, initializer, installer, package or plugin distribution, symlink or submodule layout, generated project guidance, or another shared filesystem artifact. For every field, record a concrete decision or `Not applicable` followed by concrete repository evidence.

- **Bootstrap and discovery:** State how each supported environment finds and starts the behavior.
- **Consumer path and reference resolution:** State the stable path consumers use and how references resolve from development and installed layouts.
- **Cloneable source and immutable version:** State the cloneable source identity and immutable revision, release, or equivalent reproducible version.
- **Interactive, dry-run, and non-interactive defaults:** State prompts, unattended defaults, preview behavior, failure behavior, and exit semantics.
- **Tracked, ignored, local, and private state:** State ownership and version-control treatment for every created or linked artifact, including secrets or maintainer-only state.
- **Upgrade, repair, migration, rollback, and destructive boundaries:** State repeat-run behavior, recovery paths, compatibility transitions, rollback, and what may be overwritten or removed.
