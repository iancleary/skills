---
name: documentation-and-adrs
description: "Write or update durable technical documentation, workflow docs, command contracts, architecture decision records, and policy guidance. Use when a change affects how future agents or humans should understand, operate, or maintain a system."
---

# Documentation And ADRs

Document the reason future maintainers need, not a transcript of the work.

This skill is adapted from `addyosmani/agent-skills`; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. Decide the artifact type:
   - command behavior or examples -> product/spec docs
   - workflow or operating policy -> AGENTS.md, skill, or workflow doc
   - durable architectural choice -> ADR or decision section
   - release-visible behavior -> release notes or changelog
2. Write the decision, context, and consequences.
3. Keep implementation docs aligned with actual behavior.
4. Link to the owning command, module, script, or skill when that helps maintenance.
5. Remove stale guidance instead of adding contradictory guidance nearby.

## ADR Threshold

Use an ADR-style decision only when the choice is durable and has meaningful alternatives. For small local behavior, update the nearest spec or README instead.

## Forge Bias

For Forge:

- docs describe command contracts under `docs/`
- repo-local `AGENTS.md` reinforces project behavior
- managed skills carry portable workflow instructions
- `codex/user/AGENTS.md` carries user-scoped portable baseline policy

## Output

Include:

- artifact updated
- decision or behavior documented
- stale guidance removed or left intentionally
- verification that docs match implementation when applicable

## Checks

- Do not document aspirational behavior as if it exists.
- Do not duplicate policy across docs and skills unless each location has a clear routing purpose.
