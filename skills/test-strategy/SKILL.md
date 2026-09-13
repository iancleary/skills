---
name: test-strategy
description: "Choose focused verification when test scope, regression coverage, or the right proof is unclear. Use for meaningful testing decisions; follow an established check directly for routine edits."
---

# Test Strategy

Use tests as proof, not ceremony.

This skill is adapted from `addyosmani/agent-skills` `test-driven-development`,
with a softer test-strategy contract; see `THIRD_PARTY_NOTICES.md` for upstream
provenance and MIT license notice.

## Workflow

1. Identify the behavioral risk and the smallest meaningful seam.
2. Prefer a failing regression test before the fix when the bug is reproducible and the seam is clear.
3. Use the cheapest test that proves the behavior:
   - unit test for pure logic and parsing
   - integration test for command contracts, persistence, IO, or tool boundaries
   - smoke/live check for installed or external behavior when local proof is insufficient
4. Keep tests DAMP enough that the expected behavior is visible.
5. Avoid asserting private implementation details unless the implementation is the contract.
6. Run the focused proof and required repository checks. Broaden only when the
   change, failures, or remaining uncertainty justify it.

## When Not To Force TDD

Do not invent a failing test first when:

- the change is docs-only
- the behavior is better proven by an existing contract test
- the seam is unclear and a small repro should come first
- the test would be more brittle than the production behavior

Still leave proof in the final report.

## Output

Report the verification result and material gaps. Explain the chosen test seam
when that decision needs justification.

## Checks

- Do not use snapshot churn as proof of correctness.
- Do not mock the exact behavior that needs verification.
