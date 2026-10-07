---
name: skip-and-prune-tautological-tests
description: "Use when deciding whether to add a suspected tautological test or when asked to audit and prune tautological tests. Distinguish self-confirming assertions from independent behavioral proof; skip new tautologies and rewrite or remove existing ones without losing useful coverage."
---

# Skip and prune tautological tests

## Define tautological before deleting

A **tautological test** asserts something already guaranteed by its own setup or
by repeating the implementation under test. It confirms that the code agrees
with itself, not that the code satisfies an independently defined requirement.
The same defect can affect both the actual and expected values while the test
still passes.

Common examples include:

- Comparing `f(input)` with another call to `f(input)`.
- Computing the expected result with the same production helper or copying the
  production algorithm into the assertion.
- Configuring a mock to return a value, then asserting that the mock returns it
  without exercising the real consumer.
- Asserting that a fixture contains exactly the data the test just put into it.

A weak test is not necessarily tautological. An existence assertion, an empty
result, a mock call, or a constant check can protect a real contract. Classify the
assertion by the defect it detects, not by its syntax. Cheap tests are not
worthless merely because they are cheap.

## Audit the requested scope

1. Identify the requirement each candidate protects and where its expected
   result comes from. Use a specification, worked example, known-good result,
   or independently derived invariant.
2. Trace the assertion back to the subject. Confirm that the test exercises
   production behavior rather than only its fixtures or mocks.
3. Name a plausible production defect that violates the requirement. Ask whether
   the assertion would detect it without changing the expected result.
4. For an uncertain candidate, run a narrow negative control when practical.
   Substitute a wrong result or locally introduce the named defect. Confirm that
   the test fails for that defect, then restore only your temporary change.
   If you cannot run the control safely, report that limit rather than claim proof.
5. Keep, rewrite, skip, or prune using the rules below. Run the focused tests and
   the repository's required checks after changes.

## Choose the action

- **Keep** tests with independent expectations or meaningful relational
  invariants. Round trips, idempotence, table consistency, compile-time checks,
  and interaction contracts can catch real defects. Keep them when they protect
  a requirement; add an independent example if paired implementations could
  share the same mistake.
- **Rewrite** a tautological test when its intended requirement is useful. Call
  the real subject with a concrete input and assert an independently chosen
  output or observable effect. For example, replace
  `expect(slugify(text)).toBe(slugify(text))` with
  `expect(slugify("Hello, World!")).toBe("hello-world")` when that output is the
  specified behavior.
- **Skip adding** a proposed test when its only assertion would be tautological
  and no useful independent check is available. Use an existing contract test,
  focused reproduction, or manual check instead. State any remaining gap.
- **Prune** an existing tautological test when it protects no independent
  requirement and a rewrite adds no useful coverage. Check all its assertions
  before deleting the case. Preserve shared setup needed by retained tests.

Skipping means declining to add a useless test, not marking a failing test as
skipped. Do not delete a test because it fails, exposes a bug, or slows delivery.
Do not change an expected value merely to match the current implementation.
Keep unrelated tests and production code outside the cleanup.

## Report the evidence

List the tests kept, rewritten, or pruned and the reason for each decision.
For a skipped addition, name the alternative verification and any unverified
behavior. Report the checks run, their results, and any negative-control evidence.
