---
name: security-and-hardening
description: "Review concrete security risks or changes to trust boundaries, such as untrusted input reaching execution, secrets, or privileged operations. Use for requested security reviews or meaningful boundary changes, not routine file or command use."
---

# Security And Hardening

Find concrete, actionable risk at the trust boundary.

This skill is adapted from `addyosmani/agent-skills`; see `THIRD_PARTY_NOTICES.md` for upstream provenance and MIT license notice.

## Workflow

1. Identify assets, actors, and the trust boundary.
2. Trace untrusted input through parsing, validation, execution, logging, and storage.
3. Check for:
   - command or path injection
   - secret disclosure in logs, errors, commits, or generated files
   - unsafe default permissions
   - silent destructive actions
   - broad tokens or unnecessary privilege
   - dependency execution without a pinned or documented contract
4. Prefer rejecting invalid input at the edge.
5. Keep mitigations small and observable.
6. Add regression proof for accepted findings.

## Forge Bias

For agent-facing CLIs, the highest-value hardening usually is:

- explicit write verbs
- `--force` for destructive actions
- JSON errors that state the blocked action
- no shell execution when typed APIs are available
- no secrets in output, tests, fixtures, or docs

## Output

Lead with accepted findings only:

- risk
- exploitable path or failure mode
- fix
- proof

Mention rejected speculative findings only when they explain a decision.

## Checks

- Do not cripple legitimate workflows for vague risk.
- Do not suppress a concrete risk without leaving auditable rationale.
