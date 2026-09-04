---
name: webwright
description: Use when the user asks Codex to automate a live web task by writing and running a local Playwright script with screenshots, logs, and a rerunnable `final_script.py`, or to craft a reusable browser-task CLI. Do not use for simple static web reads or frontend debugging where `chrome-devtools-mcp` is the better inspection tool.
---

# Webwright

Use this skill for code-as-action browser automation: the agent writes local
Playwright code, runs it, inspects screenshots and logs, fixes the script, and
finishes with a rerunnable artifact.

This Forge-managed copy is adapted from Microsoft Webwright. It provides the
skill instructions and reference files only. It does not install the upstream
Python package, browser binaries, plugin manifests, or slash-command assets.

## Use this when

- the user asks to automate a web task such as search, filtering, form fill,
  comparison, checkout-free selection, or data extraction
- the task needs current site UI evidence rather than a one-shot text answer
- the user wants a rerunnable `final_script.py`, saved screenshots, and an
  action log
- the user asks to parameterize the workflow or turn it into a reusable CLI

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

For this Forge-managed skill snapshot, make setup explicit and use `uvx` for
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

Required artifacts:

- `plan.md`
- `final_runs/run_<id>/final_script.py`
- `final_runs/run_<id>/screenshots/final_execution_<step>_<action>.png`
- `final_runs/run_<id>/final_script_log.txt`

Each clean execution uses a new `final_runs/run_<id>/` folder, where `<id>` is
an integer higher than any existing `run_*` folder.

Browser rules:

- launch a fresh local Firefox browser for each Playwright run
- run Playwright scripts with `uvx --with playwright python ...`
- use `viewport={"width": 1280, "height": 1800}`
- do not use `page.screenshot(full_page=True)`
- reconstruct state from scratch in the script; do not rely on a persistent
  browser session

## Workflow

1. Plan the task as critical points in `plan.md`. Every explicit constraint,
   filter, sort, selection, and required final datum gets its own checklist
   item.
2. Explore with scratch Playwright scripts. Print URL, title, visible labels,
   and ARIA snapshots. Save screenshots when visual evidence matters.
3. Author `final_script.py` inside a fresh `final_runs/run_<id>/`. Instrument
   every constraint-relevant action with a log line and a screenshot.
4. Execute the final script once from scratch. Capture stdout and stderr.
5. Self-verify every critical point against `plan.md`, the action log, and
   screenshots. Fix ambiguous or failed evidence and rerun in a new run folder.
6. Finish only when every critical point is checked off with concrete cited
   evidence, and report the final datum to the user.

## Hard Rules

- Run one shell command at a time and observe its output before continuing.
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
- Only claim blockers such as access denial or unavailable controls after
  repeated evidence from the actual site UI.
- Do not log secrets, session cookies, tokens, payment details, or personal
  account data into `plan.md`, screenshots, or `final_script_log.txt`.
- If the task asks for a final datum, append it to `final_script_log.txt` and
  state it explicitly to the user.
- Once `final_script.py` exists, prefer incremental edits over rewriting the
  whole file.

## Reference Files

- `reference/playwright_patterns.md`: browser-launch skeleton, ARIA snapshot
  recipes, screenshot naming, and log format.
- `reference/workflow.md`: detailed plan -> explore -> final -> verify
  workflow and completion gate.
- `reference/cli_tool_mode.md`: reusable CLI contract, parameter table,
  import-safety check, and `step 0 params:` log rule.
