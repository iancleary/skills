---
name: debugging-and-error-recovery
description: "Investigate failures whose cause is unclear or whose fixes keep failing. Use for difficult test, build, or runtime diagnosis; handle a routine error with an obvious correction directly."
---

# Debugging And Error Recovery

Debug from evidence, not from guesses.

This skill is adapted from `addyosmani/agent-skills`; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. Reproduce the failure with the narrowest command or scenario available.
2. Read the full error and identify the first failing boundary.
3. Localize by tracing backward through the owning code path and adjacent tests.
4. Reduce the case until the suspected cause is isolated.
5. Fix at the ownership boundary where the invariant belongs.
6. Add or update a guard: focused test, validation, clearer error, or docs.
7. Rerun the failing case. Check adjacent behavior when the fix could affect it.

## Build a discriminating feedback command

Make the reproduction detect the user's exact symptom. Record the command,
expected observation, actual observation, and relevant environment. Distinguish
the reported failure from nearby failures such as authentication or setup errors.
Read the owning code as needed to construct the reproduction.

For intermittent failures, record the trigger, number of runs, and observed
failure rate. Control relevant inputs or timing when practical. One passing run
does not establish a fix. Keep stress and instrumentation within the authorized
environment; production probes can require additional permission.

When the cause remains unclear, compare plausible hypotheses using predictions
that distinguish them. Change one relevant variable per probe. For performance
failures, record a baseline and compare the same workload after the change.
Do not manufacture a fixed number of hypotheses when evidence already isolates
the cause.

Before reporting completion, rerun the original scenario and remove temporary
instrumentation added for this investigation. Preserve useful regression proof
and existing user diagnostics. If reproduction is unavailable, state what remains
unverified and continue safe evidence gathering before requesting missing access.

## Stop And Reassess

Stop adding patches when:

- two or more fixes fail for the same reason
- the failure moves without becoming simpler
- the fix requires broad special cases
- the underlying contract is unclear

At that point, restate what is known, what is inferred, and what evidence is missing.
Continue diagnosis within the authorized scope; ask for input only when needed.

## Output

Report the cause or remaining hypothesis, the fix, and verification. Include
a reproduction command when useful to repeat the failure, and residual risk
only when a material uncertainty remains.

## Checks

- Do not hide uncertainty with confident wording.
- Do not fix symptoms when the failing invariant is clear.

The guidance on feedback commands and hypotheses also adapts Matt Pocock's skills.
See [third-party notices](THIRD_PARTY_NOTICES.md) for pinned sources and licenses.
