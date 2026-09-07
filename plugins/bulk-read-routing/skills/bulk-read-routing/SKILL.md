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

Keep editing, security and privacy judgment, unresolved product decisions, and
final verification with the primary agent. Do not delegate a small read when
coordination overhead exceeds the likely context savings.

The hook is conservative. It blocks recognizable full-file reads only.
Ambiguous shell commands and bounded reads pass through.
