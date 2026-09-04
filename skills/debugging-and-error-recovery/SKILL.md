---
name: debugging-and-error-recovery
description: "Reproduce, localize, reduce, fix, and guard failures. Use when tests fail, builds break, commands error, behavior is unexpected, or repeated fix attempts are failing and the agent needs a disciplined root-cause workflow instead of more patches."
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
7. Rerun the failing command and a small adjacent check.

## Stop And Reassess

Stop adding patches when:

- two or more fixes fail for the same reason
- the failure moves without becoming simpler
- the fix requires broad special cases
- the underlying contract is unclear

At that point, restate what is known, what is inferred, and what evidence is missing.

## Output

Include:

- reproduction command
- root cause or strongest remaining hypothesis
- fix boundary
- proof command
- residual risk

## Checks

- Do not hide uncertainty with confident wording.
- Do not fix symptoms when the failing invariant is clear.
