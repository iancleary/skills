---
name: architecture-review
description: "Review a bounded codebase area for architectural friction and propose owner-scoped interface improvements when explicitly requested."
---

# Architecture Review

Use only for an explicit architecture review request. Return concrete opportunities
and their proof requirements. An assessment alone does not authorize a refactor.

## Scope and evidence

Start with the named repository, area, or pain point. If the request names no
area, use recent change history and reported friction to choose a bounded scope.
Read applicable owner instructions, existing interfaces, and relevant decisions.
State the scope and the evidence used to choose it.

For work spanning repositories, identify the owner of each behavior. Delegate
bounded owner investigations when worthwhile and available. Keep implementation
context with that owner; the lead integrates the returned interface evidence.
A shared interface does not transfer ownership of its implementation.

## Evaluate candidates

Look for repeated caller coordination, scattered changes for one behavior,
leaked configuration or error handling, and interfaces that obstruct meaningful
verification. Cite concrete callers, code, or change history for each candidate.
Treat those patterns as leads, not findings by themselves.

Ask what a caller must learn now and after the change. Identify complexity the
owner can absorb and obligations the caller must retain. Preserve domain units,
error semantics, and private implementation boundaries. Compare alternatives
only when they resolve a real tradeoff; another abstraction is not always needed.

Respect existing design decisions. Propose revisiting one only when new evidence
shows a concrete cost. Do not infer that fewer files, more implementation code,
or more adapters means a better design. Preserve independent test coverage when
changing the interface under test.

## Output and acceptance

Return a short ranked set of findings, each with:

- Owner and specific evidence of friction.
- Proposed interface change and caller-visible benefit.
- Compatibility, migration cost, and significant alternatives.
- The owner-run proof needed before acceptance, including any runtime limits.

A result with no worthwhile change is valid. Use a diagram when it clarifies a
relationship; a visual report or interview is optional. Clearly separate evidence
from design hypotheses. If implementation is also authorized, turn the selected
finding into a bounded owner assignment with acceptance criteria.

Adapted from Matt Pocock's architecture and interface-design skills. See
[third-party notices](THIRD_PARTY_NOTICES.md) for pinned sources and MIT notice.
