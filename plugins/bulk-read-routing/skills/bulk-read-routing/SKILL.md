---
name: bulk-read-routing
description: Respond to a Codex bulk-read hook block by replacing an oversized full-file read with targeted inspection or bounded subagent delegation. Use when the hook reports that a file exceeds the configured line threshold; do not use for editing, reasoning, or already bounded reads.
---

# Bulk Read Routing

Keep large files out of the primary agent context unless the task requires the
complete file.

When the hook blocks a read:

1. Use `rg` to locate relevant symbols or text when the question is specific.
2. Read only the required range with a bounded command such as `sed -n`.
3. Delegate a summary when the question requires broad understanding and
   subagents are authorized and available.
4. Give the delegated task a concrete question. Require concise findings with
   file and line references.
5. Spot-check the findings before using them for design or edits.
6. Keep control of the task. Treat the suggested role as a starting point, not
   a mandatory route.
7. Choose the recovery path when delegation fails. Failure includes an
   unavailable role, a spawn or tool error, a timeout, a malformed response,
   or a result that does not satisfy the task.
8. Retry, select another role, or return to targeted reads according to the
   task's cost, risk, and remaining uncertainty.

The denial message uses the current model slug to select advice from
`config/delegation.json`. Planner-tier models receive a stronger recommendation
to delegate broad reading to the configured role. Efficient-tier models receive
a stronger recommendation to use targeted reads first. Unknown models receive
neutral advice. The role name is stable; Codex agent configuration owns the
model assigned to that role.

Run `just install-agent-roles` from the repository root to install the supplied
`bulk_reader` and `bulk_reader_fast` personal roles. Edit
`config/agent-roles.json` before installation to choose their models, reasoning
effort, and `default` or `fast` service tier. The installer refuses to overwrite
a different existing role unless the user explicitly passes `--force` to the
script.

Keep editing, security and privacy judgment, unresolved product decisions, and
final verification with the primary agent. Do not delegate a small read when
coordination overhead exceeds the likely context savings.

The hook does not own orchestration. It does not require a fixed escalation
order, and it does not prevent the primary agent from continuing after an
administrative or semantic delegation failure. The primary agent decides when
the evidence is sufficient and which fallback is appropriate.

The hook is conservative. It blocks recognizable full-file reads only.
Ambiguous shell commands and bounded reads pass through. When the hook cannot
resolve a relative file against its working directory, retry with an absolute
path so it can verify the file size.
