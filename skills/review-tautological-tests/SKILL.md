---
name: review-tautological-tests
description: "Use before expanding tests after an implementation or when asked to review and prune unnecessary existing tests. Identify tautological assertions and redundant coverage, add only checks for distinct behavioral risks, and preserve meaningful regression protection."
---

# Review tautological tests

Use this workflow in two situations:

- After writing code, avoid adding tests merely because more cases can be written.
  Identify what existing tests leave unverified before expanding the suite.
- When reviewing an existing suite, repair or prune assertions that provide no
  independent check, and remove redundant cases when retained tests cover the risk.

The goal is sufficient evidence for the changed behavior, not a larger or smaller
suite. Keep the review within the requested scope. Reviewing a proposed addition
is not permission to clean up unrelated tests.

## Define tautological precisely

A **tautological assertion** checks a claim that follows from the test's own
setup or from reusing the value being checked, rather than from an independent
expectation about the behavior. Its success does not establish the intended
behavior. A test can contain both tautological and meaningful assertions.

An expectation is independent when its justification does not depend on the
implementation decision being checked. A literal copied from current output is
not automatically independent. A calculated expectation can be independent when
it follows from a separately justified specification or invariant.

Distinguish these cases before acting:

- Comparing a value with itself provides no independent check of its correctness.
  Comparing two calls to `f(input)` may check repeatability, but does not establish
  that either result is correct.
- Computing the expected result with the production algorithm creates circular
  evidence for that algorithm's correctness. A copied algorithm may still detect
  divergence. Identify that narrower protection before replacing it.
- Asserting a configured mock's return value without exercising its consumer
  checks the setup, not the consumer. Exercising the real consumer and checking
  its output or a required interaction can protect behavior.
- Reading back fixture data just assigned by the test checks the setup. Validating
  a shared fixture against an external schema can protect a separate requirement.
- A redundant test may have valid, independent assertions but add no distinct
  protection beyond retained tests. Redundancy is not tautology.

Do not classify tests by assertion syntax, size, or use of mocks. Empty results,
constant checks, round trips, idempotence, compile-time checks, and interaction
checks can protect real requirements. Missing one defect does not make a test
worthless.

## Before adding more tests

1. Name the changed behavior and plausible defects that matter to its contract.
2. Inspect existing checks for that behavior. Identify the specific gap each
   proposed test would close, including a distinct boundary or failure mode.
3. Choose the smallest set of cases that covers those gaps. Do not generate a
   case for every helper, branch, or input variation without a behavioral reason.
4. Derive expectations from the requirement, a worked example, or a trusted
   reference. Explain why recorded output is trusted before using it as an oracle.
5. Add and run the focused checks. Stop expanding when the identified risks have
   executable evidence and required repository checks pass. Broaden only for a
   newly identified risk, a failure, or a repository requirement.

Decline a proposed addition that only repeats setup or existing protection.
If a relevant risk remains but no practical independent test is available, use a
focused reproduction or manual check and report the gap. Do not call that risk
covered merely because adding a test is inconvenient.

## Review existing tests before pruning

1. Identify the requirement and expected-result source for each candidate
   assertion. Trace what production behavior or contract it actually exercises.
2. Name a plausible defect it detects. For suspected redundancy, identify the
   retained test that covers the same risk. Similar outputs alone do not prove
   duplication across different boundaries or failure modes.
3. If evidence is uncertain, run a narrow negative control when practical.
   Introduce a defect relevant to the requirement without changing the expectation.
   Record whether the test detects it, then restore only your temporary change.
   A failure shows sensitivity to that defect. A pass shows a gap for that defect,
   not that the entire test is tautological. If uncertainty remains, keep the test
   and report what could not be established.
4. Keep assertions that protect relevant behavior. Rewrite a circular assertion
   when its intended requirement otherwise lacks protection. For example, use
   `expect(slugify("Hello, World!")).toBe("hello-world")` when that output follows
   from the contract, rather than comparing two calls to `slugify`.
5. Remove an assertion only after explaining why it adds no independent check or
   which retained test covers its risk. Remove a whole case only after inspecting
   all its assertions and any execution-only checks, such as a no-error contract.
   Preserve shared setup used by retained tests.
6. Run the focused tests and required repository checks. A passing suite after
   deletion does not establish that coverage was preserved; the removal rationale
   must account for the protection lost or retained.

Skipping an addition does not mean disabling an existing test. Do not remove a
check because it fails, exposes a bug, or slows delivery. Do not change expected
values merely to match implementation. Keep unrelated tests and production code
outside the cleanup, apart from temporary negative controls that you restore.

## Report the evidence

For additions, name the distinct risk each new test covers. For rewrites and
removals, state the assertion's claim, the evidence for the decision, and any
retained protection. Report verification commands, results, and unresolved gaps.
Summarize retained tests unless a particular decision needs explanation. Do not
use test counts, coverage percentages, or a green suite alone as proof of quality.
