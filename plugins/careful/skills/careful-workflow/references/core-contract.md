# Core contract

## Evidence

Use these labels only for consequential statements:

- **Verified**: backed by code, a test, a primary source, or a cited external source.
- **Inferred**: conclusion from available evidence.
- **Assumption**: must be confirmed or deliberately accepted.
- **Unknown**: not yet investigated.

Research time-sensitive or consequential external claims. Do not imply that a source supports more than it does.

## Private context

Treat `.careful/` as private local maintainer context. Do not read, modify, quote, or copy it into tracked artifacts unless the user explicitly requests it. Public conclusions must rely on tracked repository evidence.

## Challenge and blocks

For a consequential decision, consider alternatives privately and present the recommended path with a short rationale. Block only when proceeding presents material harm, incompatible requirements, or insufficient evidence for an irreversible choice.

```text
BLOCKED: <decision>
Why: <material risk or contradiction>
Evidence: <concrete evidence or missing evidence>
Recommended alternative: <one path and why>
Unblock: <decision, investigation, or verification>
```

An override is valid. Record the user rationale and accepted risk, then proceed without claiming the risk is solved.

## Deep workflow

Deep work requires a durable change record when OpenSpec is initialized:

```text
proposal → research/evidence → adversarial review → design → tasks
         → implementation evidence → retrospective → archive
```

Use an independent reviewer after implementation. It must separately check decision/spec compliance and code/product quality.

## Final handoff

Keep the handoff concise, with these sections when applicable:

1. Outcome and deliberate non-goals.
2. Evidence: tests, commands, sources, and inspected areas.
3. Claim status: material inferences, assumptions, or unknowns.
4. Review: strongest objection, residual risk, and accepted overrides.
5. Decisions or next steps that require the user.

For substantive work, also state the documentation-impact result. When a retrospective signal occurred, state either that no high-signal lesson candidate was found or present each candidate with suggested scope and trade-off.
