---
name: code-simplification
description: "Simplify working code while preserving behavior. Use when code is correct but too complex, duplicated, over-abstracted, hard to review, or carrying dead branches; use after tests exist or when simplification itself can be proven safely."
---

# Code Simplification

Make the correct behavior easier to see.

This skill is adapted from `addyosmani/agent-skills`; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. State the behavior that must not change.
2. Find existing proof: tests, examples, command output, or golden behavior.
3. Delete before abstracting:
   - unused branches
   - duplicate special cases
   - pass-through wrappers
   - abstractions with one caller and no clear invariant
4. Inline or split code when it makes ownership clearer.
5. Keep changes scoped to the simplification target.
6. Rerun the proof that behavior is unchanged.

## When To Stop

Stop when the next simplification would:

- cross an ownership boundary
- require a new public contract
- hide behavior behind a broader abstraction
- widen the diff beyond reviewable scope

Use `design-algorithm` if the issue is the product or command surface rather than code shape.

## Output

Include:

- behavior preserved
- complexity removed
- proof run
- any follow-up deliberately left out of scope

## Checks

- Do not mix simplification with unrelated formatting churn.
- Do not remove comments that document non-obvious invariants unless the invariant is now obvious in code.
