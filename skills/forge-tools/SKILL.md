---
name: forge-tools
description: "Route Codex to the right Forge CLI or workflow skill for Linear, Slack retrieval or assistant actions, Codex session retrieval, loop design, local Forge management, release helpers, diagrams, or other Forge-provided automation. Use when a task may involve more than one Forge skill or when the correct narrow Forge workflow is not obvious yet."
---

# Forge Tools

Use this as the router before reaching for a Forge command by memory. Prefer the narrow skill when one clearly matches the request; otherwise inspect Forge's current command surface and choose the smallest suitable tool.

## Route

- For Forge installation, updates, diagnostics, permissions, self-management, or available tool discovery, use `forge-cli`.
- For GitHub issues, pull requests, releases, or checks, use the normal GitHub tooling first; use Forge only when this repo has a documented Forge-specific helper.
- For Linear work, use the Linear Forge workflow if available.
- For Slack reads, searches, threads, replies, reactions, or file uploads, use the Slack Forge workflows if available and respect the conversation's permission boundary.
- For Codex session archives, use the Codex threads Forge workflow if available.
- For release execution, use repo-local release instructions first; use Forge release helpers only when those instructions point to them.
- For diagrams, use the diagram-specific Forge workflow when a skill names it.

## Discovery

When the command or workflow is uncertain, inspect the installed Forge surface instead of guessing:

```bash
forge --help
forge skills list
forge doctor
```

If `forge skills list` is unavailable, use `forge --help` and the repo-local instructions for the task.

## Working Rules

- Prefer structured command output (`--json`, `--jq`, or equivalent) when Forge supports it.
- Keep external writes explicit: comments, Slack sends, GitHub mutations, deploys, and release publishes should be intentional user-requested actions.
- Do not introduce a new Forge dependency into a repo unless it is already part of that repo's workflow or the user asked for it.
- If Forge is missing or broken, switch to `forge-cli` diagnostics before falling back to ad hoc shell work.
