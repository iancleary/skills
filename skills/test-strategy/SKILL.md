---
name: test-strategy
description: "Choose and implement focused verification for features, bug fixes, refactors, and regressions. Use when deciding what to test, where to test it, whether TDD is worthwhile, how much coverage is enough, or how to prove behavior without over-testing internals."
---

# Test Strategy

Use tests as proof, not ceremony.

This skill is adapted from `addyosmani/agent-skills` `test-driven-development`, but Forge uses a softer test-strategy contract; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. Identify the behavioral risk and the smallest meaningful seam.
2. Prefer a failing regression test before the fix when the bug is reproducible and the seam is clear.
3. Use the cheapest test that proves the behavior:
   - unit test for pure logic and parsing
   - integration test for command contracts, persistence, IO, or tool boundaries
   - smoke/live check for installed or external behavior when local proof is insufficient
4. Keep tests DAMP enough that the expected behavior is visible.
5. Avoid asserting private implementation details unless the implementation is the contract.
6. Run the focused test, then the broader check appropriate to the blast radius.

## When Not To Force TDD

Do not invent a failing test first when:

- the change is docs-only
- the behavior is better proven by an existing contract test
- the seam is unclear and a small repro should come first
- the test would be more brittle than the production behavior

Still leave proof in the final report.

## Output

Include:

- risk being tested
- test seam chosen
- command run
- remaining test gap, if any

## Checks

- Do not use snapshot churn as proof of correctness.
- Do not mock the exact behavior that needs verification.
