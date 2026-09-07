---
name: webwright
description: Use when the user explicitly requests Webwright or a rerunnable Playwright browser automation script or CLI. Produce and verify the script with task-appropriate execution evidence.
---

# Webwright

Use this skill for code-as-action browser automation: the agent writes local
Playwright code, runs it, inspects screenshots and logs, fixes the script, and
finishes with a rerunnable artifact.

This copy is adapted from Microsoft Webwright. It provides the
skill instructions and reference files only. It does not install the upstream
Python package, browser binaries, plugin manifests, or slash-command assets.

## Use this when

- the user explicitly invokes this skill
- the user requests a rerunnable browser automation script or CLI

## Do not use this when

- a static fetch, official API, or normal web search answers the question
- the job is frontend debugging, console/network inspection, DOM inspection, or
  performance tracing; use `chrome-devtools-mcp` for that
- the task requires hidden persistent login state, personal credentials, or
  private account data that the user has not explicitly authorized
- the task would submit purchases, bookings, payments, account changes, or
  other irreversible mutations without an explicit user approval step
- the task asks to bypass authentication, paywalls, anti-bot controls, rate
  limits, or site policy

## Setup boundary

For the full upstream Codex plugin, follow the official Webwright marketplace
path:

```bash
codex plugin marketplace add microsoft/Webwright
```

Then open Codex, use `/plugins`, install Webwright, and restart Codex.

For this skill snapshot, make setup explicit and use `uvx` for
Playwright. The Playwright CLI should be invoked as a uv tool, and every
Playwright script should be run through a uvx Python environment that includes
the `playwright` package. Do not run package or browser installs as a hidden
side effect of a web task; ask the user or treat setup as its own task.

```bash
uvx --from playwright playwright install firefox
```

When running scratch scripts or `final_script.py`, use:

```bash
uvx --with playwright python final_script.py
```

If pinning Playwright, use the same package spec for both commands, such as
`playwright==<version>`, so the browser binary and Python package stay coupled.

## Modes

Default one-shot mode:

- produce a `final_script.py` that solves the task for the literal values the
  user provided
- use this unless the user asks for reuse or parameterization

CLI tool mode:

- produce a reusable `final_script.py` with one parameterized function,
  a Google-style `Args:` docstring, and an `argparse` CLI
- trigger this when the user says "parameterize", "make it reusable", "turn
  this into a CLI", "craft a tool", or similar
- follow `reference/cli_tool_mode.md`

## Workspace Contract

Pick a `WORKSPACE_DIR`, such as `outputs/<task_id>/`, and keep all generated
code, screenshots, logs, and notes inside it.

Required output is a rerunnable `final_script.py` and evidence that its result
satisfies the task. Choose supporting artifacts to match the complexity:

- use a short checklist in the response or `plan.md` for multi-step tasks
- capture logs or structured results for values and actions
- save and inspect screenshots when layout or visible selected state matters

Use separate run folders when needed to distinguish current evidence from
earlier attempts. Simple runs can keep the script and evidence together.

Browser rules:

- use the requested browser; Firefox is a default when none is specified
- run Playwright scripts with `uvx --with playwright python ...`
- choose a viewport and screenshot scope that make the relevant state legible
- verify reruns from documented starting state; identify any authorized login
  prerequisites instead of relying on unexplained session state

## Workflow

1. Identify the requested constraints and final result. Use a written checklist
   when it helps track a multi-step task.
2. Explore with scratch Playwright scripts. Print URL, title, visible labels,
   and ARIA snapshots. Save screenshots when visual evidence matters.
3. Author `final_script.py` with assertions, logs, or screenshots sufficient to
   verify the requested constraints.
4. Execute the final script from its documented starting state. Capture errors.
5. Verify each requirement against the result and relevant evidence. Fix failed
   or ambiguous checks and rerun when safe; avoid repeating external mutations.
6. Report the result, script path, rerun command, and any unresolved limitation.

## Hard Rules

- Use stable selectors and current-run evidence; never guess UI state.
- If a site exposes a dedicated control for a requirement, use that control.
  A search-box query does not satisfy an explicit filter, sort, style, or
  attribute requirement.
- Ranking language such as `cheapest`, `highest-rated`, `latest`, or `most
  reviewed` must be grounded in the site's own sort or filter control.
- Numeric, date, quantity, and unit constraints are exact. Wider buckets are
  failures unless the site offers no exact control.
- If selected state is hidden after a drawer, accordion, modal, or dropdown
  closes, reopen it or capture a visible chip or summary before treating it as
  verified.
- Ground blockers in observed UI or execution evidence. Stop when further
  attempts cannot usefully resolve the issue.
- Do not log secrets, session cookies, tokens, payment details, or personal
  account data into `plan.md`, screenshots, or `final_script_log.txt`.
- If the task asks for a final datum, retain it in the run evidence and state it
  explicitly to the user.
- Once `final_script.py` exists, prefer incremental edits over rewriting the
  whole file.

## Reference Files

- `reference/playwright_patterns.md`: browser-launch skeleton, ARIA snapshot
  recipes, screenshot naming, and log format.
- `reference/workflow.md`: detailed plan -> explore -> final -> verify
  workflow and completion gate.
- `reference/cli_tool_mode.md`: reusable CLI contract, parameter table,
  import-safety check, and `step 0 params:` log rule.
