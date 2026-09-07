---
name: api-and-interface-design
description: "Design or review public or shared API, CLI, and data contracts when callers depend on stable inputs, outputs, errors, or compatibility. Use for new shared interfaces or contract changes, not routine internal edits."
---

# API And Interface Design

Make the contract explicit before implementation details harden around it.

Use this for contracts shared across callers or published to users. If the need
for the interface remains unresolved, use `design-algorithm` when available.

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

## CLI Contracts

For commands used by automation:

- preserve stable machine-readable output
- use explicit verbs for writes
- keep destructive actions behind explicit flags
- avoid hidden Git, browser, or network side effects
- follow the existing command naming convention

## Output

Include:

- chosen interface
- compatibility decision
- rejected alternatives
- tests or examples proving the contract

## Checks

- Do not add flags or fields only because a similar tool has them.
- Do not widen a public contract to avoid making one local caller clearer.
