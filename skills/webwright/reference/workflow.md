# Workflow

This is the detailed Webwright loop for Codex. The original Webwright harness
used model-side image QA and self-reflection tools. In this skill, the agent
replaces those with direct inspection of saved screenshots and reasoning
against `plan.md`.

## 1. Plan

Parse the task into critical points and write `WORKSPACE_DIR/plan.md`:

```markdown
# Task
<verbatim task description>

# Critical Points
- [ ] CP1: <constraint / filter / sort / selection / required datum>
- [ ] CP2: ...
```

Rules for critical points:

- one independently verifiable requirement per CP
- numeric, date, quantity, and unit CPs must be exact
- ranking CPs such as `cheapest`, `best-selling`, or `highest-rated` must
  reference the site's actual sort or filter control
- if the task asks for a final datum, make that datum its own CP

## 2. Explore

Discover stable selectors, confirm every required filter control exists, and
identify how to capture evidence for each CP.

- run scratch Playwright scripts inside `WORKSPACE_DIR/` with
  `uvx --with playwright python`
- save scratch PNGs under `WORKSPACE_DIR/screenshots/`
- print URL, title, visible labels, and `aria_snapshot()` for the relevant
  region at every step
- inspect saved PNGs when ARIA evidence is ambiguous
- expand drawers, accordions, dropdowns, and mobile filter panels before
  concluding that a filter is unavailable
- never use a search-box query as a substitute for a dedicated filter control

## 3. Author `final_script.py`

Create a fresh `final_runs/run_<id>/` and place `final_script.py` inside it.
Use the next integer above any existing `run_*`.

Instrument the script:

- viewport 1280x1800, headless local Firefox, no full-page screenshots
- one `final_execution_<step>_<action>.png` per CP
- one `step <n> action: <reason and action>` log line per
  constraint-relevant interaction
- the final datum printed into `final_script_log.txt` at the end

Each screenshot should map clearly to a CP from `plan.md`.

## 4. Execute

Run the script once from scratch:

```bash
uvx --with playwright python final_runs/run_<id>/final_script.py
```

If it crashes, fix it and re-execute. If a partial run produced screenshots
that no longer match the fixed flow, use a new run folder so the final folder
reflects one clean execution.

## 5. Self-Verify

For every CP in `plan.md`:

1. Identify the screenshot or log line that proves it.
2. Inspect each cited PNG.
3. Confirm the evidence is unambiguous:
   - selected filter chips or summaries are visible
   - numeric and date values match exactly
   - sorting is applied through the site's own control
   - required submit, search, or apply actions visibly happened
   - the final datum is legible or logged
4. Tick the CP only when the evidence is concrete.

If any CP fails, diagnose the specific issue, fix `final_script.py`, run again
inside `final_runs/run_<id+1>/`, and re-verify against `plan.md`.

Empty result sets are acceptable only when the correct filters were
demonstrably applied.

## 6. Done

Stop only when all of the following are true:

1. `plan.md` exists with every CP enumerated as a checklist item.
2. `final_runs/run_<id>/final_script.py` ran cleanly from scratch.
3. The run produced `final_script_log.txt` and all CP screenshots.
4. Every CP is checked off with a cited screenshot or log line.
5. The final datum, if any, is reported to the user and present in the log.
6. `ls -R final_runs/run_<id>` and `cat final_runs/run_<id>/final_script_log.txt`
   show the expected artifacts.

If any item is false, diagnose, fix, and rerun in a new `run_<id+1>/`.
