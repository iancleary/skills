---
name: api-and-interface-design
description: "Design or review stable APIs, CLI command surfaces, JSON contracts, module boundaries, error semantics, and compatibility behavior before implementation. Use when adding or changing an interface; use design-algorithm first if the need for the interface is still in question."
---

# API And Interface Design

Make the contract explicit before implementation details harden around it.

This skill is adapted from `addyosmani/agent-skills`; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. Name the caller, owner, and job the interface serves.
2. Find the existing contract: docs, command help, schema, tests, examples, or callers.
3. Define the smallest stable surface:
   - inputs and defaults
   - output shape
   - error semantics
   - compatibility and migration behavior
   - examples that should keep working
4. Prefer typed, explicit contracts over prompt-shaped or shell-shaped behavior.
5. Decide which invalid states should be rejected at the boundary.
6. Update docs and tests with the contract, not just the implementation.

## Forge Bias

For Forge CLIs:

- keep output JSON-first and stable
- use explicit verbs for writes
- keep destructive actions behind explicit flags
- avoid hidden Git, browser, or network side effects
- prefer singular top-level resource nouns when adding command surface

## Output

Include:

- chosen interface
- compatibility decision
- rejected alternatives
- tests or examples proving the contract

## Checks

- Do not add flags or fields only because a similar tool has them.
- Do not widen a public contract to avoid making one local caller clearer.
