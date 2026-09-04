---
name: forge-cli
description: "Use the Forge CLI for local Forge management: install checks, version checks, doctor diagnostics, permissions, self-update, managed tools, skill installation support, and troubleshooting Forge-provided automation. Use when the user asks about Forge itself or when another Forge workflow fails because the CLI, auth, permissions, or installed tools are missing or stale."
---

# Forge CLI

Use `forge` for Forge management and diagnostics. Use task-specific skills for actual GitHub, Linear, Slack, release, diagram, or Codex thread work once the right workflow is known.

## Quick Checks

Start with:

```bash
forge version
forge doctor
forge --help
```

Treat `forge doctor` required failures as blockers for Forge-backed workflows. Optional integration warnings are blockers only when they affect the requested task.

## Tool Discovery

Inspect available Forge-managed tools before assuming a command exists:

```bash
forge version
forge skills list
forge --help
```

If the installed Forge version does not support those commands, use `forge --help` and the current `iancleary/forge` repository documentation.

## Updates

Before updating Forge or managed tools, check the current version and working directory state:

```bash
forge version
git status --short
```

Use Forge's documented update command when available. Do not replace local development builds with a packaged release unless the user asked for that.

## Failure Recovery

- If `forge` is missing from `PATH`, inspect the shell profile and Forge install docs before editing environment files.
- If a Forge subcommand is missing, check whether it was renamed, moved behind `forge tool`, or removed in the installed version.
- If auth fails for a backing service, use that service's normal auth checks as well as `forge doctor`.
- If a command emits JSON, parse it with structured tooling instead of text slicing.
